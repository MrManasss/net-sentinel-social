"""
Converts the real ingestion sample (post-level JSON) into the
interactions_df the network module expects (account-level edges).

Run: python load_sample_data.py
"""
import json
import pandas as pd


def load_posts(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def posts_to_interactions(posts: list[dict]) -> pd.DataFrame:
    """
    Turn 'post replies to post' into 'account interacted with account'.
    Only rows where reply_to is not null become an edge.
    """
    by_id = {p["post_id"]: p for p in posts}   # post_id -> the whole post, for lookups
    rows = []
    for p in posts:
        if not p["reply_to"]:
            continue                            # original post, not a reply -> no edge
        parent = by_id.get(p["reply_to"])
        if parent is None:
            continue                            # the parent post isn't in this file
        rows.append({
            "source_account": p["author_id"],           # the person replying
            "target_account": parent["author_id"],       # the person they replied to
            "interaction_type": "reply",
            "timestamp": p["timestamp"],
            "platform": p["platform"],
        })
    return pd.DataFrame(rows)


def posts_to_profiles(posts: list[dict]) -> pd.DataFrame:
    """
    One row per account. This sample has no age/gender/location -
    only what's actually in the file.
    """
    rows = []
    seen = set()
    for p in posts:
        if p["author_id"] in seen:
            continue
        seen.add(p["author_id"])
        a = p["author"]
        rows.append({
            "account_id": p["author_id"],
            "platform": p["platform"],
            "display_name": a["display_name"],
            "account_created_at": a["account_created_at"],
            "followers": a["followers"],
            "following": a["following"],
            "karma": a["karma"],
            # This sample has no age/gender/location - add them as empty so
            # demographics.py runs and correctly reports 0% coverage,
            # instead of crashing with a missing-column error.
            "age": None,
            "gender": None,
            "location": None,
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    posts = load_posts("sample_social_media.json")
    interactions = posts_to_interactions(posts)
    profiles = posts_to_profiles(posts)

    print(f"{len(posts)} posts -> {len(interactions)} interaction edges, {len(profiles)} unique accounts\n")
    print("interactions_df:")
    print(interactions.to_string(index=False))
    print("\nprofiles_df (head):")
    print(profiles.head().to_string(index=False))

    interactions.to_csv("interactions_from_sample.csv", index=False)
    profiles.to_csv("profiles_from_sample.csv", index=False)
    print("\nSaved interactions_from_sample.csv and profiles_from_sample.csv")
