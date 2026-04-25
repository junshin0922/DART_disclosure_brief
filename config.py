from dotenv import load_dotenv
import os

load_dotenv()

DART_API_KEY = os.environ["DART_API_KEY"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHANNEL_ID = os.environ["TELEGRAM_CHANNEL_ID"]

# KOSPI top 20 corp codes (DART corpCode, not ticker)
WATCHLIST: dict[str, str] = {
    "00126380": "Samsung Electronics",
    "00164779": "SK Hynix",
    "00631518": "LG Energy Solution",
    "00164742": "Hyundai Motor",
    "00293886": "NAVER",
    "00918444": "Kakao",
    "00104426": "POSCO Holdings",
    "00164788": "Kia",
    "00107356": "Samsung Biologics",
    "00159021": "KB Financial",
    "00138321": "Shinhan Financial",
    "00111163": "Hana Financial",
    "00148649": "Celltrion",
    "00126186": "SK Telecom",
    "00119650": "LG Chem",
    "00107757": "Samsung SDI",
    "00126186": "KT",
    "00164786": "Hyundai Mobis",
    "00104408": "KEPCO",
    "00104480": "LG Electronics",
}

POLL_INTERVAL_SECONDS = 300  # 5 minutes
