"""
Example script demonstrating how to use Chatbruti programmatically.
"""

import logging
from chatbruti.config import get_settings
from chatbruti.models import create_model
from chatbruti.utils import get_system_prompt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

def main():
    """Example usage of the Chatbruti library."""
    
    # Get settings (loads from .env or uses defaults)
    settings = get_settings()
    print(f"Using backend: {settings.backend}")
    print(f"Model: {settings.model_name}\n")
    
    # Create model instance
    model = create_model(backend=settings.backend, settings=settings)
    
    # Load the model
    print("Loading model...")
    model.load()
    
    # Load system prompt
    system_prompt = get_system_prompt()
    if system_prompt:
        print(f"System prompt loaded: {system_prompt[:80]}...\n")
    else:
        print("No system prompt file found, using default behavior\n")
    
    # Show model info
    info = model.get_model_info()
    print("Model Information:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    print()
    
    # Example prompts
    prompts = [
        "What is artificial intelligence?",
        "Explain the concept of recursion in programming.",
        "Write a haiku about coding.",
    ]
    
    # Generate responses
    for i, prompt in enumerate(prompts, 1):
        print(f"Prompt {i}: {prompt}")
        print("-" * 60)
        
        response = model.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            max_new_tokens=256,
            temperature=0.7,
        )
        
        print(f"Response: {response}\n")
        print("=" * 60 + "\n")

if __name__ == "__main__":
    main()

