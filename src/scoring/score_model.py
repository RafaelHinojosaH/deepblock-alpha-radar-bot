from typing import Dict, Any

from src.utils.logger import get_logger
from .score_utils import safe_div

logger = get_logger(__name__)


def score_fdv(fdv: float) -> float:
    """
    Score del marketcap / FDV.
    Tokens entre 300k y 15M son la "zona alfa".
    """
    if fdv is None or fdv <= 0:
        return 0

    if fdv < 200_000:  # demasiado microcap = riesgo extremo
        return 0.1

    if 200_000 <= fdv <= 15_000_000:
        # Alta probabilidad de upside
        # Se normaliza entre 0.6 y 1.0
        return 0.6 + (fdv / 15_000_000) * 0.4

    # >15M ya tiene menor upside relativo
    return 0.3


def score_liquidity(liq: float) -> float:
    """
    Score basado en la liquidez en USD.
    """
    if liq is None:
        return 0

    if liq < 20_000:
        return 0.0
    if 20_000 <= liq < 50_000:
        return 0.4
    if 50_000 <= liq < 200_000:
        return 0.7
    if liq >= 200_000:
        return 1.0

    return 0.0


def score_volume(vol24h: float) -> float:
    """
    Score basado en volumen 24h.
    """
    if vol24h is None:
        return 0.0

    if vol24h < 30_000:
        return 0.2
    if 30_000 <= vol24h < 100_000:
        return 0.5
    if 100_000 <= vol24h < 500_000:
        return 0.75
    if vol24h >= 500_000:
        return 1.0

    return 0.0


def score_holders_distribution(holder_ratio: float) -> float:
    """
    Ratio que indica qué % del supply está en top wallets.
    Mientras más distribuido, mejor.
    
    Ejemplo:
        0.05 → 5% supply en top 10 wallets → excelente
        0.5  → 50% supply en top 10 wallets → riesgoso
    """
    if holder_ratio is None:
        return 0.5  # neutral

    if holder_ratio < 0.10:
        return 1.0  # excelente distribución
    if 0.10 <= holder_ratio < 0.30:
        return 0.7
    if 0.30 <= holder_ratio < 0.50:
        return 0.4
    if holder_ratio >= 0.50:
        return 0.1  # super riesgoso

    return 0.5


def score_risk(risk_flags: Dict[str, bool]) -> float:
    """
    Riesgos detectados:
    - honeypot
    - unlocked liquidity
    - recent deploy (<24h)
    - dev wallet dominance
    """
    score = 1.0

    if risk_flags.get("honeypot"):
        score -= 0.9
    if risk_flags.get("unlocked_liquidity"):
        score -= 0.5
    if risk_flags.get("recent_deploy"):
        score -= 0.3
    if risk_flags.get("dev_wallet_high"):
        score -= 0.4

    return max(score, 0.0)


def compute_total_score(token: Dict[str, Any], weights: Dict[str, float]) -> float:
    """
    Calcula el score total.
    token = normalized token dictionary
    weights = ponderaciones desde config/scoring.yaml
    """
    fdv = token.get("fdv_usd")
    liq = token.get("liquidity_usd")
    vol = token.get("volume_24h")

    # Opcional: estos vienen luego de integrar onchain tracking
    holder_ratio = token.get("holder_ratio", 0.3)
    risk_flags = token.get("risk_flags", {})

    fdv_s = score_fdv(fdv)
    liq_s = score_liquidity(liq)
    vol_s = score_volume(vol)
    holder_s = score_holders_distribution(holder_ratio)
    risk_s = score_risk(risk_flags)

    total = (
        fdv_s * weights["marketcap_score"]
        + liq_s * weights["liquidity_score"]
        + vol_s * weights["volume_score"]
        + holder_s * weights["holder_distribution_score"]
        + risk_s * weights["risk_score"]
    )

    # Lo normalizamos a escala 0–100
    return round(total * 100, 2)


def add_score_to_tokens(tokens: list, scoring_cfg: Dict[str, Any]) -> list:
    """
    Toma una lista de tokens (dicts) y añade key 'score' calculado.
    """
    weights = scoring_cfg["weights"]
    results = []

    for token in tokens:
        score = compute_total_score(token, weights)
        token["score"] = score
        results.append(token)

    return results

