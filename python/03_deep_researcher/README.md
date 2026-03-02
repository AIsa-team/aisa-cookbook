# Academic Fact Checker / Deep Researcher

In an era of misinformation, standard web search isn't enough. The Academic Fact Checker agent leverages the **AIsa Smart Search API** to search across rigorous, peer-reviewed studies and academic journals to mathematically fact-check any claim.

## Features
- **Rigorous Sourcing**: Uses an LLM to generate targeted search queries, then fetches both academic and web results using AIsa's `/search/smart` endpoint.
- **Fact-Checking LLM**: Instructs `gpt-4o` (via AIsa LLMs) to synthesize evidence objectively, assigning a clear Verdict (True, False, Mixed) supported by references.
- **Markdown Reports**: Automatically saves a detailed `.md` report of the findings.

## Setup
1. Clone the repository and navigate to this folder.
2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your AIsa API key.

## Usage
Run the script and provide a claim or topic to fact check.
```bash
python bot.py
```

## Output

<img width="1014" height="1122" alt="aisa-cookbook-deep-research" src="https://github.com/user-attachments/assets/1c070674-d254-44c5-9ec6-8fba222b160d" />
