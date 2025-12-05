"""Groq API model implementation."""

import logging
from typing import Dict, Any, Optional

try:
    from groq import Groq
except ImportError:
    Groq = None

from ..config import get_settings
from .base import BaseModelInterface

logger = logging.getLogger(__name__)


class GroqModel(BaseModelInterface):
    """Groq API model implementation for cloud inference."""
    
    def __init__(self, settings=None):
        """Initialize the Groq API model."""
        self.settings = settings or get_settings()
        self.client = None
        
        if Groq is None:
            raise ImportError(
                "groq package is required for Groq backend. "
                "Install it with: pip install groq"
            )
    
    def load(self) -> None:
        """Initialize the API client."""
        if self.is_loaded():
            logger.info("API client already initialized")
            return
        
        api_key = self.settings.groq_api_key
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY environment variable is required for Groq backend"
            )
        
        logger.info("Initializing Groq API client...")
        try:
            self.client = Groq(api_key=api_key)
            logger.info("API client initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing API client: {e}")
            raise
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        conversation_history: Optional[list] = None,
        max_new_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        do_sample: Optional[bool] = None,
        stream: bool = False,
        **kwargs
    ) -> str:
        """Generate a response using Groq API."""
        if not self.is_loaded():
            raise RuntimeError("API client not initialized. Call load() first.")
        
        # Use settings defaults if not provided
        max_completion_tokens = max_new_tokens or self.settings.max_new_tokens
        temperature = temperature or self.settings.temperature
        top_p = top_p or self.settings.top_p
        reasoning_effort = kwargs.get("reasoning_effort", self.settings.reasoning_effort)
        
        # Format messages for Groq API
        messages = []
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add system prompt if provided (only if not already in history)
        if system_prompt and not any(msg.get("role") == "system" for msg in messages):
            messages.append({"role": "system", "content": system_prompt})
        
        # Add current user prompt
        messages.append({"role": "user", "content": prompt})
        
        try:
            # Prepare API call parameters
            api_params = {
                "model": self.settings.model_name,
                "messages": messages,
                "temperature": temperature,
                "max_completion_tokens": max_completion_tokens,
                "top_p": top_p,
                "stream": stream,
            }
            
            # Add reasoning_effort if specified (for reasoning models)
            if reasoning_effort:
                api_params["reasoning_effort"] = reasoning_effort
            
            # Add stop sequences if provided
            if "stop" in kwargs and kwargs["stop"] is not None:
                api_params["stop"] = kwargs["stop"]
            
            # Call the API
            completion = self.client.chat.completions.create(**api_params)
            
            # Handle streaming response
            if stream:
                generated_text = ""
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        generated_text += chunk.choices[0].delta.content
                return generated_text.strip()
            else:
                # Non-streaming response
                generated_text = completion.choices[0].message.content
                return generated_text.strip()
            
        except Exception as e:
            logger.error(f"Error during API generation: {e}")
            raise
    
    def is_loaded(self) -> bool:
        """Check if the API client is initialized."""
        return self.client is not None
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the API configuration."""
        return {
            "status": "initialized" if self.is_loaded() else "not_initialized",
            "backend": "groq",
            "model_name": self.settings.model_name,
            "has_api_key": bool(self.settings.groq_api_key),
            "reasoning_effort": self.settings.reasoning_effort,
        }

