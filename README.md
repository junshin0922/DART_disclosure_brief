# Disclosure Brief

> Real-time AI translation of Korean corporate disclosures for global investors.

Korean listed companies file ~200 disclosures per day on [DART](https://dart.fss.or.kr/). For global investors covering Korea, there is a consistent 30-minute to 2-hour window between filing release and English-language coverage appearing on Bloomberg or Reuters.

Disclosure Brief closes that gap.

## How It Works

```
DART Open API → Parser → Claude Haiku → Telegram Channel
```

1. Monitors DART filings every 5 minutes for KOSPI top 20 companies
2. Parses the raw HTML disclosure document
3. Generates a structured English summary via Claude Haiku:
   - 3–5 bullet points (key figures, dates, counterparties)
   - 1-sentence market impact commentary
4. Publishes to a Telegram channel with the original DART link

## Sample Output

```
🏢 SK Hynix
📄 연결재무제표기준영업(잠정)실적(공정공시)
📅 2026-04-23

Summary
• Q1 2026 revenue: KRW 52,576.3B, up 60.2% QoQ and 198.1% YoY
• Q1 2026 operating profit: KRW 37,610.3B, up 96.2% QoQ and 405.5% YoY
• Q1 2026 net income: KRW 40,330.2B, up 165.0% QoQ and 397.5% YoY
• All figures preliminary (잠정), pending external audit under K-IFRS

SK Hynix reported exceptionally strong Q1 2026 results with triple-digit
YoY growth across all profitability metrics, though figures remain
preliminary pending audit finalization.

🔗 View on DART
#Korea #Disclosure #00164779
```

## Coverage

KOSPI top 20 by market cap — Samsung Electronics, SK Hynix, LG Energy Solution, Hyundai Motor, NAVER, Kakao, POSCO Holdings, Kia, Samsung Biologics, KB Financial, Shinhan Financial, Hana Financial, Celltrion, SK Telecom, LG Chem, Samsung SDI, KT, Hyundai Mobis, KEPCO, LG Electronics.

## Stack

| Component         | Technology              |
| ----------------- | ----------------------- |
| Language          | Python 3.12             |
| AI Summarization  | Anthropic Claude Haiku  |
| Data Source       | DART Open API           |
| HTML Parsing      | BeautifulSoup4          |
| Deduplication     | SQLite                  |
| Distribution      | Telegram Bot API        |
| Hosting           | Fly.io (Tokyo)          |

## Setup

**1. Clone and install dependencies**

```bash
git clone https://github.com/junshin0922/DART_disclosure_brief.git
cd DART_disclosure_brief
pip install -r requirements.txt
```

**2. Configure environment variables**

```bash
cp .env.example .env
```

Edit `.env`:

```
DART_API_KEY=your_dart_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHANNEL_ID=@your_channel
```

DART API key: [opendart.fss.or.kr](https://opendart.fss.or.kr)

**3. Run**

```bash
python main.py
```

## Cost

- Claude Haiku: ~$0.005 per filing → ~$30/month at full scale (200 filings/day)
- Fly.io: free tier (shared-cpu-1x, 256MB)
- DART Open API: free (commercial use permitted with attribution)

## Legal

DART Open API permits commercial use with attribution. Only AI-generated summaries are distributed — original filings are never redistributed.

---

Built by [Jun Shin](https://github.com/junshin0922) · NYU Data Science '28
