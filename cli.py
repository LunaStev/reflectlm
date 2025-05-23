from backend.model.inference import load_model_and_tokenizer, generate_response
from backend.engine.reflection import evaluate_response
from backend.engine.memory import save_conversation

def evaluate_confidence(response):
    length = len(response)
    if length < 5:
        confidence = 30
    elif length < 15:
        confidence = 60
    else:
        confidence = 80 + (length % 20)
    return confidence

def main():
    lang = "ko"
    model, tokenizer = load_model_and_tokenizer(lang)

    print(f"[{lang.upper()} ReflectLM] 대화를 시작합니다. 종료하려면 Ctrl+C\n")
    while True:
        try:
            user_input = input("당신: ")
            response = generate_response(model, tokenizer, user_input)
            confidence = evaluate_confidence(response)
            reflection = evaluate_response(response)
            print(f"AI: {response}")
            print(f"[신뢰도 평가] {reflection['confidence']}% 확신")
            print(f"[이유] {reflection['reason']}\n")
            save_conversation(user_input, response, reflection, lang)
        except KeyboardInterrupt:
            print("\n대화를 종료합니다.")
            break

if __name__ == "__main__":
    main()