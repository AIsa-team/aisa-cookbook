# Automated Investment Memos

Transform hours of manual equity research into seconds with this automated financial analyst agent. It leverages **AIsa**'s financial datasets and LLM routing to fetch live metrics, press releases, and news, and synthesizes a comprehensive investment memo.

## Features
- **Live Data**: Uses AIsa Financial APIs to pull real-time snapshot metrics, earnings press releases, and recent news.
- **Deep Synthesis**: Employs `gpt-4o` (via AIsa) to calculate a valuation verdict, bull case, bear case, and a definitive recommendation.
- **Export Ready**: Generates an exhaustive markdown memo ready for review.

## Setup
1. Clone the repository and navigate to this folder.
2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your AIsa API key.

## Usage
Run the script and provide a stock ticker (e.g., AAPL).
```bash
python analyst.py
```