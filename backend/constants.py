# ─────────────────────────────────────────────
#  NIL Valuation Engine · Constants
# ─────────────────────────────────────────────

# Position identifiers
POSITIONS = ["QB", "RB", "WR"]

# ── Tier definitions ──────────────────────────
TIERS = {
    "Elite":               {"min": 0.80, "max": 1.01, "color": "#0d0d0d"},
    "High-Level Starter":  {"min": 0.70, "max": 0.80, "color": "#1d4ed8"},
    "Starter":             {"min": 0.60, "max": 0.70, "color": "#16a34a"},
    "Contributor":         {"min": 0.50, "max": 0.60, "color": "#d97706"},
    "Below NIL Threshold": {"min": 0.00, "max": 0.50, "color": "#dc2626"},
}

# ── Position accent colors ────────────────────
POSITION_COLORS = {
    "QB": "#0369a1",
    "RB": "#16a34a",
    "WR": "#c2410c",
}

# ── QB normalization ranges ───────────────────
QB_RANGES = {
    "passing_yards": {"min": 0,   "max": 5000},
    "passing_tds":   {"min": 0,   "max": 50},
    "completion_pct":{"min": 40,  "max": 80},
    "int_pct":       {"min": 0,   "max": 10},
}

QB_WEIGHTS = {
    "passing_yards":  0.35,
    "passing_tds":    0.35,
    "completion_pct": 0.20,
    "int_pct":        0.10,   # inverted
}

# ── RB normalization ranges ───────────────────
RB_RANGES = {
    "rushing_yards": {"min": 0,   "max": 2000},
    "rushing_tds":   {"min": 0,   "max": 25},
    "ypc":           {"min": 2.0, "max": 8.0},
}

RB_WEIGHTS = {
    "rushing_yards": 0.35,
    "rushing_tds":   0.30,
    "ypc":           0.35,
}

# ── WR normalization ranges ───────────────────
WR_RANGES = {
    "receptions":      {"min": 0,   "max": 120},
    "receiving_yards": {"min": 0,   "max": 1800},
    "receiving_tds":   {"min": 0,   "max": 20},
    "ypr":             {"min": 5.0, "max": 25.0},
}

WR_WEIGHTS = {
    "receptions":      0.30,
    "receiving_yards": 0.35,
    "receiving_tds":   0.25,
    "ypr":             0.10,
}

# ── NIL recommendation ranges ─────────────────
NIL_RANGES = {
    "Elite":               (500_000, 2_000_000),
    "High-Level Starter":  (150_000,   500_000),
    "Starter":             (50_000,    150_000),
    "Contributor":         (10_000,     50_000),
    "Below NIL Threshold": (0, 0),
}

# ── Research R² values ────────────────────────
RESEARCH_R2 = {
    "QB": 0.0031,
    "RB": 0.0032,
    "WR": 0.216,
}
