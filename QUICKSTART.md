# Quick Start Guide

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create `.env` file:**
   ```bash
   cp .env.example .env
   ```

3. **Edit `.env` file and add your Groq API key:**
   ```
   GROQ_API_KEY= your key
   ```

   The `.env` file should look like:
   ```
   MODEL_NAME=openai/gpt-oss-120b
   BACKEND=groq
   GROQ_API_KEY= you key
   REASONING_EFFORT=medium
   MAX_NEW_TOKENS=8192
   TEMPERATURE=1.0
   TOP_P=1.0
   ```

## Usage

**Interactive mode:**
```bash
python -m chatbruti.main --interactive
```

**Single prompt:**
```bash
python -m chatbruti.main --prompt "Explain quantum computing"
```

**Run example script:**
```bash
python example.py
```

## Python API

```python
from chatbruti.config import get_settings
from chatbruti.models import create_model

# Create and load model
model = create_model(backend="groq")
model.load()

# Generate response
response = model.generate("What is AI?")
print(response)
```
