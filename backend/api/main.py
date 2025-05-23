from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.model.inference import load_model_and_tokenizer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

lang = "ko"
model, tokenizer = load_model_and_tokenizer(lang)

@app.on_event("startup")
def load_model():
    from backend.model.inference import load_model_and_tokenizer
    global model, tokenizer
    model, tokenizer = load_model_and_tokenizer(lang)

from backend.model.inference import generate_response
from backend.engine.reflection import evaluate_response
from backend.engine.memory import save_conversation

class ChatInput(BaseModel):
    message: str

@app.post("/chat")
def chat(input: ChatInput):
    response = generate_response(model, tokenizer, input.message)
    reflection = evaluate_response(response)
    save_conversation(input.message, response, reflection, lang)
    return {
        "response": response,
        "confidence": reflection["confidence"],
        "reason": reflection["reason"]
    }
