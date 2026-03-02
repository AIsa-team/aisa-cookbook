# Crypto Sentiment Trader (Whale)

Crypto markets move at the speed of light, driven largely by sentiment and breaking news. This automated trading agent fetches the live price of a cryptocurrency, scrapes the latest news about the coin, and uses AIsa's LLM gateway (`gpt-4o`) to make a calculated sentiment-based trading decision.

## Features
- **Real-Time Crypto Prices**: Utilizes the AIsa `/crypto/prices/snapshot` endpoint to fetch the live price of any ticker (e.g., BTC, ETH).
- **Breaking News**: Leverages AIsa's `/news` API to grab the latest 5 headlines about the specific coin.
- **Whale Analysis**: Prompts `gpt-4o` as an elite Whale Trader to synthesize the data, gauge Fear & Greed, and output a concise action (Buy/Sell/Hold).

## Setup
1. Clone the repository and navigate to this folder.
2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your AIsa API key.

## Usage
Run the script and provide a crypto ticker (e.g., SOL).
```bash
python trader.py
```

## Output

<img width="890" height="473" alt="aisa-cookbook-crypto-whale" src="https://github.com/user-attachments/assets/4c7b1c90-5c78-4f89-9702-1a6c887c8d03" />
