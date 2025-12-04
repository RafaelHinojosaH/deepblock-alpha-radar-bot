import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from dotenv import load_dotenv
from src.integrations.telegram import send_message

def main():
    load_dotenv()
    ok = send_message("🚀 Test desde *Alpha Radar Bot* hacia el canal público.")
    if ok:
        print("✅ Mensaje enviado correctamente.")
    else:
        print("❌ Error al enviar mensaje.")

if __name__ == "__main__":
    main()

