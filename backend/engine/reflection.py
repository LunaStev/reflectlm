def evaluate_response(response: str) -> dict:
    """
    A function that allows the AI to evaluate its own response and determine confidence.
    The initial version is based on simple rule-based logic.
    Now with cute emojis! 🐣🌟
    """
    result = {
        "confidence": 0,
        "reason": ""
    }

    length = len(response)

    if not response.strip():
        result["confidence"] = 10
        result["reason"] = "🫥 Said nothing at all"
    elif len(set(response.split())) == 1:
        result["confidence"] = 20
        result["reason"] = "🔁 Only repeated the same word"
    elif length < 5:
        result["confidence"] = 40
        result["reason"] = "📏 Sentence too short"
    elif any(c in response for c in ["?", "!"]):
        result["confidence"] = 70
        result["reason"] = "❗ Includes expressive punctuation"
    else:
        result["confidence"] = 85
        result["reason"] = "✅ Natural language structure"

    if response.count(response.split()[0]) > len(response.split()) * 0.6:
        result["confidence"] = 15
        result["reason"] = "🚨 Excessive repetition of the same word"

    if any(response.count(word) > 5 for word in set(response.split())):
        result["confidence"] = 20
        result["reason"] = "🔂 A word is repeated more than 5 times"

    return result
