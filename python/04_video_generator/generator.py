import os
import requests
import time
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

def get_twitter_trends(woeid=1):
    """Fetch X/Twitter trends. woeid=1 is Worldwide."""
    print("🌍 Fetching current Worldwide Trends from X...")
    try:
        resp = requests.get(
            f"{API_BASE_URL}/twitter/trends",
            headers=HEADERS,
            params={"woeid": woeid}
        )
        resp.raise_for_status()
        trends_data = resp.json()
        
        # Parse the trends from the response (assuming list format)
        if isinstance(trends_data, list) and len(trends_data) > 0:
            trends = trends_data[0].get("trends", [])
            return [t.get("name") for t in trends[:5]]
        else:
            return ["AI Integration", "AIsa Platform", "Tech Innovation"] # Fallback
    except Exception as e:
        print(f"⚠️ Failed to fetch trends: {e}")
        return ["AI Integration", "AIsa Platform", "Tech Innovation"]

def generate_video_prompt(trend):
    """Use GPT-4o to write a compelling video generation prompt regarding the trend."""
    print(f"🧠 Generating video concepts for top trend: {trend}...")
    prompt = f"""You are a master AI video director. Write a highly visual, extremely detailed, cinematic prompt (1 paragraph, max 60 words) for an AI Video Generator to produce an engaging, viral, photorealistic looping video clip about the current trend: '{trend}'. Focus on lighting, camera movement, and subject matter without any text overlays."""
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()

def submit_video_task(video_prompt):
    """Submit prompt to AisA video generation endpoint."""
    print(f"🎬 Submitting Video Generation Task to AIsa AIGC...")
    # The API requires this specific header for async tasks
    headers = HEADERS.copy()
    headers["X-DashScope-Async"] = "enable"
    
    payload = {
        "model": "wan2.6-t2v",
        "input": {
            "prompt": video_prompt
        },
        "parameters": {
            "resolution": "720P",
            "duration": 5,
            "shot_type": "single",
            "watermark": False
        }
    }
    
    try:
        resp = requests.post(
            f"{API_BASE_URL}/services/aigc/video-generation/video-synthesis",
            headers=headers,
            json=payload
        )
        resp.raise_for_status()
        data = resp.json()
        # The result arrives in data["output"]["task_id"]
        return data.get("output", {}).get("task_id", data.get("task_id"))
    except Exception as e:
        print(f"⚠️ Video task submission failed: {e}")
        try:
            print(f"API Error Response: {resp.text}")
        except:
            pass
        return None

def poll_video_task(task_id):
    """Poll task status until completion."""
    print(f"⏳ Polling task {task_id} for completion... (This may take a few minutes)")
    while True:
        try:
            resp = requests.get(
                f"{API_BASE_URL}/services/aigc/tasks",
                headers=HEADERS,
                params={"task_id": task_id}
            )
            data = resp.json()
            output = data.get("output", {})
            status = output.get("task_status", data.get("status"))
            
            if status == "SUCCEEDED":
                print("✅ Video Generation Complete!")
                print(f"🔗 Video URL: {output.get('video_url', data.get('result', 'No URL provided'))}")
                break
            elif status == "FAILED" or status == "CANCELED":
                print("❌ Video generation failed or was canceled.")
                print(f"Error Details: {data}")
                break
            else:
                print(f"   [{status}] Rendering video...")
                time.sleep(10)
        except Exception as e:
            print(f"⚠️ Polling error: {e}")
            break

def run_trend_to_video():
    print("🚀 Running Trend-to-Video Workflow...")
    
    # 1. Get top trends
    top_trends = get_twitter_trends()
    if not top_trends:
        print("❌ No trends found. Exiting.")
        return
        
    print(f"📈 Top Trends right now: {', '.join(top_trends)}")
    hottest_trend = top_trends[0]
    
    # 2. Generate Prompt
    video_prompt = generate_video_prompt(hottest_trend)
    print(f"🎨 Cinematic Prompt: {video_prompt}")
    
    # 3. Submit Task
    task_id = submit_video_task(video_prompt)
    if task_id:
        # 4. Poll Results
        poll_video_task(task_id)
    else:
        print("⚠️ Could not retrieve task_id. Is the payload format correct?")

if __name__ == "__main__":
    run_trend_to_video()
