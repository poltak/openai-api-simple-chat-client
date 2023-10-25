# openai-api-simple-chat-client

## Install

```
python -m venv .venv
python -m pip install -r requirements.txt
```

## Usage

```
# Basic prompt
OPENAI_API_KEY='sk-...' python chat.py my-chat

# Basic prompt with gpt4
OPENAI_API_KEY='sk-...' python chat.py my-chat 4

# Custom prompt with gpt3-turbo
OPENAI_API_KEY='sk-...' python chat.py my-chat "System prompt..."

# Custom prompt with gpt4
OPENAI_API_KEY='sk-...' python chat.py my-chat "System prompt..." 4
```
