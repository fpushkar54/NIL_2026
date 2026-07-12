# ─────────────────────────────────────────────
#  NIL Valuation Engine · Normalization
# ─────────────────────────────────────────────

from backend.constants import QB_RANGES, RB_RANGES, WR_RANGES


def _normalize(value: float, min_val: float, max_val: float, invert: bool = False) -> float:
    """Min-max normalization clamped to [0, 1]."""
    if max_val == min_val:
        return 0.0
    normalized = (value - min_val) / (max_val - min_val)
    normalized = max(0.0, min(1.0, normalized))
    return (1.0 - normalized) if invert else normalized


# ── QB ────────────────────────────────────────
def normalize_qb(passing_yards: float, passing_tds: float,
                  completion_pct: float, int_pct: float) -> dict:
    r = QB_RANGES
    return {
        "passing_yards":  _normalize(passing_yards,  r["passing_yards"]["min"],  r["passing_yards"]["max"]),
        "passing_tds":    _normalize(passing_tds,    r["passing_tds"]["min"],    r["passing_tds"]["max"]),
        "completion_pct": _normalize(completion_pct, r["completion_pct"]["min"], r["completion_pct"]["max"]),
        "int_pct":        _normalize(int_pct,        r["int_pct"]["min"],        r["int_pct"]["max"], invert=True),
    }


# ── RB ────────────────────────────────────────
def normalize_rb(rushing_yards: float, rushing_tds: float, ypc: float) -> dict:
    r = RB_RANGES
    return {
        "rushing_yards": _normalize(rushing_yards, r["rushing_yards"]["min"], r["rushing_yards"]["max"]),
        "rushing_tds":   _normalize(rushing_tds,   r["rushing_tds"]["min"],   r["rushing_tds"]["max"]),
        "ypc":           _normalize(ypc,            r["ypc"]["min"],           r["ypc"]["max"]),
    }


# ── WR ────────────────────────────────────────
def normalize_wr(receptions: float, receiving_yards: float,
                  receiving_tds: float, ypr: float) -> dict:
    r = WR_RANGES
    return {
        "receptions":      _normalize(receptions,      r["receptions"]["min"],      r["receptions"]["max"]),
        "receiving_yards": _normalize(receiving_yards, r["receiving_yards"]["min"], r["receiving_yards"]["max"]),
        "receiving_tds":   _normalize(receiving_tds,   r["receiving_tds"]["min"],   r["receiving_tds"]["max"]),
        "ypr":             _normalize(ypr,              r["ypr"]["min"],             r["ypr"]["max"]),
    }
