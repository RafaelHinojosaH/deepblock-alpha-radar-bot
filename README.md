# 🛰️ **Alpha Radar Bot**
### _By **DeepBlockAI** — Inteligencia Autónoma para Crypto_

> Un escáner avanzado que detecta **protocolos sin token**, oportunidades tempranas, narrativas emergentes y señales de TVL en múltiples redes.  
> Diseñado para traders, airdrop hunters y creadores de comunidades Web3.

---

## 🚀 **Descripción**

**Alpha Radar Bot** es un proyecto independiente del ecosistema **DeepBlockAI**.  
Escanea diversas fuentes on-chain y off-chain para identificar:

- Protocolos sin token  
- Proyectos con TVL en crecimiento  
- Narrativas emergentes (AI, RWA, DePIN, etc.)  
- Liquidez temprana y actividades sospechosas  
- Métricas de riesgo simples  
- Oportunidades potenciales para testnets y puntos  

Envía los resultados directamente a **Telegram**, **Discord** o **Twitter/X**.

> La misión del bot es detectar oportunidades antes de que el mercado general las note.

---

## ✨ **Características principales**

- 🔍 *Scanner inteligente* – TVL, liquidez inicial, narrativa, categoría y señales de riesgo.  
- 📡 *Fuentes múltiples* – DefiLlama, Debank, DEX listings, narrativas Web3.  
- 🤖 *Modo autónomo* – Ejecuta el análisis cada X horas (configurable).  
- 📈 *Sistema de scoring* – Evalúa riesgo, hype y crecimiento.  
- 🧠 *Módulo de IA* – Genera resúmenes inteligentes.  
- 📤 *Integraciones listas* – Telegram, Discord, Twitter.  
- 💾 *Persistencia opcional* – Guarda reportes para análisis posterior.  

---

## 🧩 **Estructura del proyecto**

```
alpha-radar-bot/
├── config/
│   ├── alerts.yaml
│   ├── filters.yaml
│   ├── schedule.yaml
│   ├── scoring.yaml
│   └── sources.yaml
├── src/
│   ├── ai/
│   ├── cli/
│   ├── integrations/
│   ├── scanner/
│   ├── scoring/
│   └── utils/
├── storage/
│   ├── raw/
│   ├── processed/
│   └── reports/
└── tests/
```

---

## 🛠️ **Requisitos**

- Python 3.10+  
- pip / venv  
- Token de BotFather  
- Cuenta de Telegram  

---

## ⚙️ **Instalación**

```bash
git clone https://github.com/RafaelHinojosaH/alpha-radar-bot
cd alpha-radar-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🔧 **Configuración**

Copia el archivo de ejemplo:

```bash
cp config/example.env .env
```

Edita tus credenciales:

```env
TELEGRAM_BOT_TOKEN=xxxx
TELEGRAM_DEFAULT_CHAT_ID=@tugrupo
MIN_TVL_USD=2000000
```

---

## ▶️ **Ejecutar**

### Modo prueba:

```bash
python src/cli/run_scan.py
```

### Modo autónomo:

```bash
python src/cli/run_daily.py
```

---

## 📬 **Integraciones**

- **Telegram**  
- **Discord**  
- **Twitter/X**

---

## 🧪 **Tests**

```bash
pytest
```

---

## 🛣️ **Roadmap**

- [ ] Integración directa con DefiLlama  
- [ ] Soporte para puntos y campañas web3  
- [ ] Dashboard web  
- [ ] Historial de oportunidades  
- [ ] Alertas avanzadas  
- [ ] Exportaciones CSV  
- [ ] Modo newsletter  

---

## 🧠 **DeepBlockAI Ecosystem**

Proyectos hermanos:

- Alpha Radar Bot  
- Whale Watcher  
- Airdrop Finder  
- DeFi Yield Scanner  
- New Token Explorer  
- Narratives AI Detector  
- Crypto Academy Mini  
- Market Pulse Daily  
- Crypto Tools Publisher  
- Crypto Backtesting Starter  

---

## 📄 **Licencia**

MIT License — Libre para uso personal y comercial.

---

## ⭐ **Apoya el proyecto**

Si este bot te ayuda, considera dejar una estrella ⭐ en GitHub.
