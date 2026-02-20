import json
from openai import OpenAI
from typing import List
from agent.models import Claim, Source
from config.settings import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    CHAT_MODEL,
    MAX_CLAIMS_PER_SOURCE
)

# Initialize OpenRouter client
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL
)


def extract_claims(source: Source) -> List[Claim]:
    prompt = f"""
Extract up to {MAX_CLAIMS_PER_SOURCE} key claims from the text below.

Each claim must include:
- claim: concise statement
- evidence: exact quote from the text supporting the claim

Return ONLY valid JSON list:
[
  {{
    "claim": "...",
    "evidence": "..."
  }}
]

Only extract claims explicitly stated in the text.
Do not invent information.

TEXT:
{source.content}
"""

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    try:
        content = response.choices[0].message.content.strip()

        # Extract JSON array safely
        start = content.find("[")
        end = content.rfind("]") + 1
        json_block = content[start:end]

        parsed = json.loads(json_block)

    except Exception:
        print("⚠️ Failed to parse model output.")
        print("Raw model output:\n", content)
        return []


    claims = []
    for item in parsed:
        claims.append(
            Claim(
                claim=item["claim"],
                evidence=item["evidence"],
                source_id=source.source_id
            )
        )

    return claims
