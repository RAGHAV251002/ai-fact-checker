import json
import re


def parse_json_response(response_text: str):
    """
    Parse Gemini responses safely.

    Handles:
    - ```json ... ```
    - Extra explanatory text
    - JSON arrays
    - JSON objects
    """

    if not response_text:
        raise ValueError("Empty response received from Gemini.")

    # Remove markdown fences
    cleaned = re.sub(r"```json|```", "", response_text).strip()

    # -------------------------
    # Try direct JSON parsing
    # -------------------------
    try:
        return json.loads(cleaned)

    except json.JSONDecodeError:
        pass

    # -------------------------
    # Try extracting JSON array
    # -------------------------
    array_match = re.search(
        r"(\[\s*.*\s*\])",
        cleaned,
        re.DOTALL
    )

    if array_match:

        try:
            return json.loads(array_match.group(1))

        except json.JSONDecodeError:
            pass

    # -------------------------
    # Try extracting JSON object
    # -------------------------
    object_match = re.search(
        r"(\{\s*.*\s*\})",
        cleaned,
        re.DOTALL
    )

    if object_match:

        try:
            return json.loads(object_match.group(1))

        except json.JSONDecodeError:
            pass

    raise ValueError(
        f"Unable to parse Gemini response:\n\n{response_text}"
    )