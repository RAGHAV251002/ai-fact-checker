import os

from dotenv import load_dotenv
import google.generativeai as genai

from utils.json_parser import parse_json_response

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def extract_claims_with_gemini(text: str):
    """
    Extract factual claims from PDF using Gemini.

    Always returns a list of dictionaries.
    """

    prompt = f"""
You are an expert AI fact extraction system.

Extract ONLY factual claims.

Ignore:

- Instructions
- Opinions
- Titles
- Bullet headings
- Questions

Keep ONLY claims containing:

- Statistics
- Percentages
- Dates
- Years
- Revenue
- Funding
- Market Size
- Company Facts
- Technical Facts
- Research Findings

Return ONLY a VALID JSON ARRAY.

DO NOT explain anything.

DO NOT use markdown.

DO NOT use ```json.

Return EXACTLY like this:

[
    {{
        "claim":"OpenAI has 800 million weekly active users.",
        "type":"Statistic"
    }},
    {{
        "claim":"ChatGPT launched in 2022.",
        "type":"Date"
    }}
]

TEXT

{text}
"""

    try:

        response = model.generate_content(prompt)

        result = parse_json_response(response.text)

        # -----------------------------
        # Normalize response
        # -----------------------------

        if isinstance(result, dict):

            if "claims" in result:
                result = result["claims"]

            else:
                result = [result]

        normalized = []

        for item in result:

            # Gemini returned string
            if isinstance(item, str):

                normalized.append(
                    {
                        "claim": item,
                        "type": "Unknown"
                    }
                )

            # Gemini returned dictionary
            elif isinstance(item, dict):

                normalized.append(
                    {
                        "claim": item.get("claim", ""),
                        "type": item.get("type", "Unknown")
                    }
                )

        return normalized

    except Exception as e:

        print(e)

        return []