"""
Issue #13 - Interaction network analysis module (Member B).

Input  : DataFrame with columns
           source_account, target_account, interaction_type, timestamp, platform
         (agree this schema with Prashant's normalized feed)
Output : plain dicts / lists (JSON-safe) so FastAPI + React can use them directly.
"""
from __future__ import annotations

import networkx as nx
import numpy as np
import pandas as pd

REQUIRED_COLS = {"source_account", "target_account", "interaction_type", "timestamp"}
ALERT_THRESHOLD = 0.60  # tune with Hitesh on real data; his text-similarity score can be blended in later


# --------------------------------------------------------------------------- graph
def build_graph(interactions: pd.DataFrame) -> nx.DiGraph:
    """Nodes = accounts. Edge u->v = u interacted with v (weight = count)."""
    missing = REQUIRED_COLS - set(interactions.columns)
    if missing:
        raise ValueError(f"interactions is missing columns: {sorted(missing)}")

    df = interactions.dropna(subset=["source_account", "target_account"]).copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)  # utc=True: works whether or not the source has a timezone
    df = df[df["source_account"] != df["target_account"]]  # drop self-loops

    G = nx.DiGraph()
    for (u, v), g in df.groupby(["source_account", "target_account"]):
        G.add_edge(
            u, v,
            weight=int(len(g)),
            types=g["interaction_type"].value_counts().to_dict(),
            first_ts=g["timestamp"].min().isoformat(),
            last_ts=g["timestamp"].max().isoformat(),
        )

    # per-account activity times (as the actor) -> used for burst detection
    for acct, g in df.groupby("source_account"):
        G.nodes[acct]["ts"] = (g["timestamp"] - pd.Timestamp("1970-01-01", tz="UTC")).dt.total_seconds().to_numpy()
    if "platform" in df.columns:
        for acct, g in df.groupby("source_account"):
            G.nodes[acct]["platform"] = g["platform"].mode().iat[0]
    return G


# --------------------------------------------------------------------------- influence
def get_influencers(G: nx.DiGraph, top_k: int = 10) -> list[dict]:
    """Rank accounts by PageRank (+ degree and betweenness for context)."""
    if G.number_of_nodes() == 0:
        return []
    pr = nx.pagerank(G, weight="weight")
    k = min(200, G.number_of_nodes())  # sampled betweenness keeps it fast on big graphs
    bt = nx.betweenness_centrality(G, k=k, weight=None, seed=1)
    rows = [{
        "account": n,
        "pagerank": round(pr[n], 5),
        "in_degree": int(G.in_degree(n)),
        "out_degree": int(G.out_degree(n)),
        "betweenness": round(bt[n], 5),
    } for n in G.nodes]
    rows.sort(key=lambda r: r["pagerank"], reverse=True)
    return rows[:top_k]


# --------------------------------------------------------------------------- clustering
def _burst_score(timestamps: np.ndarray, window_s: int = 600) -> float:
    """Largest share of a cluster's actions that fall inside one `window_s` window (0-1)."""
    if len(timestamps) < 5:
        return 0.0
    ts = np.sort(timestamps)
    j = np.searchsorted(ts, ts + window_s, side="right")
    return float((j - np.arange(len(ts))).max() / len(ts))


def detect_clusters(G: nx.DiGraph, min_size: int = 4, seed: int = 1) -> list[dict]:
    """
    Louvain communities, each scored for 'puppet-account / coordinated' behaviour.

    suspicion_score (0-1) = 0.35 * temporal_burst
                          + 0.25 * insularity   (share of edge weight staying inside the group)
                          + 0.20 * density
                          + 0.20 * reciprocity  (mutual interactions)
    Flagged when score >= ALERT_THRESHOLD.
    """
    if G.number_of_edges() == 0:
        return []
    U = nx.Graph()
    U.add_nodes_from(G.nodes)
    for u, v, d in G.edges(data=True):  # merge u->v and v->u into one undirected weight
        w = d["weight"] + (U[u][v]["weight"] if U.has_edge(u, v) else 0)
        U.add_edge(u, v, weight=w)

    comms = nx.community.louvain_communities(U, weight="weight", seed=seed)
    out = []
    for cid, members in enumerate(sorted(comms, key=len, reverse=True)):
        if len(members) < min_size:
            continue
        sub = G.subgraph(members)
        n = len(members)
        density = nx.density(sub)

        internal = sum(d["weight"] for _, _, d in sub.edges(data=True))
        total = sum(d["weight"] for m in members
                    for _, _, d in list(G.out_edges(m, data=True)) + list(G.in_edges(m, data=True)))
        insularity = (2 * internal) / total if total else 0.0  # internal edges counted twice in `total`

        recip = nx.reciprocity(sub) if sub.number_of_edges() else 0.0
        recip = 0.0 if recip is None else recip

        ts = np.concatenate([G.nodes[m]["ts"] for m in members if "ts" in G.nodes[m]] or [np.array([])])
        burst = _burst_score(ts)

        score = 0.35 * burst + 0.25 * min(insularity, 1) + 0.20 * min(density * 3, 1) + 0.20 * recip
        out.append({
            "cluster_id": cid,
            "size": n,
            "members": sorted(members),
            "density": round(density, 3),
            "insularity": round(insularity, 3),
            "reciprocity": round(recip, 3),
            "temporal_burst": round(burst, 3),
            "suspicion_score": round(score, 3),
            "flagged": score >= ALERT_THRESHOLD,
        })
    out.sort(key=lambda c: c["suspicion_score"], reverse=True)
    return out


# --------------------------------------------------------------------------- export for dashboard
def graph_to_json(G: nx.DiGraph, clusters: list[dict] | None = None, max_nodes: int = 400) -> dict:
    """Nodes/links JSON for react-force-graph / D3. Keeps the highest-PageRank nodes if graph is big."""
    clusters = clusters if clusters is not None else detect_clusters(G)
    cluster_of = {m: c["cluster_id"] for c in clusters for m in c["members"]}
    flagged = {m for c in clusters if c["flagged"] for m in c["members"]}

    pr = nx.pagerank(G, weight="weight") if G.number_of_nodes() else {}
    keep = set(sorted(pr, key=pr.get, reverse=True)[:max_nodes]) | flagged
    nodes = [{
        "id": n,
        "cluster": cluster_of.get(n, -1),
        "pagerank": round(pr[n], 5),
        "platform": G.nodes[n].get("platform"),
        "suspicious": n in flagged,
    } for n in keep]
    links = [{"source": u, "target": v, "weight": d["weight"]}
             for u, v, d in G.edges(data=True) if u in keep and v in keep]
    return {"nodes": nodes, "links": links,
            "summary": {"accounts": G.number_of_nodes(), "edges": G.number_of_edges(),
                        "flagged_clusters": sum(c["flagged"] for c in clusters)}}


def analyze_network(interactions: pd.DataFrame, top_k: int = 10) -> dict:
    """One-call entry point for the FastAPI layer."""
    G = build_graph(interactions)
    clusters = detect_clusters(G)
    return {
        "influencers": get_influencers(G, top_k),
        "clusters": [{k: v for k, v in c.items() if k != "members"} | {"members": c["members"][:50]}
                     for c in clusters],
        "graph": graph_to_json(G, clusters),
    }
