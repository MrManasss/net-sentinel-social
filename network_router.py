"""
Network + demographics endpoints for the Net-Sentinel backend (issues #13, #15).

Add these two lines to backend.py to wire it in:

    from network_router import router as network_router
    app.include_router(network_router)

That's it - this file defines its own routes; backend.py doesn't need any
other changes.
"""
from fastapi import APIRouter

from backend import load_posts  # reuse backend.py's existing DATA_FILE lookup, don't duplicate it
from load_sample_data import posts_to_interactions, posts_to_profiles
from network_analysis import analyze_network
from demographics import analyze_demographics

# Same pattern as backend.py's DATA_FILE - one router, reuses the same data file.
router = APIRouter(prefix="/api/v1", tags=["network"])


@router.get("/network")
def get_network():
    """
    Issue #13. Returns:
      influencers - accounts ranked by PageRank
      clusters    - Louvain communities scored for coordinated ("puppet-account") behaviour
      graph       - nodes/links JSON for the React graph view
    """
    posts = load_posts()
    interactions = posts_to_interactions(posts)
    return analyze_network(interactions)


@router.get("/demographics")
def get_demographics():
    """
    Issue #15. Returns aggregated, coverage-scored age/gender/location
    estimates. With the current sample data (no age/gender/location fields
    yet) every field will correctly show 0% coverage - that's expected,
    not a bug. Re-check this once Prashant's feed includes those fields.
    """
    posts = load_posts()
    interactions = posts_to_interactions(posts)
    profiles = posts_to_profiles(posts)
    return analyze_demographics(profiles, interactions)
