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
- confidence: a float between 0.0 and 1.0 indicating how clearly the claim is supported by the evidence

You MUST return ONLY valid JSON.
Do NOT include explanations.
Do NOT include markdown.
Do NOT include numbering.
Do NOT include text before or after JSON.

Return EXACTLY this format:
[
  {{
    "claim": "...",
    "evidence": "...",
    "confidence": 0.95
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

    except Exception as e:
        print(f"\n⚠️ Failed parsing source {source.source_id}")
        print("Error:", e)
        print("Raw output:\n", content)
        return []


    claims = []
    for item in parsed:
        claims.append(
            Claim(
                claim=item["claim"],
                evidence=item["evidence"],
                source_id=source.source_id,
                confidence=float(item["confidence"]) if "confidence" in item else None
            )
        )

    return claims
