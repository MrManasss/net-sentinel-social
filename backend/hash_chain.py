"""
pipeline/hash_chain.py

SHA-256 Tamper-Evident Linked Hash-Chain for NET-SENTINEL SOCIAL demo
(SIH 2026 Problem Statement SIH26152).

WHAT THIS DOES:
- Creates a cryptographic, linked SHA-256 audit log for each ingested social post.
- Computes post data hash from normalized payload (id, platform, author, text, timestamp).
- Links each block to the previous entry hash:
    entry_hash = SHA-256(index + timestamp + data_hash + prev_hash)
- Implements verify_chain() to mathematically validate complete chain integrity.
- Provides a comprehensive tamper test demonstrating that mutating even 1 character
  in a post immediately invalidates the chain and pinpoints the exact tampered block.

WHAT THIS DOES NOT DO:
- Does NOT claim to be a distributed blockchain or Hyperledger Fabric network.
  (Fabric anchoring is explicitly labeled as roadmap / future architecture).
"""

import hashlib
import json
import sys

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

GENESIS_PREV_HASH = "0" * 64


def sha256(data_str: str) -> str:
    """Computes standard hex SHA-256 digest."""
    return hashlib.sha256(data_str.encode("utf-8")).hexdigest()


def compute_post_hash(post: dict) -> str:
    """
    Computes deterministic SHA-256 hash of normalized post payload fields.
    """
    normalized_payload = (
        f"{post['id']}|{post['platform']}|{post['author_handle']}|"
        f"{post['text']}|{post['timestamp']}"
    )
    return sha256(normalized_payload)


def compute_entry_hash(index: int, timestamp: str, data_hash: str, prev_hash: str) -> str:
    """
    Computes cryptographic link hash for a chain block.
    """
    block_string = f"{index}:{timestamp}:{data_hash}:{prev_hash}"
    return sha256(block_string)


def build_chain(posts: list[dict]) -> list[dict]:
    """
    Builds a linked SHA-256 hash chain over a chronologically ordered list of posts.
    """
    chain = []
    prev_hash = GENESIS_PREV_HASH

    for idx, post in enumerate(posts):
        data_hash = compute_post_hash(post)
        entry_hash = compute_entry_hash(idx, post["timestamp"], data_hash, prev_hash)
        
        block = {
            "index": idx,
            "timestamp": post["timestamp"],
            "post_id": post["id"],
            "author_handle": post["author_handle"],
            "platform": post["platform"],
            "data_hash": data_hash,
            "prev_hash": prev_hash,
            "entry_hash": entry_hash
        }
        chain.append(block)
        prev_hash = entry_hash

    return chain


def verify_chain(chain: list[dict], posts_lookup: dict = None) -> tuple[bool, int, str, int]:
    """
    Verifies cryptographic integrity of the hash chain.
    
    Returns:
      (is_valid: bool, verified_count: int, message: str, failed_index: int or None)
    """
    if not chain:
        return False, 0, "Chain is empty.", None

    expected_prev = GENESIS_PREV_HASH

    for idx, block in enumerate(chain):
        # 1. Verify index sequence
        if block["index"] != idx:
            return False, idx, f"Block index discontinuity at #{idx} (got {block['index']})", idx

        # 2. Verify link to previous block
        if block["prev_hash"] != expected_prev:
            return (
                False, idx,
                f"Previous hash mismatch at Block #{idx}! Broken link in chain.",
                idx
            )

        # 3. If post lookup is available, verify data integrity against payload
        if posts_lookup and block["post_id"] in posts_lookup:
            actual_post_hash = compute_post_hash(posts_lookup[block["post_id"]])
            if block["data_hash"] != actual_post_hash:
                return (
                    False, idx,
                    f"TAMPER DETECTED: Post data hash mismatch at Block #{idx} (Post {block['post_id']})! "
                    f"Content was altered post-ingestion.",
                    idx
                )

        # 4. Verify block entry hash recalculation
        expected_entry = compute_entry_hash(
            block["index"], block["timestamp"], block["data_hash"], block["prev_hash"]
        )
        if block["entry_hash"] != expected_entry:
            return (
                False, idx,
                f"TAMPER DETECTED: Block #{idx} entry hash is invalid! Expected {expected_entry[:12]}..., got {block['entry_hash'][:12]}...",
                idx
            )

        expected_prev = block["entry_hash"]

    return True, len(chain), f"✓ Chain Valid: All {len(chain)} blocks cryptographically verified.", None


def run_tamper_test():
    """
    Executes the required tamper verification test:
    1. Validates untampered chain.
    2. Deliberately mutates a post text in block #5.
    3. Confirms verify_chain() immediately catches the tamper.
    """
    print("==================================================")
    print("NET-SENTINEL SOCIAL — Hash Chain Integrity Unit Test")
    print("==================================================")

    # Sample posts
    test_posts = [
        {"id": f"pst_00{i}", "platform": "x", "author_handle": f"@user_{i}",
         "text": f"Audit post record #{i}", "timestamp": f"2026-09-16T10:{i:02d}:00Z"}
        for i in range(10)
    ]
    posts_lookup = {p["id"]: dict(p) for p in test_posts}

    # Build chain
    chain = build_chain(test_posts)
    print(f"[TEST 1] Verifying clean chain of {len(chain)} blocks...")
    valid, count, msg, fail_idx = verify_chain(chain, posts_lookup)
    assert valid is True, f"Clean chain failed verification: {msg}"
    print(f"  PASS: {msg}")

    # Test Tamper Scenario A: Mutate text of post #5
    print("\n[TEST 2] Simulating unauthorized data mutation in Post #5 payload...")
    tampered_posts = {k: dict(v) for k, v in posts_lookup.items()}
    tampered_posts["pst_005"]["text"] = "MODIFIED / TAMPERED CONTENT BY MALICIOUS ACTOR"
    
    valid, count, msg, fail_idx = verify_chain(chain, tampered_posts)
    print(f"  Result: valid={valid}, fail_idx={fail_idx}")
    print(f"  Diagnostic: {msg}")
    assert valid is False and fail_idx == 5, "Tamper was not detected at block #5!"
    print("  PASS: Tampered post data was successfully caught and flagged!")

    # Test Tamper Scenario B: Mutate entry hash in block #7
    print("\n[TEST 3] Simulating ledger block hash modification at Block #7...")
    tampered_chain = [dict(b) for b in chain]
    tampered_chain[7]["entry_hash"] = "deadbeef" * 8
    
    valid, count, msg, fail_idx = verify_chain(tampered_chain, posts_lookup)
    print(f"  Result: valid={valid}, fail_idx={fail_idx}")
    print(f"  Diagnostic: {msg}")
    assert valid is False and fail_idx in [7, 8], "Chain link breakage was not caught!"
    print("  PASS: Broken hash chain link was successfully detected!")

    print("\n==================================================")
    print("ALL INTEGRITY TESTS PASSED SUCCESSFULLY.")
    print("==================================================")


if __name__ == "__main__":
    run_tamper_test()
