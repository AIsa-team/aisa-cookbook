# Trend-to-Video Creator

Don't just post about a trend—create a viral, high-quality video instantly! This bot fetches the top real-time trends from X using the AIsa Twitter API, crafts a highly visual, cinematic prompt via the AIsa LLM Gateway (`gpt-4o`), and finally submits it to AIsa's AIGC Video Synthesis engine.

## Features
- **Real-Time Targeting**: Pings the `/twitter/trends` API endpoint for the hottest topics.
- **Cinematic Prompts**: Employs an LLM to translate a simple text trend into a detailed visual generation prompt. 
- **Asynchronous Rendering**: Creates an AI video synthesis task and continuously polls for completion automatically.

## Setup
1. Clone the repository and navigate to this folder.
2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your AIsa API key.

## Usage
Simply run the script. It will automatically detect the top trend and start rendering!
```bash
python generator.py
```

## Output

<img width="892" height="419" alt="aisa-cookbook-video-generator" src="https://github.com/user-attachments/assets/1e333942-fb0a-47b3-a019-2d0fbb0acf18" />
