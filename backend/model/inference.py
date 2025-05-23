import torch
from tokenizers import Tokenizer
from .transformer import TransformerLanguageModel

def load_model_and_tokenizer(lang: str):
    tokenizer = Tokenizer.from_file(f"tokenizers/{lang}.json")
    vocab_size = tokenizer.get_vocab_size()
    model = TransformerLanguageModel(vocab_size)
    model.load_state_dict(torch.load(f"checkpoints/{lang}/model.pt"))
    model.eval()
    return model, tokenizer

def generate_response(model, tokenizer, user_input: str, max_length: int = 32):
    input_ids = tokenizer.encode(user_input).ids
    input_tensor = torch.tensor([input_ids])
    with torch.no_grad():
        for _ in range(max_length):
            outputs = model(input_tensor)
            next_token = torch.argmax(outputs[0, -1]).item()
            next_token_tensor = torch.tensor([[next_token]])
            input_tensor = torch.cat([input_tensor, next_token_tensor], dim=1)
            if next_token == tokenizer.token_to_id("<PAD>"):
                break
    return tokenizer.decode(input_tensor[0].tolist())