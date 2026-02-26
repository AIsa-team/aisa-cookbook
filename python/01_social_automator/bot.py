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

def search_web(query, max_results=5):
    """Search the web using Tavily Search via AISA."""
    resp = requests.post(
        f"{API_BASE_URL}/tavily/search",
        headers=HEADERS,
        json={
            "query": query,
            "search_depth": "advanced",
            "topic": "general",
            "max_results": max_results,
            "include_answer": True,
        },
    )
    resp.raise_for_status()
    return resp.json()

def generate_viral_thread(topic):
    print(f"\n🚀 Viral X/Twitter Thread Bot")
    print(f"📌 Topic: {topic}")
    print("-" * 50)

    # --- Step 1: Search for recent and relevant information ---
    print(f"🔍 Searching the web for: {topic}...")
    try:
        results = search_web(f"latest news {topic} interesting facts viral", max_results=5)
        sources = results.get("results", [])
        print(f"   ✅ Found {len(sources)} engaging facts/news")
    except Exception as e:
        print(f"   ⚠️ Search failed: {e}")
        sources = []

    # --- Step 2: Prepare context ---
    context = ""
    for s in sources:
        context += f"Fact: {s.get('title', 'Unknown')} - {s.get('content', '')}\n"

    # --- Step 3: Write the Viral Thread ---
    print("\n🧠 Writing the thread (this might take a few seconds)...")

    prompt = f"""You are a master X (formerly Twitter) ghostwriter. Write a highly engaging, viral 5-part thread about: "{topic}"

### SOURCE MATERIAL TO USE (IF ANY)
{context}

### INSTRUCTIONS
- Write exactly 5 tweets to form a continuous thread.
- Tweet 1 must be an incredible hook that makes people stop scrolling.
- Tweets 2-4 should deliver high-value insights, astonishing facts, or compelling narrative using the source material if relevant.
- Tweet 5 should wrap it up with a strong takeaway and a Call-To-Action (e.g., "Follow me for more...").
- Keep formatting clean. Use emojis appropriately but sparingly.
- Make the tone punchy, authoritative, and fast-paced.
- Do NOT use hashtags unless absolutely necessary.
- Format the output clearly separated by "---"

Ensure the thread is ready to copy-paste.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )

    thread_content = response.choices[0].message.content
    print("\n" + "=" * 50)
    print("✨ YOUR VIRAL THREAD IS READY ✨")
    print("=" * 50 + "\n")
    print(thread_content)

    # --- Save to file ---
    filename = topic.lower().replace(" ", "_").replace("/", "_")[:30] + "_thread.txt"
    with open(filename, "w") as f:
        f.write(thread_content)
    print(f"\n💾 Saved thread to {filename}")


if __name__ == "__main__":
    topic = input("🗣️ What topic should the viral thread be about? ")
    generate_viral_thread(topic)
