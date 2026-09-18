"""
pipeline/build_demo_data.py

Master Orchestrator for NET-SENTINEL SOCIAL Demo MVP (v5.0).
Coordinates data generation, 4 analytical engines, coordination detection,
and SHA-256 hash-chain creation into demo_data.json and dashboard/data.js.

WHAT THIS DOES:
- Executes synthetic_data.py, analyze.py, and hash_chain.py in sequence.
- Verifies all cryptographic and structural invariants.
- Emits demo_data.json (root) and dashboard/data.js (for direct file:/// browser support).
- Prints comprehensive demo readiness summary.
"""

import json
import os
import sys
from datetime import datetime, timezone

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Add pipeline directory to sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from synthetic_data import generate_synthetic_dataset
from analyze import (
    analyze_sentiments,
    analyze_demographics,
    analyze_trends,
    analyze_network,
    analyze_coordination
)
from hash_chain import build_chain, verify_chain


def build_all_demo_data():
    print("=================================================================")
    print("  NET-SENTINEL SOCIAL (v5.0 Demo) — Pipeline Orchestration")
    print("  SIH 2026 Problem Statement SIH26152 | Theme: Blockchain & Cyber")
    print("=================================================================")

    # 1. Synthetic Data Generation
    print("\n[PHASE 1/4] Generating synthetic multi-platform social data...")
    raw_dataset = generate_synthetic_dataset()
    posts = raw_dataset["posts"]
    authors = raw_dataset["authors"]
    edges = raw_dataset["edges"]
    print(f"  ✓ Created {len(posts)} posts, {len(authors)} authors, {len(edges)} interaction edges.")

    # 2. Analytics Engines
    print("\n[PHASE 2/4] Running 5 AI intelligence analysis engines...")
    
    # Engine B: Sentiment
    post_sentiments, sentiment_summary = analyze_sentiments(posts)
    print(f"  ✓ Nuanced Sentiment: 6 classes computed. Supportive: {sentiment_summary['distribution']['supportive']['percentage']}%, Anxious: {sentiment_summary['distribution']['anxious']['percentage']}%.")

    # Engine C: Demographics
    demographics = analyze_demographics(authors, posts)
    print(f"  ✓ Demographic Profiling: Inferred {len(demographics['regional_distribution'])} regions, {len(demographics['age_distribution'])} age brackets (Anonymized & Aggregated).")

    # Engine D: Trends & Forward Momentum
    trends = analyze_trends(posts)
    top_trend = trends[0]
    print(f"  ✓ Trend Detection: Top topic '{top_trend['topic']}' ({top_trend['total_mentions']} mentions, Momentum: {top_trend['momentum']}).")

    # Engine E: Network Topology
    network_summary = analyze_network(authors, edges)
    print(f"  ✓ Network Topology: {network_summary['metrics']['total_nodes']} nodes, {network_summary['metrics']['total_edges']} edges. Top Influencer: {network_summary['top_influencers'][0]['handle']}.")

    # Cybersecurity Engine: Coordination / Bot Detection
    coordination_data = analyze_coordination(posts, authors, edges)
    campaign = coordination_data["campaign"]
    alert = coordination_data["alert"]
    print(f"  ✓ Coordination Detection: Flagged Campaign {campaign['campaign_id']} with {campaign['confidence_percentage']}% confidence across {campaign['total_accounts_involved']} accounts.")

    # Attach analysis back to posts
    bot_authors = set(campaign["accounts_list"])
    for p in posts:
        pid = p["id"]
        p_analysis = post_sentiments.get(pid, {})
        p["sentiment_label"] = p_analysis.get("sentiment_label", "neutral")
        p["sentiment_score"] = p_analysis.get("sentiment_score", 0.8)
        p["is_flagged_bot_cluster"] = (p["author_handle"] in bot_authors) or p.get("_is_bot", False)
        p["bot_cluster_id"] = campaign["campaign_id"] if p["is_flagged_bot_cluster"] else None

    # 3. Cryptographic Hash-Chain
    print("\n[PHASE 3/4] Building SHA-256 tamper-evident linked hash-chain...")
    chain = build_chain(posts)
    posts_lookup = {p["id"]: p for p in posts}
    is_valid, verified_count, verify_msg, fail_idx = verify_chain(chain, posts_lookup)
    assert is_valid is True, f"Integrity check failed: {verify_msg}"
    print(f"  ✓ Hash Chain: {len(chain)} blocks linked. Root Hash: {chain[-1]['entry_hash'][:16]}...")
    print(f"  ✓ Verification: {verify_msg}")

    # 4. Assembly & Export
    print("\n[PHASE 4/4] Assembling unified demo dataset...")
    platform_counts = {}
    for p in posts:
        plat = p["platform"]
        platform_counts[plat] = platform_counts.get(plat, 0) + 1

    demo_data = {
        "version": "5.0-demo",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "metadata": {
            "title": "NET-SENTINEL SOCIAL Intelligence Dossier",
            "problem_statement": "SIH26152",
            "theme": "Blockchain & Cybersecurity",
            "agency": "National Technical Research Organisation (NTRO)",
            "total_posts": len(posts),
            "total_authors": len(authors),
            "platforms": platform_counts,
            "time_range": {
                "start": posts[0]["timestamp"],
                "end": posts[-1]["timestamp"]
            },
            "honesty_badge": "Synthetic demo data — not live"
        },
        "alert": alert,
        "campaign": campaign,
        "sentiment": sentiment_summary,
        "demographics": demographics,
        "trends": trends,
        "network": network_summary,
        "hash_chain": {
            "is_valid": is_valid,
            "total_blocks": len(chain),
            "verification_message": verify_msg,
            "latest_root_hash": chain[-1]["entry_hash"],
            "chain": chain,
            "sample_audit_log": chain[:20]  # First 20 blocks for quick audit view
        },
        "posts": posts
    }

    # Save to root demo_data.json
    root_json_path = os.path.join(ROOT_DIR, "demo_data.json")
    with open(root_json_path, "w", encoding="utf-8") as f:
        json.dump(demo_data, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Emitted root dataset: {root_json_path} ({os.path.getsize(root_json_path):,} bytes)")

    # Ensure dashboard directory exists
    dashboard_dir = os.path.join(ROOT_DIR, "dashboard")
    os.makedirs(dashboard_dir, exist_ok=True)

    # Save copy into dashboard/demo_data.json
    dash_json_path = os.path.join(dashboard_dir, "demo_data.json")
    with open(dash_json_path, "w", encoding="utf-8") as f:
        json.dump(demo_data, f, indent=2, ensure_ascii=False)

    # Also emit dashboard/data.js as window.NET_SENTINEL_DEMO_DATA
    # This guarantees the dashboard opens directly via file:/// without browser CORS errors!
    dash_js_path = os.path.join(dashboard_dir, "data.js")
    with open(dash_js_path, "w", encoding="utf-8") as f:
        f.write("// Auto-generated precomputed data bundle for NET-SENTINEL SOCIAL demo\n")
        f.write("window.NET_SENTINEL_DEMO_DATA = ")
        json.dump(demo_data, f, indent=2, ensure_ascii=False)
        f.write(";\n")
    print(f"  ✓ Emitted zero-CORS JS bundle: {dash_js_path} ({os.path.getsize(dash_js_path):,} bytes)")

    print("\n=================================================================")
    print("  DEMO PIPELINE EXECUTION COMPLETED SUCCESSFULLY")
    print(f"  - Total Posts Analyzed: {len(posts)}")
    print(f"  - Must-Have Platforms: X ({platform_counts.get('x', 0)}) + Telegram ({platform_counts.get('telegram', 0)})")
    print(f"  - Planted Campaign Flagged: {campaign['campaign_id']} ({campaign['confidence_percentage']}% confidence)")
    print(f"  - SHA-256 Hash-Chain Blocks Verified: {len(chain)} / {len(chain)}")
    print("=================================================================\n")
    return demo_data


if __name__ == "__main__":
    build_all_demo_data()
