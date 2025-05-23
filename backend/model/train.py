import json
import torch
import os
from torch.utils.data import Dataset, DataLoader
from tokenizers import Tokenizer, models, trainers, pre_tokenizers
from transformer import TransformerLanguageModel

class TextDataset(Dataset):
    def __init__(self, file_path, tokenizer, block_size=64):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.examples = []
        for item in data:
            encoded = tokenizer.encode(item["text"]).ids
            for i in range(0, len(encoded) - block_size + 1):
                self.examples.append(encoded[i:i+block_size])
                print(f"[DEBUG] 문장 길이: {len(encoded)} 토큰 → 추가됨: {len(encoded) - block_size + 1 > 0}")
        self.block_size = block_size

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        x = torch.tensor(self.examples[idx][:-1])
        y = torch.tensor(self.examples[idx][1:])
        return x, y

def train_model(language):
    data_path = f"../../data/{language}/train.json"
    tokenizer_path = f"../../tokenizers/{language}.json"
    model_path = f"../../checkpoints/{language}/model.pt"
    os.makedirs(os.path.dirname(tokenizer_path), exist_ok=True)
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    if not os.path.exists(tokenizer_path):
        tokenizer = Tokenizer(models.BPE())
        tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
        trainer = trainers.BpeTrainer(special_tokens=["<PAD>", "<UNK>"])
        with open(data_path, "r", encoding="utf-8") as f:
            lines = [item["text"] for item in json.load(f)]
        tokenizer.train_from_iterator(lines, trainer)
        tokenizer.save(tokenizer_path)
    else:
        tokenizer = Tokenizer.from_file(tokenizer_path)

    vocab_size = tokenizer.get_vocab_size()
    model = TransformerLanguageModel(vocab_size)
    dataset = TextDataset(data_path, tokenizer, block_size=8)
    loader = DataLoader(dataset, batch_size=16, shuffle=True)

    if len(dataset) == 0:
        print(f"[ERROR] 학습 샘플이 없습니다. block_size를 더 줄이거나 문장을 더 늘리세요.")
        return


    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
    loss_fn = torch.nn.CrossEntropyLoss()

    model.train()
    for epoch in range(5) :
        total_loss = 0
        for x, y, in loader:
            out = model(x)
            loss = loss_fn(out.view(-1, vocab_size), y.view(-1))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"[{language}] Epoch {epoch+1} Loss: {total_loss:.4f}")

    torch.save(model.state_dict(), model_path)
    print(f"[{language}] 모델 저장 완료: {model_path}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("사용법: python train.py <언어코드>")
    else:
        train_model(sys.argv[1])