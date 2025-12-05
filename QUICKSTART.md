# Quick Start Guide

## Setup

1. **Clone the repository (if you haven't already):**
   ```bash
   git clone https://github.com/azizsouiai/Pink-Bot.git
   cd Pink-Bot  # Navigate to the cloned folder
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the package in editable mode:**
   ```bash
   pip install -e .
   ```
   ⚠️ **Important:** This step is required so Python can find the `chatbruti` module.

5. **Create `.env` file:**
   ```bash
   cp .env.example .env
   ```

6. **Edit `.env` file and add your Groq API key:**
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

   The `.env` file should look like:
   ```
   MODEL_NAME=openai/gpt-oss-120b
   BACKEND=groq
   GROQ_API_KEY=your_groq_api_key_here
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
