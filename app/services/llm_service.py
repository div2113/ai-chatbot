import requests

OLLAMA_URL ="http://localhost:11434/api/generate"
MODEL_NAME= "qwen2.5-coder:0.5b"

SYSTEM_PROPMT= """
You are a helpful AI assistant.

Rules:
- Give clear and simple answers.
- Be accurate and concise.
- If you don't know something , say that you don't know.
- Do not invent facts.
"""

def build_prompt(user_message:str):
    return f"""
{SYSTEM_PROPMT}

User:
{user_message}

Assistant:
"""

def generate_response(prompt):
    full_prompt= build_prompt(prompt)
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": full_prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()
        data=response.json()

        return data["response"].strip()

    except requests.exceptions.Timeout:
        raise Exception("LLM request timed out")

    except requests.exceptions.ConnectionError:
        raise Exception("Could not connect to Ollama")

    except requests.exceptions.RequestException:
        raise Exception("LLM request failed")