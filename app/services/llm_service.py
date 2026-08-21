import requests

OLLAMA_URL ="http://localhost:11434/api/generate"
MODEL_NAME= "qwen2.5-coder:0.5b"

SYSTEM_PROMPT= """
You are a helpful AI assistant.

Rules:
- Answer the user's question directly.
- Keep answers concise.
- Do not add unnecessary explanations.
- If the user asks for a name, date, number, or other simple fact, give the answer directly.
- If you don't know something, say that you don't know.
- Do not invent facts.
"""

def build_prompt(user_message:str):
    return f"""
{SYSTEM_PROMPT}

User:
{user_message}

Assistant:
"""

def generate_response(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
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


def build_chat_prompt(messages: list , summary: str | None = None) -> str:
    prompt = SYSTEM_PROMPT.strip() + "\n\n"

    if summary:
        prompt += f"""
Conversation summary :
{summary}

"""

    for message in messages:
        prompt += f"{message.role.capitalize()}: {message.content}\n"

    prompt += "\nAssistant:"

    return prompt


def generate_summary(messages: list) -> str:
    conversation_text = ""

    for message in messages:
        conversation_text += (
            f"{message.role.capitalize()}: "
            f"{message.content}\n"
        )

    prompt = f"""
Summarize the important information from this conversation.

Keep:
- Important facts about the user
- User preferences
- Important topics discussed
- Important decisions or context

Do not include unnecessary details.

Conversation:
{conversation_text}

Summary:
"""

    return generate_response(prompt)