# AIsa Cookbook

Welcome to the **AIsa Cookbook**! This repository contains a collection of standalone, ready-to-run recipes for building AI agents and automated workflows using the [AIsa.one](https://aisa.one) ecosystem.

Each recipe is designed as a completely independent project. You can copy any folder out of this repository, install its specific requirements, configure your API keys, and run it immediately!

## 📚 Available Recipes (Python)

Below is a summary of the fully-functional agents and scripts currently available in the `python/` directory:

| Recipe | Description | AIsa Features Used |
| :--- | :--- | :--- |
| [**01. Viral X/Twitter Thread Bot**](./python/01_social_automator) | Automates social media growth by finding the latest engaging facts on a topic and crafting a viral 5-part Twitter thread. | LLM Gateway (`gpt-4o`), Tavily Web Search |
| [**02. Automated Investment Memos**](./python/02_financial_analyst) | Transforms hours of manual equity research into an automated investment memo with live data synthesis. | Live Financial Metrics, Earnings Press Releases, News, LLM Gateway |
| [**03. Academic Fact Checker**](./python/03_deep_researcher) | Rigorous researcher that searches peer-reviewed studies to mathematically fact-check any claim and generate markdown reports. | Smart Search API, LLM Gateway (`gpt-4o`) |
| [**04. Trend-to-Video Creator**](./python/04_video_generator) | Fetches top real-time trends from X, crafts cinematic prompts, and generates AI video automatically. | Twitter API, AIGC Video Synthesis, LLM Gateway |
| [**05. CEO/CFO Trade Monitor**](./python/05_insider_spy) | Monitors SEC filings for specific stock tickers to fetch insider trades, then analyzes structural buying or dumping by executives. | Insider Trades API, LLM Gateway (`gpt-4o`) |
| [**06. Crypto Sentiment Trader**](./python/06_crypto_whale) | Fetches live crypto prices and breaking news, then synthesizes fear & greed sentiment to make Buy/Sell/Hold decisions. | Crypto Prices Snapshot, News API, LLM Gateway |

## 🚀 Quick Start

To run any of the recipes in this cookbook:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AIsa-team/aisa-cookbook.git
   cd aisa-cookbook
   ```

2. **Navigate to the setup folder:**
   ```bash
   cd python/01_social_automator
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your API keys:**
   Get your API key from [AIsa.one](https://marketplace.aisa.one/?aff=GzQxs) and add it to your environment.
   ```bash
   cp .env.example .env
   # Edit .env and insert: AISA_API_KEY="sk-..."
   ```

5. **Run the agent:**
   Consult the `README.md` inside the specific recipe's folder for exact run commands (e.g., `python bot.py` or `python analyst.py`).

## 🔗 References

- **Official Documentation**: [docs.aisa.one](https://docs.aisa.one)
- **Main Website**: [AIsa.one](https://aisa.one)
- **Get API Key**: [Marketplace](https://marketplace.aisa.one/?aff=GzQxs)

## 🤝 Contributing

Contributions are always welcome! If you have a powerful use case or a minimal agent recipe built on top of AIsa, please open a PR.