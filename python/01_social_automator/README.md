# Viral X/Twitter Thread Bot

Automate your social media growth with the Viral Thread Bot! This script utilizes the power of **AIsa's LLM routing** and **Tavily Web Search** to find the latest engaging facts on any topic and craft a viral 5-part Twitter thread ready to be posted.

## Features
- **Real-Time Context**: Uses AIsa's Tavily Search integration to pull the latest news and facts.
- **Viral Copywriting**: Uses `gpt-4o` (via AIsa) with a specialized prompt to write engaging, high-retention threads.
- **Ready-to-Post**: Outputs your thread clearly separated and automatically saves it to a text file.

## Setup
1. Clone the repository and navigate to this folder.
2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your AIsa API key.
   ```bash
   cp .env.example .env
   ```

## Usage
Run the bot, enter your topic, and watch it generate facts and the thread!
```bash
python bot.py
```
