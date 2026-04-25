"""Test Telegram dispatch with the SK Hynix summary we already generated."""
from telegram.bot import dispatch

filing = {
    "rcept_no": "20260423800001",
    "corp_code": "00164779",
    "corp_name": "SK Hynix",
    "report_nm": "연결재무제표기준영업(잠정)실적(공정공시)",
    "rcept_dt": "20260423",
}

summary = {
    "bullets": [
        "Q1 2026 revenue: KRW 52,576.3B, up 60.2% QoQ and 198.1% YoY",
        "Q1 2026 operating profit: KRW 37,610.3B, up 96.2% QoQ and 405.5% YoY",
        "Q1 2026 net income attributable to parent: KRW 40,330.2B, up 165.0% QoQ and 397.5% YoY",
        "All figures preliminary (잠정), pending external audit under K-IFRS consolidated basis",
    ],
    "market_impact": (
        "SK Hynix reported exceptionally strong Q1 2026 results with triple-digit YoY growth "
        "across all profitability metrics, though figures remain preliminary pending audit finalization."
    ),
}

ok = dispatch(filing, summary)
print("Sent!" if ok else "Failed — check TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID in .env")
