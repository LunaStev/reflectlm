import json
import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def save_conversation(user_input: str, ai_response: str, reflection: dict, lang: str = "ko"):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "language": lang,
        "user_input": user_input,
        "ai_response": ai_response,
        "reflection": reflection
    }

    path = os.path.join(LOG_DIR, f"{lang}.jsonl")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
