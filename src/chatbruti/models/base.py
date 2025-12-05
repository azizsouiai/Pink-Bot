"""Base interface for model implementations."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseModelInterface(ABC):
    """Abstract base class for model interfaces."""
    
    @abstractmethod
    def load(self) -> None:
        """Load the model into memory."""
        pass
    
    @abstractmethod
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
        **kwargs
    ) -> str:
        """
        Generate a response from the model.
        
        Args:
            prompt: Input prompt text
            system_prompt: Optional system prompt to set context/behavior
            conversation_history: Optional list of previous messages for context
            max_new_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            top_k: Top-k sampling parameter
            do_sample: Whether to use sampling
            **kwargs: Additional generation parameters
            
        Returns:
            Generated text response
        """
        pass
    
    @abstractmethod
    def is_loaded(self) -> bool:
        """Check if the model is loaded."""
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        pass

