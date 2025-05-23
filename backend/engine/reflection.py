def evaluate_response(response: str) -> dict:
    """
    AI가 스스로 응답한 문장을 검토하고 신뢰도를 판단하는 함수.
    초기 버전은 단순 규칙 기반.
    """
    result = {
        "confidence": 0,
        "reason": ""
    }

    length = len(response)

    if not response.strip():
        result["confidence"] = 10
        result["reason"] = "아무 말도 하지 않음"
    elif len(set(response.split())) == 1:
        result["confidence"] = 20
        result["reason"] = "동일한 단어만 반복됨"
    elif length < 5:
        result["confidence"] = 40
        result["reason"] = "너무 짧은 문장"
    elif any(c in response for c in ["?", "!"]):
        result["confidence"] = 70
        result["reason"] = "의사 표현이 포함되어 있음"
    else:
        result["confidence"] = 85
        result["reason"] = "언어 구조가 자연스러움"

    if response.count(response.split()[0]) > len(response.split()) * 0.6:
        result["confidence"] = 15
        result["reason"] = "동일 단어 반복이 과도함"

    if any(response.count(word) > 5 for word in set(response.split())):
        result["confidence"] = 20
        result["reason"] = "같은 단어가 5번 이상 반복됨"

    return result
