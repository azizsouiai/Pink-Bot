# Chatbruti

A well-structured Python project for loading and interacting with LLM models. Supports local inference via Hugging Face and cloud inference via Groq API. Default configuration uses Groq with GPT OSS 120B model.

## Features

- 🚀 **Multiple Backends**: Support for Hugging Face (local) and Groq API (cloud)
- ⚙️ **Flexible Configuration**: Environment-based configuration with sensible defaults
- 🏗️ **Clean Architecture**: Modular design with interfaces and factory pattern
- 💻 **CLI Interface**: Command-line interface with interactive mode
- 🔧 **Quantization Support**: 4-bit and 8-bit quantization for memory efficiency
- 📝 **Type Hints**: Full type annotations for better code quality

## Project Structure

```
Chatbruti/
├── src/
│   └── chatbruti/
│       ├── __init__.py
│       ├── main.py              # CLI entry point
│       ├── config/
│       │   ├── __init__.py
│       │   └── settings.py     # Configuration management
│       └── models/
│           ├── __init__.py
│           ├── base.py         # Base interface
│           ├── huggingface_model.py
│           ├── groq_model.py
│           └── factory.py     # Model factory
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd Chatbruti
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Configuration

Create a `.env` file in the project root (copy from `.env.example`):

### System Prompt

You can customize the AI's behavior by editing the `system_prompt.txt` file in the project root. This file contains instructions that are sent to the model before each user prompt, allowing you to set the AI's personality, role, or behavior.

**Example system prompt:**
```
You are a helpful, knowledgeable, and friendly AI assistant. 
You provide clear, accurate, and concise responses to user questions. 
Always be respectful and professional in your interactions.
```

The system prompt is automatically loaded and used with every request. You can change the file path in your `.env` file by setting `SYSTEM_PROMPT_FILE`.

### For Groq API Backend (Cloud) - Recommended

```env
MODEL_NAME=openai/gpt-oss-120b
BACKEND=groq
GROQ_API_KEY=your_groq_api_key_here
REASONING_EFFORT=medium  # Options: low, medium, high
```

### For Hugging Face Backend (Local)

```env
MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.2
BACKEND=huggingface
DEVICE=auto  # auto, cpu, cuda, mps
TORCH_DTYPE=auto
LOAD_IN_8BIT=false  # Set to true for 8-bit quantization
LOAD_IN_4BIT=false  # Set to true for 4-bit quantization
```

### Generation Parameters

```env
MAX_NEW_TOKENS=8192
TEMPERATURE=1.0
TOP_P=1.0
TOP_K=50
DO_SAMPLE=true
```

### System Prompt Configuration

Edit `system_prompt.txt` in the project root to customize the AI's behavior. This prompt is automatically included with every request.

You can also specify a different file path:
```env
SYSTEM_PROMPT_FILE=system_prompt.txt
```

## Usage

### Command Line Interface

**Single prompt:**
```bash
python -m chatbruti.main --prompt "Explain quantum computing in simple terms"
```

**Interactive mode:**
```bash
python -m chatbruti.main --interactive
```

**With custom parameters:**
```bash
python -m chatbruti.main \
  --prompt "Write a short story" \
  --max-tokens 1000 \
  --temperature 0.9
```

**Show model information:**
```bash
python -m chatbruti.main --model-info
```

**Use different backend:**
```bash
python -m chatbruti.main --backend groq --prompt "Hello!"
python -m chatbruti.main --backend huggingface --prompt "Hello!"
```

### Python API

```python
from chatbruti.config import get_settings
from chatbruti.models import create_model

# Get settings
settings = get_settings()

# Create and load model
model = create_model(backend="huggingface", settings=settings)
model.load()

# Generate response
response = model.generate(
    prompt="What is machine learning?",
    max_new_tokens=256,
    temperature=0.7
)

print(response)

# For Groq with streaming
response = model.generate(
    prompt="Explain AI",
    stream=True  # Enable streaming
)
print(response)
```

## Backends

### Groq API (Cloud) - Default & Recommended

- Runs on Groq's ultra-fast inference servers
- Requires Groq API key
- Extremely fast inference (optimized hardware)
- Supports reasoning models with `reasoning_effort` parameter
- Pay-per-use pricing
- No local model download needed
- Default model: `openai/gpt-oss-120b` (120B parameter model)

### Hugging Face (Local)

- Runs the model locally on your machine
- Requires sufficient RAM/VRAM (7B model needs ~14GB+)
- Supports quantization (4-bit/8-bit) to reduce memory usage
- No API key required
- Slower initial load, but no API costs

## Memory Requirements

For local models (e.g., Mistral 7B):

- **Full precision (float32)**: ~28GB RAM/VRAM
- **Half precision (float16)**: ~14GB RAM/VRAM
- **8-bit quantization**: ~7GB RAM/VRAM
- **4-bit quantization**: ~4GB RAM/VRAM

## Troubleshooting

### Out of Memory Errors

- Enable quantization: `LOAD_IN_4BIT=true` or `LOAD_IN_8BIT=true`
- Use CPU instead of GPU: `DEVICE=cpu`
- Reduce `MAX_NEW_TOKENS`

### Model Download Issues

- Ensure you have sufficient disk space (~14GB for the model)
- Check your internet connection
- For Hugging Face, you may need to login: `huggingface-cli login`

### API Key Issues

- For Groq: Ensure `GROQ_API_KEY` is set in `.env`
- Verify the API key is valid
- Check your Groq API account status

## Development

### Project Structure Principles

- **Separation of Concerns**: Configuration, models, and CLI are separated
- **Interface-Based Design**: Base interface allows easy backend swapping
- **Factory Pattern**: Centralized model creation
- **Configuration Management**: Environment-based with Pydantic validation

### Adding a New Backend

1. Create a new model class inheriting from `BaseModelInterface`
2. Implement all abstract methods
3. Register it in `ModelFactory._backends`

## License

This project is provided as-is for educational and development purposes.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

