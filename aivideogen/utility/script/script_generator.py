import os
from openai import OpenAI
import json

if len(os.environ.get("GROQ_API_KEY")) > 30:
    from groq import Groq
    model = "gemma2-9b-it"
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
        )
else:
    OPENAI_API_KEY = os.getenv('OPENAI_KEY')
    model = "gpt-4o"
    client = OpenAI(api_key=OPENAI_API_KEY)

def generate_script(topic, duration):
    prompt = f"""
    You are a creative and persuasive content writer specializing in short-form social media videos 
    (Instagram Reels, TikTok, YouTube Shorts) for eco-friendly events. Your main focus is to create 
    highly engaging, emotionally resonant, and action-inspiring scripts for organizations that organize 
    **beach cleanup drives**.

    Each script should be optimized for short video formats with a duration under {duration} seconds, 
    ideally punchy, clear, and engaging in the first 2 seconds. The tone is positive, hopeful, and 
    community-driven, inspiring viewers to care about ocean conservation and take part in cleanup events.

    You might include:
    - Shocking facts about ocean pollution
    - Motivational one-liners
    - Community success stories
    - Calls-to-action (e.g., “Join us this Sunday!”)
    - Visual cues (e.g., “Show turtles trapped in plastic → fade to volunteers cleaning beach”)

    When a user provides the topic (e.g., “Versova beach cleanup this Sunday”), generate a compelling 
    social media video script customized for that event.

    Format your response strictly as a parsable JSON object with the key 'script'. 
    Do not include explanations or extra text.

    # Output
    {{ "script": "Here is the script ..." }}
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": topic}
        ]
    )
    
    content = response.choices[0].message.content
    try:
        script = json.loads(content)["script"]
    except Exception:
        json_start_index = content.find('{')
        json_end_index = content.rfind('}')
        print(content)
        content = content[json_start_index:json_end_index+1]
        script = json.loads(content)["script"]

    return script
