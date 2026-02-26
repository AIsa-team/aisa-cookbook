import os
import requests
from openai import OpenAI
from dotenv import load_dotenv
from typing import Optional, Dict, Any, List

load_dotenv()

# --- Configuration ---
API_KEY = os.getenv("AISA_API_KEY")
LLM_BASE_URL = "https://api.aisa.one/v1"
DATA_BASE_URL = "https://api.aisa.one/apis/v1/financial"

if not API_KEY:
    raise ValueError("❌ Please set AISA_API_KEY in your environment or .env file")

client = OpenAI(api_key=API_KEY, base_url=LLM_BASE_URL)

def get_data(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """Helper to fetch data from AISA financial endpoints."""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        resp = requests.get(f"{DATA_BASE_URL}{endpoint}", headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"⚠️ API Error on {endpoint}: {e}")
        return None

def analyze_stock(ticker: str) -> None:
    """Fetches financial data and generates an investment memo."""
    print(f"\n🕵️‍♂️ Analyzing {ticker}...\n" + "-"*30)

    # 1. Fetch Financial Metrics (Snapshot)
    metrics = get_data("/financial-metrics/snapshot", params={"ticker": ticker})
    
    # 2. Fetch Latest Press Release
    pr_resp = get_data("/earnings/press-releases", params={"ticker": ticker, "limit": 1})
    pr_list = pr_resp.get("press_releases", []) if isinstance(pr_resp, dict) else (pr_resp or [])
    pr_text = pr_list[0].get('content', '')[:1500] if pr_list else "No press release available."

    # 3. Fetch News
    news_resp = get_data("/news", params={"ticker": ticker, "limit": 5})
    news = news_resp.get("news", []) if isinstance(news_resp, dict) else (news_resp or [])

    # 4. Generate Memo
    print("🧠 Synthesizing Investment Memo...")
    
    market_cap = metrics.get('market_cap', 'N/A') if metrics else 'N/A'
    pe_ratio = metrics.get('pe_ratio', 'N/A') if metrics else 'N/A'
    
    prompt = f"""
Act as a senior Wall Street Analyst. Write a comprehensive Investment Memo for {ticker}.
    
### DATA
- Market Cap: {market_cap}
- P/E Ratio: {pe_ratio}
- Latest PR Snippet: "{pr_text}..."
- Recent Headlines: {str(news)[:500]}...

### OUTPUT FORMAT
# Investment Memo: {ticker}

## Valuation Verdict
(Overvalued, Undervalued, or Fairly Valued based on the metrics)

## Bull Case
(3 bullet points based on news/earnings)

## Bear Case
(3 bullet points based on news/earnings/general risks)

## Final Recommendation
(**BUY**, **SELL**, or **HOLD**) with a 2-sentence rationale.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    
    memo = response.choices[0].message.content
    print("\n" + memo)
    
    # --- Save to file ---
    filename = f"{ticker.lower()}_memo.md"
    with open(filename, "w") as f:
        f.write(memo)
    print(f"\n💾 Saved memo to {filename}")

if __name__ == "__main__":
    ticker = input("📈 Enter Stock Ticker (e.g., NVDA): ").upper().strip()
    if ticker:
        analyze_stock(ticker)