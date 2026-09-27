"""
Issue #15 - Audience demographics module (Member B).

Input : profiles DataFrame -> account_id, platform, age, gender, location  (values may be missing)
        optional interactions DataFrame (for activity-by-hour)
Output: JSON-safe dicts of AGGREGATED estimates only.

Design rules (say these to the judges):
  * aggregate-only - never return per-person age/gender
  * every field reports its coverage (% of accounts where it is known)
  * groups smaller than `min_group` are suppressed (privacy)
  * anything not stated on a profile is labelled "unknown", not guessed
"""
from __future__ import annotations

import pandas as pd

AGE_BINS = [0, 17, 24, 34, 44, 54, 200]
AGE_LABELS = ["<18", "18-24", "25-34", "35-44", "45-54", "55+"]

# small city -> state alias map (extend as needed)
STATE_ALIASES = {
    "indore": "Madhya Pradesh", "bhopal": "Madhya Pradesh", "mp": "Madhya Pradesh",
    "mumbai": "Maharashtra", "pune": "Maharashtra", "nagpur": "Maharashtra",
    "delhi": "Delhi", "new delhi": "Delhi",
    "bengaluru": "Karnataka", "bangalore": "Karnataka",
    "chennai": "Tamil Nadu", "kolkata": "West Bengal", "lucknow": "Uttar Pradesh",
    "jaipur": "Rajasthan", "hyderabad": "Telangana", "ahmedabad": "Gujarat",
}


def normalize_location(raw) -> str | None:
    """'Indore, MP' -> 'Madhya Pradesh'. Returns None if unknown."""
    if raw is None or (isinstance(raw, float) and pd.isna(raw)) or not str(raw).strip():
        return None
    for part in str(raw).lower().replace("/", ",").split(","):
        part = part.strip()
        if part in STATE_ALIASES:
            return STATE_ALIASES[part]
    return "Other/Unmapped"


def _dist(series: pd.Series, min_group: int) -> dict:
    """Distribution of a categorical series with small-group suppression + coverage."""
    total = len(series)
    known = series.dropna()
    counts = known.value_counts()
    shares = {}
    suppressed = 0
    for k, c in counts.items():
        if c < min_group:
            suppressed += int(c)
        else:
            shares[str(k)] = round(c / len(known), 3) if len(known) else 0.0
    if suppressed:
        shares["Other (suppressed)"] = round(suppressed / len(known), 3)
    coverage = round(len(known) / total, 3) if total else 0.0
    return {
        "distribution": shares,
        "coverage": coverage,  # share of accounts where this field is known
        "confidence": "high" if coverage >= 0.7 else "medium" if coverage >= 0.4 else "low",
        "n_known": int(len(known)),
    }


def compute_demographics(profiles: pd.DataFrame, min_group: int = 5) -> dict:
    """Overall demographics estimate for a set of accounts."""
    df = profiles.copy()
    df["age_band"] = pd.cut(pd.to_numeric(df["age"], errors="coerce"),
                            bins=AGE_BINS, labels=AGE_LABELS)
    df["age_band"] = df["age_band"].astype(object).where(df["age_band"].notna(), None)
    # astype("string") first: if the whole column is empty, pandas reads it as a
    # number type and .str.lower() crashes. The "string" dtype keeps missing
    # values as missing while still allowing .str on the real values.
    df["gender"] = df["gender"].astype("string").str.lower()
    df["region"] = df["location"].map(normalize_location)
    return {
        "accounts": int(len(df)),
        "estimated": True,  # label in UI: "estimated audience distribution"
        "age": _dist(df["age_band"], min_group),
        "gender": _dist(df["gender"], min_group),
        "location": _dist(df["region"], min_group),
    }


def demographics_by(profiles: pd.DataFrame, group_col: str = "platform", min_group: int = 5) -> dict:
    """Same summary split by platform (or any column, e.g. a cluster id you joined in)."""
    return {str(k): compute_demographics(g, min_group)
            for k, g in profiles.groupby(group_col) if len(g) >= min_group}


def activity_by_hour(interactions: pd.DataFrame) -> dict:
    """Hour-of-day activity histogram (0-23) - useful chart + weak location/timezone proxy."""
    ts = pd.to_datetime(interactions["timestamp"])
    counts = ts.dt.hour.value_counts().reindex(range(24), fill_value=0)
    return {"hours": list(range(24)), "counts": [int(x) for x in counts]}


def analyze_demographics(profiles: pd.DataFrame, interactions: pd.DataFrame | None = None) -> dict:
    """One-call entry point for the FastAPI layer."""
    out = {"overall": compute_demographics(profiles),
           "by_platform": demographics_by(profiles, "platform")}
    if interactions is not None:
        out["activity_by_hour"] = activity_by_hour(interactions)
    return out
