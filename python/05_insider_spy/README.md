# CEO/CFO Trade Monitor (Insider Spy)

Don't guess what the executives are doing—know it. This script monitors SEC filings for a specific stock ticker to fetch recent insider trades (buys/sells) by company executives. It then uses AIsa's LLM gateway (`gpt-4o`) to analyze the sentiment of these trades.

## Features
- **Live Insider Data**: Pulls the latest insider trades using AIsa's `/insider-trades` financial endpoint.
- **Sentiment Analysis**: Translates raw SEC filings into a formatted "Insider Spy Report", emphasizing structural buying or dumping by key executives (CEO/CFO).
- **Export Ready**: Generates a fast, readable markdown report.

## Setup
1. Clone the repository and navigate to this folder.
2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your AIsa API key.

## Usage
Run the script and provide a stock ticker (e.g., PLTR).
```bash
python spy.py
```
