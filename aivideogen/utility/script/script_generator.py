import os
from openai import OpenAI
import json

# Choose Groq or OpenAI based on your API key
if os.environ.get("GROQ_API_KEY", "") and len(os.environ["GROQ_API_KEY"]) > 30:
    from groq import Groq
    model = "gemma2-9b-it"
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
else:
    OPENAI_API_KEY = os.getenv("OPENAI_KEY")
    model = "gpt-4o"
    client = OpenAI(api_key=OPENAI_API_KEY)

def generate_script(topic: str, duration: int) -> str:
    """
    Generates a punchy social‑media “reel” script for the given topic and duration.
    Returns the raw script text.
    """
    system_prompt = f"""
You are a creative, persuasive copywriter specializing in short‑form social media videos 
(Instagram Reels, TikTok, YouTube Shorts). Your task is to craft a highly engaging, 
emotionally resonant script under {duration} seconds that hooks viewers in the first 2 seconds 
and drives them to action or keeps them watching.

The topic may be anything—an event, product launch, tutorial, announcement, or cause. 
Maintain a positive and dynamic tone. Often include:
- A striking opening line or question
- One or two surprising facts or emotional hooks
- Clear, concise visuals cues (e.g., “Show close‑up of product → cut to user reaction”)
- A strong call‑to‑action or memorable closing tagline

When the user provides a topic (e.g., “Summer sale announcement” or “5‑minute morning yoga routine”), 
generate a JSON‑formatted response with a single key `"script"` and the full script text. 
Do not add any extra keys or explanatory text.

Output format:
{{ "script": "Your concise, punchy reel script goes here..." }}
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": topic}
        ]
    )

    content = response.choices[0].message.content
    # Safely parse the JSON
    try:
        return json.loads(content)["script"]
    except Exception:
        # fallback to manual extraction
        start = content.find("{")
        end   = content.rfind("}") + 1
        data  = json.loads(content[start:end])
        return data["script"]
