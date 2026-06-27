import re
from typing import List

import spacy

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")


def extract_claims(text: str) -> List[str]:
    """
    Extract factual claim candidates from text.

    Returns:
        List of possible factual claims.
    """

    doc = nlp(text)

    claims = []

    for sent in doc.sents:

        sentence = sent.text.strip()

        if len(sentence) < 20:
            continue

        # Ignore questions
        if sentence.endswith("?"):
            continue

        # Ignore bullet titles
        if len(sentence.split()) < 4:
            continue

        # Keep sentences containing numbers
        has_number = bool(re.search(r"\d", sentence))

        # Keep sentences containing named entities
        has_entity = any(
            ent.label_ in [
                "ORG",
                "GPE",
                "DATE",
                "MONEY",
                "PERCENT",
                "CARDINAL"
            ]
            for ent in sent.ents
        )

        if has_number or has_entity:
            claims.append(sentence)

    return claims