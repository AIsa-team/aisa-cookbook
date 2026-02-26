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


def search_academic(query, max_results=5):
    """Search Google Scholar and Web using AISA Smart Search."""
    resp = requests.get(
        f"{API_BASE_URL}/search/smart",
        headers=HEADERS,
        params={
            "q": query,
            "max_results": max_results,
        },
    )
    if resp.status_code != 200:
        print(f"⚠️ API Error: {resp.text}")
    resp.raise_for_status()
    return resp.json()


def research(topic):
    print(f"\n🔬 Academic Deep Researcher & Fact Checker")
    print(f"📌 Claim/Topic: {topic}")
    print("-" * 50)

    # --- Step 1: Generate concise academic search queries ---
    print(f"\n🧠 Generating academic keywords for: {topic}...")
    keyword_prompt = f"Extract exactly 3 concise academic search queries (max 5 words each) to fact-check this claim: '{topic}'. Do not use quotes, punctuation, or special characters. Return ONLY a comma-separated list of the 3 queries."
    try:
        kw_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": keyword_prompt}],
        )
        queries_text = kw_response.choices[0].message.content.replace('"', '').replace("'", "")
        angles = [q.strip() for q in queries_text.split(",") if q.strip()][:3]
    except Exception as e:
        print(f"⚠️ Failed to generate keywords, using fallback: {e}")
        safe_topic = ''.join(e for e in topic if e.isalnum() or e.isspace())[:40]
        angles = [safe_topic, f"{safe_topic} study", f"{safe_topic} review"]

    all_sources = []
    for i, query in enumerate(angles):
        print(f"🔍 Academic Search [{i+1}/{len(angles)}]: {query}")
        try:
            results = search_academic(query, max_results=3)
            # The Aisa /search/smart endpoint returns webPages.value
            sources = results.get("webPages", {}).get("value", [])
            all_sources.extend(sources)
            print(f"   ✅ Found {len(sources)} sources")
        except Exception as e:
            print(f"   ⚠️ Search failed: {e}")

    # --- Step 2: Prepare context ---
    context = ""
    seen_urls = set()
    for s in all_sources:
        url = s.get("url", s.get("link", ""))
        if url not in seen_urls and url:
            seen_urls.add(url)
            context += f"### {s.get('title', 'Untitled')}\n"
            context += f"Source/Link: {url}\n"
            snippet = s.get('snippet', s.get('content', ''))
            context += f"Content: {snippet}\n\n"

    # --- Step 3: Synthesize with LLM ---
    print(f"\n🧠 Synthesizing {len(seen_urls)} unique academic/web sources...")

    prompt = f"""You are a rigorous Academic Fact Checker. Produce a comprehensive research brief evaluating the following topic or claim: "{topic}"

### SOURCE MATERIAL
{context}

### OUTPUT FORMAT
# Academic Fact Check: {topic}

## Executive Summary
(3-4 sentence overview of the academic consensus regarding the claim)

## Verdict
(True, False, Mixed, or Unverifiable based on the evidence)

## Key Evidence & Findings
(Bullet points of the most important discoveries, strictly referencing the source material)

## Nuance & Methodological Limitations
(What's uncertain or contested in the literature?)

## References
(Numbered list of all sources used, with URLs)

Be highly specific. Distinguish peer-reviewed consensus from speculation."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )

    report = response.choices[0].message.content
    print("\n" + "=" * 50)
    print(report)

    # --- Save to file ---
    filename = topic.lower().replace(" ", "_").replace("/", "_")[:30] + "_factcheck.md"
    with open(filename, "w") as f:
        f.write(report)
    print(f"\n💾 Saved to {filename}")


if __name__ == "__main__":
    topic = input("🔎 Enter a claim or topic to mathematically fact-check: ")
    if topic.strip():
        research(topic)