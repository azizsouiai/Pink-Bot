"""Application settings and configuration."""

import os
from typing import Optional

try:
    from pydantic_settings import BaseSettings
    from pydantic import Field
except ImportError:
    # Fallback for pydantic v1
    from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Model configuration
    model_name: str = Field(
        default="openai/gpt-oss-120b",
        env="MODEL_NAME",
        description="Model name or identifier (varies by backend)"
    )
    
    # Backend selection
    backend: str = Field(
        default="groq",
        env="BACKEND",
        description="Backend to use: 'huggingface' or 'groq'"
    )
    
    # Hugging Face configuration
    device: str = Field(
        default="auto",
        env="DEVICE",
        description="Device to run model on: 'auto', 'cpu', 'cuda', 'mps'"
    )
    torch_dtype: str = Field(
        default="auto",
        env="TORCH_DTYPE",
        description="Torch dtype: 'auto', 'float16', 'bfloat16', 'float32'"
    )
    load_in_8bit: bool = Field(
        default=False,
        env="LOAD_IN_8BIT",
        description="Load model in 8-bit mode (quantization)"
    )
    load_in_4bit: bool = Field(
        default=False,
        env="LOAD_IN_4BIT",
        description="Load model in 4-bit mode (quantization)"
    )
    
    # Groq API configuration
    groq_api_key: Optional[str] = Field(
        default=None,
        env="GROQ_API_KEY",
        description="Groq API key for cloud inference"
    )
    
    # Groq-specific parameters
    reasoning_effort: Optional[str] = Field(
        default="medium",
        env="REASONING_EFFORT",
        description="Reasoning effort for Groq models: 'low', 'medium', or 'high'"
    )
    
    # Generation parameters
    max_new_tokens: int = Field(
        default=8192,
        env="MAX_NEW_TOKENS",
        description="Maximum number of tokens to generate"
    )
    temperature: float = Field(
        default=1.0,
        env="TEMPERATURE",
        description="Sampling temperature"
    )
    top_p: float = Field(
        default=1.0,
        env="TOP_P",
        description="Nucleus sampling parameter"
    )
    top_k: int = Field(
        default=50,
        env="TOP_K",
        description="Top-k sampling parameter"
    )
    do_sample: bool = Field(
        default=True,
        env="DO_SAMPLE",
        description="Whether to use sampling"
    )
    
    # System prompt configuration
    system_prompt_file: Optional[str] = Field(
        default="system_prompt.txt",
        env="SYSTEM_PROMPT_FILE",
        description="Path to the system prompt file"
    )
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings

