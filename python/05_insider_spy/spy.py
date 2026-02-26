import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
API_KEY = os.getenv("AISA_API_KEY")
LLM_BASE_URL = "https://api.aisa.one/v1"
API_BASE_URL = "https://api.aisa.one/apis/v1"

if not API_KEY:
    raise ValueError("❌ Please set AISA_API_KEY in your .env file")

client = OpenAI(api_key=API_KEY, base_url=LLM_BASE_URL)
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

def get_insider_trades(ticker, limit=20):
    """Fetch recent insider trades for a specific ticker."""
    print(f"🕵️ Fetching insider trades for {ticker}...")
    try:
        resp = requests.get(
            f"{API_BASE_URL}/financial/insider-trades",
            headers=HEADERS,
            params={"ticker": ticker, "limit": limit}
        )
        resp.raise_for_status()
        trades = resp.json()
        
        # Depending on API response structure, extract the list.
        if isinstance(trades, dict) and "insider_trades" in trades:
            return trades.get("insider_trades", [])
        elif isinstance(trades, list):
            return trades
        return []
        
    except Exception as e:
        print(f"⚠️ Failed to fetch insider trades: {e}")
        return []

def analyze_trades_with_llm(ticker, trades):
    """Use GPT-4o to analyze trades and detect sentiment."""
    if not trades:
        print("❌ No trades available to analyze.")
        return

    print("🧠 Synthesizing Insider Sentiment Report...")
    
    # Format trades into a readable string for the prompt
    trades_context = ""
    for i, t in enumerate(trades[:15]): # Limit to top 15 to save context
        date = t.get('filing_date', t.get('date', 'Unknown'))
        name = t.get('reporting_name', t.get('name', 'Unknown'))
        title = t.get('type_of_owner', t.get('title', 'Insider'))
        trade_type = t.get('transaction_type', 'Trade')
        shares = t.get('securities_transacted', t.get('shares', 0))
        price = t.get('price', 0)
        
        trades_context += f"- {date}: {name} ({title}) executed a {trade_type} of {shares} shares at ${price}\n"

    prompt = f"""Act as a forensic financial researcher monitoring insider sentiment.
Analyze the following recent insider transactions for {ticker}. 
Pay special attention to C-suite (CEO, CFO, CTO) trades compared to regular directors.

### RECENT TRADES
{trades_context}

### OUTPUT FORMAT
# 🕵️ Insider Spy Report: {ticker}

## Executive Summary
(2-3 sentences summarizing the recent insider activity)

## Major Movers
(List the most significant transactions, particularly highlighting CEO/CFO activity if present)

## Corporate Sentiment
(Are insiders Bullish, Bearish, or Neutral? Why?)

## Key Takeaway
(1 sentence conclusion on whether this activity should concern retail investors)
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    
    report = response.choices[0].message.content
    print("\n" + "=" * 50)
    print(report)
    print("=" * 50 + "\n")
    
    # Save to file
    filename = f"{ticker.lower()}_insider_report.md"
    with open(filename, "w") as f:
        f.write(report)
    print(f"💾 Saved report to {filename}")

if __name__ == "__main__":
    target_ticker = input("Enter a stock ticker to spy on insiders (e.g., TSLA, PLTR): ").upper().strip()
    if target_ticker:
        recent_trades = get_insider_trades(target_ticker)
        analyze_trades_with_llm(target_ticker, recent_trades)
