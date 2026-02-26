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

def get_crypto_price(ticker):
    """Fetch real-time snapshot for a cryptocurrency."""
    print(f"💰 Fetching current price for {ticker}...")
    try:
        resp = requests.get(
            f"{API_BASE_URL}/financial/crypto/prices/snapshot",
            headers=HEADERS,
            params={"ticker": ticker}
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"⚠️ Failed to fetch crypto price: {e}")
        return None

def get_crypto_news(ticker):
    """Fetch recent news for the cryptocurrency ticker."""
    print(f"📰 Fetching recent news for {ticker}...")
    try:
        resp = requests.get(
            f"{API_BASE_URL}/financial/news",
            headers=HEADERS,
            params={"ticker": ticker, "limit": 5}
        )
        resp.raise_for_status()
        # Parse based on expected JSON format
        news_data = resp.json()
        if isinstance(news_data, dict) and "news" in news_data:
            return news_data.get("news", [])
        return news_data if isinstance(news_data, list) else []
    except Exception as e:
        print(f"⚠️ Failed to fetch crypto news: {e}")
        return []

def execute_sentiment_trade(ticker, price_data, news_data):
    """Use GPT-4o to act as a whale trader and make a trading decision based on sentiment."""
    print("🧠 Analyzing Sentiment & Market Conditions...")
    
    # Format Price Data
    price_context = f"Current Price Data: {price_data}" if price_data else "Price data unavailable."
    
    # Format News Data
    news_context = ""
    for n in news_data[:5]:
        title = n.get('title', 'Headline')
        snippet = n.get('snippet', n.get('description', 'No details.'))
        news_context += f"- {title}: {snippet}\n"

    prompt = f"""You are an elite Crypto Whale Trader known for immaculate market timing.
Make a trading decision on {ticker} based on its current realtime price and recent news sentiment.

### MARKET DATA
{price_context}

### RECENT NEWS
{news_context}

### OUTPUT FORMAT
# 🐋 Crypto Whale Output: {ticker}

## The Thesis
(2-3 sentences analyzing the news sentiment and how it reflects on the current price)

## Fear & Greed Assessment
(Estimate the market sentiment purely based on the news provided)

## Actionable Trade
(**BUY**, **SELL**, **HOLD**, or **SHORT**) heavily justified in 1 sentence.
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
    filename = f"{ticker.lower()}_whale_trade.md"
    with open(filename, "w") as f:
        f.write(report)
    print(f"💾 Saved trade thesis to {filename}")

if __name__ == "__main__":
    target_ticker = input("Enter a Crypto Ticker (e.g., BTC, ETH, SOL): ").upper().strip()
    if target_ticker:
        price = get_crypto_price(target_ticker)
        news = get_crypto_news(target_ticker)
        execute_sentiment_trade(target_ticker, price, news)
