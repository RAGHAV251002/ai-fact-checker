import json
import os

from dotenv import load_dotenv
import google.generativeai as genai

from utils.json_parser import parse_json_response

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def verify_claims(claims_with_evidence):
    """
    Verify all claims in a single Gemini request.
    """

    prompt = f"""
You are an expert AI Fact Checker.

You will receive a JSON array.

Each object contains:

- claim
- evidence

For EVERY claim classify it into EXACTLY ONE category:

- Verified
- False
- Outdated
- Insufficient Evidence

Return ONLY a VALID JSON ARRAY.

DO NOT return markdown.

DO NOT return ```json.

DO NOT explain anything.

Return exactly like this:

[
  {{
    "claim": "...",
    "status": "Verified",
    "confidence": 96,
    "correct_fact": "...",
    "reason": "..."
  }}
]

Claims and Evidence:

{json.dumps(claims_with_evidence, indent=2)}
"""

    response = model.generate_content(prompt)

    result = parse_json_response(response.text)

    # Gemini sometimes returns a dictionary instead of a list
    if isinstance(result, dict):

        if "results" in result:
            return result["results"]

        return [result]

    return result