"""Main application entry point."""

import argparse
import logging
import sys
from typing import Optional

from .config import get_settings
from .models import create_model
from .utils import get_system_prompt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Chatbruti - Interact with LLM models via Groq API or Hugging Face"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        help="Prompt to send to the model",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode",
    )
    parser.add_argument(
        "--backend",
        type=str,
        choices=["huggingface", "groq"],
        help="Backend to use (overrides environment variable)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        help="Maximum number of tokens to generate",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        help="Sampling temperature",
    )
    parser.add_argument(
        "--model-info",
        action="store_true",
        help="Show model information and exit",
    )
    
    args = parser.parse_args()
    
    try:
        # Get settings
        settings = get_settings()
        if args.backend:
            settings.backend = args.backend
        
        # Create model
        logger.info(f"Initializing model with backend: {settings.backend}")
        model = create_model(backend=settings.backend, settings=settings)
        
        # Load model
        logger.info("Loading model...")
        model.load()
        
        # Load system prompt
        system_prompt = get_system_prompt()
        if system_prompt:
            logger.info("System prompt loaded from file")
        else:
            logger.info("No system prompt file found, using default behavior")
        
        # Show model info if requested
        if args.model_info:
            info = model.get_model_info()
            print("\nModel Information:")
            for key, value in info.items():
                print(f"  {key}: {value}")
            if system_prompt:
                print(f"\nSystem Prompt (first 100 chars): {system_prompt[:100]}...")
            return
        
        # Interactive mode
        if args.interactive:
            run_interactive(model, settings, system_prompt)
        # Single prompt mode
        elif args.prompt:
            response = model.generate(
                prompt=args.prompt,
                system_prompt=system_prompt,
                max_new_tokens=args.max_tokens,
                temperature=args.temperature,
            )
            print("\nResponse:")
            print(response)
        else:
            parser.print_help()
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


def run_interactive(model, settings, system_prompt=None):
    """Run in interactive mode."""
    print("\n" + "="*60)
    print("Chatbruti - Interactive Mode")
    print("Type 'exit' or 'quit' to exit, 'clear' to clear screen")
    if system_prompt:
        print(f"System prompt: {system_prompt[:50]}..." if len(system_prompt) > 50 else f"System prompt: {system_prompt}")
    print("="*60 + "\n")
    
    while True:
        try:
            prompt = input("You: ").strip()
            
            if not prompt:
                continue
            
            if prompt.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            
            if prompt.lower() == "clear":
                print("\n" * 50)
                continue
            
            print("\nModel: ", end="", flush=True)
            response = model.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                max_new_tokens=settings.max_new_tokens,
                temperature=settings.temperature,
            )
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()

