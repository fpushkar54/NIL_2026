# ─────────────────────────────────────────────
#  NIL Valuation Engine · Tier Classification
# ─────────────────────────────────────────────

from backend.constants import TIERS


def classify_tier(pvm_score: float) -> str:
    """Return tier label for a given PVM score."""
    for tier_name, bounds in TIERS.items():
        if bounds["min"] <= pvm_score < bounds["max"]:
            return tier_name
    return "Below NIL Threshold"


def get_tier_color(tier_name: str) -> str:
    return TIERS.get(tier_name, {}).get("color", "#0d0d0d")


def get_tier_badge_style(tier_name: str) -> dict:
    colors = {
        "Elite":               {"bg": "#0d0d0d", "text": "#ffffff"},
        "High-Level Starter":  {"bg": "#dbeafe", "text": "#1d4ed8"},
        "Starter":             {"bg": "#dcfce7", "text": "#16a34a"},
        "Contributor":         {"bg": "#fef3c7", "text": "#d97706"},
        "Below NIL Threshold": {"bg": "#fee2e2", "text": "#dc2626"},
    }
    return colors.get(tier_name, {"bg": "#f3f4f6", "text": "#374151"})
