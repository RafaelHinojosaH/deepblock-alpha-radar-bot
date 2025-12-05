import sys
from pathlib import Path
import json
from datetime import datetime
import shutil

# Permitir correr el script desde la raíz del proyecto:
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.main import bootstrap
from src.utils.logger import get_logger
from src.scanner.alpha_scanner import scan
from src.scoring.score_model import add_score_to_tokens
from src.integrations.telegram import send_message
from src.utils.paths import PROCESSED_DIR, DASHBOARD_DATA_DIR  # 👈 asegúrate de definir esto

logger = get_logger("alpha-radar-scan")


def _save_json_for_dashboard(top_sorted):
    """
    Guarda el resultado del scan en:
      - storage/processed/alpha-radar_YYYYMMDD_HHMMSS.json      (histórico interno)
      - ../deepblockai-dashboard/data/alpha-radar-latest.json   (consumido por el dashboard)
    """
    try:
        # Asegurar directorios
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        DASHBOARD_DATA_DIR.mkdir(parents=True, exist_ok=True)

        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        # Archivo histórico interno del bot
        internal_path = PROCESSED_DIR / f"alpha-radar_{ts}.json"

        # Archivo que va a leer el dashboard
        dashboard_path = DASHBOARD_DATA_DIR / "alpha-radar-latest.json"

        # Guardar histórico
        with internal_path.open("w", encoding="utf-8") as f:
            json.dump(top_sorted, f, ensure_ascii=False, indent=2)

        # Copiar/actualizar el archivo del dashboard
        shutil.copy(internal_path, dashboard_path)

        logger.info(f"💾 JSON guardado en {internal_path}")
        logger.info(f"📊 JSON actualizado para dashboard en {dashboard_path}")
    except Exception as e:
        logger.error(f"❌ Error guardando JSON para dashboard: {e}")


def run_scan():
    logger.info("🔥 Iniciando Alpha Radar Scan REAL con Scoring Profesional...")

    # 1. Cargar configuraciones
    config = bootstrap()

    # 2. Ejecutar escáner real
    tokens = scan(config)

    if not tokens:
        logger.warning("⚠️ No se encontraron oportunidades en este escaneo.")
        return

    logger.info(f"🎯 Total tokens detectados antes del scoring: {len(tokens)}")

    # 3. Añadir scores
    scored_tokens = add_score_to_tokens(tokens, config["scoring"])

    # 4. Ordenarlos por mayor score
    top_sorted = sorted(scored_tokens, key=lambda x: x["score"], reverse=True)

    logger.info("📈 TOP 5 TOKENS POR SCORE:")

    for idx, t in enumerate(top_sorted[:5], start=1):
        logger.info(
            f"[{idx}] {t['token_symbol']} | Chain: {t['chain_id']} | "
            f"Score: {t['score']} | MC: {t['fdv_usd']} | "
            f"Liq: {t['liquidity_usd']} | Vol24h: {t['volume_24h']}"
        )

    # 💾 Guardar JSON para histórico + dashboard
    _save_json_for_dashboard(top_sorted)

    logger.info("✅ Scan con scoring finalizado.")

    # 📨 Construir el mensaje para Telegram (AQUÍ SÍ VE top_sorted)
    msg_lines = ["🔥 *TOP 5 ALPHA DETECTADOS HOY*\n"]

    for idx, t in enumerate(top_sorted[:5], start=1):
        msg_lines.append(
            f"*{idx}) {t['token_symbol']}*  `{t['chain_id']}`\n"
            f"*Score:* {t['score']} / 100\n"
            f"*MC:* ${t['fdv_usd']:,}\n"
            f"*Liquidez:* ${t['liquidity_usd']:,}\n"
            f"*Vol 24h:* ${t['volume_24h']:,}\n"
            f"[Ver en Dexscreener]({t.get('pair_url', 'N/A')})\n"
        )

    full_msg = "\n".join(msg_lines)

    send_ok = send_message(full_msg)
    if send_ok:
        logger.info("📩 TOP 5 enviado a Telegram.")
    else:
        logger.error("❌ No se pudo enviar el TOP 5 a Telegram.")


if __name__ == "__main__":
    run_scan()

