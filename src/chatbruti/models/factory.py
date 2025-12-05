"""Model factory for creating model instances."""

import logging
import importlib
from typing import Type

from ..config import get_settings
from .base import BaseModelInterface

logger = logging.getLogger(__name__)


class ModelFactory:
    """Factory for creating model instances."""
    
    _backends: dict[str, tuple[str, str]] = {
        "huggingface": ("chatbruti.models.huggingface_model", "HuggingFaceModel"),
        "groq": ("chatbruti.models.groq_model", "GroqModel"),
    }
    
    @classmethod
    def _load_backend_class(cls, backend: str) -> Type[BaseModelInterface]:
        """Lazy load backend class."""
        if backend not in cls._backends:
            raise ValueError(
                f"Unknown backend: {backend}. "
                f"Available backends: {list(cls._backends.keys())}"
            )
        
        module_name, class_name = cls._backends[backend]
        module = importlib.import_module(module_name)
        return getattr(module, class_name)
    
    @classmethod
    def create(cls, backend: str = None, settings=None) -> BaseModelInterface:
        """
        Create a model instance based on the backend.
        
        Args:
            backend: Backend name ('huggingface' or 'groq')
            settings: Settings instance (optional)
            
        Returns:
            Model instance
        """
        settings = settings or get_settings()
        backend = backend or settings.backend
        
        model_class = cls._load_backend_class(backend)
        logger.info(f"Creating model with backend: {backend}")
        return model_class(settings=settings)
    
    @classmethod
    def register_backend(cls, name: str, model_class: Type[BaseModelInterface]):
        """Register a new backend."""
        cls._backends[name] = model_class
        logger.info(f"Registered backend: {name}")


def create_model(backend: str = None, settings=None) -> BaseModelInterface:
    """
    Convenience function to create a model instance.
    
    Args:
        backend: Backend name (optional)
        settings: Settings instance (optional)
        
    Returns:
        Model instance
    """
    return ModelFactory.create(backend=backend, settings=settings)

