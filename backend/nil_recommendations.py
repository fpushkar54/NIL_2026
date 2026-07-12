# ─────────────────────────────────────────────
#  NIL Valuation Engine · NIL Recommendations
# ─────────────────────────────────────────────

from backend.constants import NIL_RANGES


def get_nil_recommendation(tier: str, pvm_score: float) -> dict:
    """
    Returns NIL recommendation details based on tier.
    Returns a dict with keys: eligible, low, high, display, description
    """
    if tier == "Below NIL Threshold":
        return {
            "eligible": False,
            "low": 0,
            "high": 0,
            "display": "No Recommended NIL Allocation",
            "description": (
                "This player's current production metrics fall below the threshold "
                "for NIL valuation. Continued development and increased statistical "
                "production may qualify this athlete in future evaluations."
            ),
        }

    low, high = NIL_RANGES[tier]

    # Scale within band based on position within tier
    tier_bounds = {
        "Elite":              (0.80, 1.00),
        "High-Level Starter": (0.70, 0.80),
        "Starter":            (0.60, 0.70),
        "Contributor":        (0.50, 0.60),
    }
    t_min, t_max = tier_bounds.get(tier, (0.50, 1.00))
    if t_max > t_min:
        position_in_tier = (pvm_score - t_min) / (t_max - t_min)
        position_in_tier = max(0.0, min(1.0, position_in_tier))
    else:
        position_in_tier = 0.5

    estimated = low + (high - low) * position_in_tier
    estimated = round(estimated / 1000) * 1000  # round to nearest $1K

    return {
        "eligible": True,
        "low": low,
        "high": high,
        "estimated": estimated,
        "display": f"${estimated:,.0f} estimated annual value",
        "range_display": f"${low:,.0f} – ${high:,.0f}",
        "description": _tier_description(tier),
    }


def _tier_description(tier: str) -> str:
    descriptions = {
        "Elite": (
            "Elite-tier athletes command top-of-market NIL deals. "
            "Expect significant brand partnerships, national exposure, and "
            "multi-platform endorsement opportunities."
        ),
        "High-Level Starter": (
            "High-level starters are attractive NIL prospects with strong production "
            "metrics. Regional partnerships and mid-market brand deals are well within reach."
        ),
        "Starter": (
            "Starter-tier athletes have established production profiles suitable for "
            "local endorsements, camp appearances, and emerging brand partnerships."
        ),
        "Contributor": (
            "Contributor-tier athletes represent early-stage NIL opportunities. "
            "Local business partnerships, social media deals, and niche endorsements "
            "are the primary avenues at this tier."
        ),
    }
    return descriptions.get(tier, "")
