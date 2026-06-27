from services.gemini_service import extract_claims_with_gemini

sample = """
OpenAI has 500 million weekly active users.

India's GDP grew by 8.2%.

We are the best company in the world.

Tesla revenue reached 97 billion dollars.
"""

claims = extract_claims_with_gemini(sample)

print(claims)