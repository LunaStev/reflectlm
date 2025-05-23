# ReflectLM

ReflectLM is a self-reflective, language-structure-only AI model that learns exclusively through interaction. It starts with zero factual knowledge but can engage in dialogue, evaluate its own responses, and remember conversations for future learning.

## Features

* Custom Transformer-based language model (no pretrained knowledge)

* CLI interface for local interaction

* FastAPI backend with `/chat` endpoint

* Next.js + TypeScript frontend for web-based chat

* Reflection engine to self-assess AI responses

* Memory engine for saving all conversations

* Multilingual ready (currently supports Korean)

* Fully open-source and locally runnable

## Project Structure

```
reflectlm/
├── backend/
│ ├── api/ → FastAPI REST server
│ ├── engine/ → reflection, memory storage
│ ├── model/ → Transformer model, training, inference
├── frontend/ → Next.js web UI
├── logs/ → Chat memory logs
├── tokenizers/, checkpoints/, data/ → Model-related assets
└── cli.py → Command-line interface
```

## Requirements

* Python 3.10+

* Node.js 18+ (for frontend)

* PyTorch

* FastAPI, Uvicorn

* Tokenizers (HuggingFace)

* TypeScript + Next.js

## Installation

1. Clone the repo:

```bash
git clone https://github.com/yourname/reflectlm.git
cd reflectlm
```

2. Install Python packages:

```bash
python -m venv .venv
source .venv/bin/activate # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

3. Train the model:

```bash
python backend/model/train.py ko
```

4. Start the API server (on Windows or WSL):

```bash
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000
```

5. Start the frontend (on WSL or Windows):

```bash
cd frontend
npm install
npm run dev
```

If you are running backend and frontend in different environments (e.g., backend on Windows, frontend on WSL), make sure to update the API URL in `frontend/pages/index.tsx` to use your Windows host IP instead of `localhost`.

### Example:

```ts
const res = await fetch("http://172.28.32.1:8000/chat", ...
```

You can find the correct IP using `ipconfig` on Windows, look for the WSL virtual adapter.

## Usage

* Open the frontend at `http://localhost:3000`

* Type messages into the input

* View AI responses and self-evaluation (confidence + reasoning)

* All conversations are logged in `logs/ko.jsonl`

## Development Notes

* All AI behavior is derived from language-only training

* The model does not contain external factual knowledge

* Designed for experimentation and educational purposes

* Extension ideas include GPT-assisted reflection, better decoding, self-finetuning, multilingual switching

## License

MPL-2.0 License. Use freely, contribute freely.