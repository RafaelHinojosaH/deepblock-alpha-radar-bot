import os
from typing import Dict, List, Any, Optional
from src.utils.logger import get_logger
from src.utils.fetch import get

logger = get_logger(__name__)

DEXSCREENER_URL = "https://api.dexscreener.com/latest/dex/search"


def fetch_pairs(query: str) -> Optional[List[Dict[str, Any]]]:
    """
    Llama a Dexscreener y devuelve pares encontrados según el query.
    Query puede ser:
        - símbolo
        - contrato
        - nombre del token
    """
    url = f"{DEXSCREENER_URL}?q={query}"

    logger.info(f"Fetching Dexscreener data for query='{query}'")

    data = get(url)

    if not data or "pairs" not in data:
        logger.warning("No pairs found or Dexscreener returned invalid data.")
        return None

    return data["pairs"]


def normalize_pair(pair: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normaliza datos clave del par.
    """
    return {
        "token_symbol": pair.get("baseToken", {}).get("symbol"),
        "token_name": pair.get("baseToken", {}).get("name"),
        "chain_id": pair.get("chainId"),
        "pair_url": pair.get("url"),
        "price_usd": pair.get("priceUsd"),
        "volume_24h": pair.get("volume", {}).get("h24"),
        "liquidity_usd": pair.get("liquidity", {}).get("usd"),
        "fdv_usd": pair.get("fdv"),
        "created_at": pair.get("pairCreatedAt"),
    }


def apply_filters(pair: Dict[str, Any], filters: Dict[str, Any]) -> bool:
    """
    Aplica filtros desde config/filters.yaml
    """
    mc_min = filters["marketcap"]["min_usd"]
    mc_max = filters["marketcap"]["max_usd"]
    liq_min = filters["liquidity"]["min_usd"]
    vol_min = filters["volume_24h"]["min_usd"]
    chains_ok = filters["chains_allowlist"]

    # Marketcap / FDV
    mc = pair.get("fdv_usd") or 0
    if not (mc_min <= mc <= mc_max):
        return False

    # Liquidez
    liq = pair.get("liquidity_usd") or 0
    if liq < liq_min:
        return False

    # Volumen
    vol = pair.get("volume_24h") or 0
    if vol < vol_min:
        return False

    # Chain
    chain = pair.get("chain_id")
    if chain not in chains_ok:
        return False

    return True


def scan(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Escaneo real:
    - lee palabras clave definidas por el usuario
    - consulta Dexscreener
    - normaliza datos
    - filtra resultados
    - regresa lista de oportunidades
    """
    filters = config["filters"]
    sources = config["sources"]

    queries = [
        "ai",
        "agent",
        "meme",
        "sol",
        "base",
        "layer2",
        "new",
        "proto",
        "zk",
    ]

    logger.info("🚀 Running REAL alpha scan...")

    opportunities = []

    for q in queries:
        pairs = fetch_pairs(q)
        if not pairs:
            continue

        for p in pairs:
            normalized = normalize_pair(p)

            if apply_filters(normalized, filters):
                opportunities.append(normalized)

    logger.info(f"Found {len(opportunities)} alpha candidates.")
    return opportunities

