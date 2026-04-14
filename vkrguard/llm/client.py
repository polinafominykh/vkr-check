import os
from openai import OpenAI


def get_llm_client() -> OpenAI:
    base_url = os.getenv("OPENAI_BASE_URL", "http://10.32.2.11:8041/v1")
    api_key = os.getenv("OPENAI_API_KEY", "test-key")

    return OpenAI(
        base_url=base_url,
        api_key=api_key,
    )


def ask_llm(prompt: str, model: str = "/model") -> str:
    client = get_llm_client()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Ты помощник для проверки ВКР. Отвечай строго по формату и кратко."
            },
            {
                "role": "user",
                "content": prompt
            },
        ],
        temperature=0,
    )

    return response.choices[0].message.content