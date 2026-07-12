# ─────────────────────────────────────────────
#  NIL Valuation Engine · PVM Models
# ─────────────────────────────────────────────

from backend.constants import QB_WEIGHTS, RB_WEIGHTS, WR_WEIGHTS
from backend.normalization import normalize_qb, normalize_rb, normalize_wr


def calculate_qb_pvm(passing_yards: float, passing_tds: float,
                      completion_pct: float, int_pct: float) -> tuple[float, dict]:
    norms = normalize_qb(passing_yards, passing_tds, completion_pct, int_pct)
    score = (
        norms["passing_yards"]  * QB_WEIGHTS["passing_yards"] +
        norms["passing_tds"]    * QB_WEIGHTS["passing_tds"] +
        norms["completion_pct"] * QB_WEIGHTS["completion_pct"] +
        norms["int_pct"]        * QB_WEIGHTS["int_pct"]
    )
    return round(score, 4), norms


def calculate_rb_pvm(rushing_yards: float, rushing_tds: float,
                      ypc: float) -> tuple[float, dict]:
    norms = normalize_rb(rushing_yards, rushing_tds, ypc)
    score = (
        norms["rushing_yards"] * RB_WEIGHTS["rushing_yards"] +
        norms["rushing_tds"]   * RB_WEIGHTS["rushing_tds"] +
        norms["ypc"]           * RB_WEIGHTS["ypc"]
    )
    return round(score, 4), norms


def calculate_wr_pvm(receptions: float, receiving_yards: float,
                      receiving_tds: float, ypr: float) -> tuple[float, dict]:
    norms = normalize_wr(receptions, receiving_yards, receiving_tds, ypr)
    score = (
        norms["receptions"]      * WR_WEIGHTS["receptions"] +
        norms["receiving_yards"] * WR_WEIGHTS["receiving_yards"] +
        norms["receiving_tds"]   * WR_WEIGHTS["receiving_tds"] +
        norms["ypr"]             * WR_WEIGHTS["ypr"]
    )
    return round(score, 4), norms
