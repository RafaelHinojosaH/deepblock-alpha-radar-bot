import os
from dotenv import load_dotenv

from src.utils.logger import get_logger
from src.utils.paths import CONFIG_DIR
import yaml
from pathlib import Path

logger = get_logger("alpha-radar-main")

def load_yaml(path: Path):
    if not path.exists():
        logger.warning(f"Config file not found: {path}")
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def bootstrap():
    # Cargar .env
    load_dotenv()
    env = os.getenv("ENV", "local")
    logger.info(f"Starting Alpha Radar Bot (env={env})")

    sources_cfg = load_yaml(CONFIG_DIR / "sources.yaml")
    filters_cfg = load_yaml(CONFIG_DIR / "filters.yaml")
    scoring_cfg = load_yaml(CONFIG_DIR / "scoring.yaml")

    logger.info(f"Loaded sources: {list(sources_cfg.keys()) if sources_cfg else 'none'}")
    logger.info(f"Filters loaded: {bool(filters_cfg)} | Scoring loaded: {bool(scoring_cfg)}")

    return {
        "sources": sources_cfg,
        "filters": filters_cfg,
        "scoring": scoring_cfg,
    }

def main():
    config = bootstrap()
    logger.info("Alpha Radar Bot is ready to scan (demo mode).")
    # Aquí luego llamamos a scanner.alpha_scanner.run(config)

if __name__ == "__main__":
    main()

