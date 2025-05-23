import json
import torch
import os
from torch.utils.data import Dataset, DataLoader
from tokenizers import Tokenizer, models, trainers, pre_tokenizers
from transformer import TransformerLanguageModel

class TextDataset(Dataset):
    def __init__(self, file_path, tokenizer, block_sizes=[4, 16, 32, 64]):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.examples = []

        for block_size in block_sizes:
            buffer = ""
            for item in data:
                buffer += item["text"] + " "
                token_ids = tokenizer.encode(buffer).ids
                while len(token_ids) >= block_size:
                    self.examples.append(token_ids[:block_size])
                    token_ids = token_ids[block_size:]
                    buffer = tokenizer.decode(token_ids)

        import random
        random.shuffle(self.examples)

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        x = torch.tensor(self.examples[idx][:-1])
        y = torch.tensor(self.examples[idx][1:])
        return x, y

def pad_collate(batch, pad_id=0):
    x_batch, y_batch = zip(*batch)
    max_len = max(len(x) for x in x_batch)
    x_padded = [torch.cat([x, torch.full((max_len - len(x),), pad_id)]) for x in x_batch]
    y_padded = [torch.cat([y, torch.full((max_len - len(y),), pad_id)]) for y in y_batch]
    return torch.stack(x_padded), torch.stack(y_padded)

def train_model(language):
    data_path = f"data/{language}/train.json"
    tokenizer_path = f"tokenizers/{language}.json"
    model_path = f"checkpoints/{language}/model.pt"
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
    dataset = TextDataset(data_path, tokenizer, block_sizes=[4, 16, 32])
    pad_id = tokenizer.token_to_id("<PAD>")
    loader = DataLoader(dataset, batch_size=16, shuffle=True, collate_fn=lambda b: pad_collate(b, pad_id))

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