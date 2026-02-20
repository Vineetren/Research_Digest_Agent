from openai import OpenAI
from config.settings import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    CHAT_MODEL
)

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL
)


def llm_conflict_check(claim1: str, claim2: str) -> bool:
    """
    Uses LLM to determine if two claims conflict.
    """

    prompt = f"""
Determine whether the following two claims express conflicting viewpoints.

Claim 1:
{claim1}

Claim 2:
{claim2}

Respond with ONLY one word:
YES or NO
"""

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": "You are a precise reasoning engine."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    answer = response.choices[0].message.content.strip().upper()

    return answer == "YES"
