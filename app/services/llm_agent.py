import json
import requests
from app.config import settings

def generate_execution_plan(user_request: str) -> dict:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
    
    prompt = f"""
    You are an autonomous planning and document-generation agent. 
    Convert the following natural-language request into a structured, dependency-aware execution plan.
    
    User Request: "{user_request}"

    Return ONLY a valid JSON object containing these precise keys:
    - title: Project title
    - objectives: List of core project objectives
    - requirements: List of technical/functional requirements
    - tasks: List of objects, each containing: "id", "name", "description", "dependencies" (list of task IDs it depends on), "timeline" (estimated duration)
    - resources: List of required resources/tools
    - risks: List of potential risks and mitigation strategies
    - execution_strategy: Summary text of how to execute the plan
    """

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json"}
    }

    response = requests.post(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Gemini API Error: {response.text}")

    result = response.json()
    raw_text = result["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(raw_text)