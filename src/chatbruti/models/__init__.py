"""Model loading and inference module."""

from .base import BaseModelInterface
from .factory import ModelFactory, create_model

# Lazy imports to avoid loading heavy dependencies when not needed
def _lazy_import_huggingface():
    from . import huggingface_model
    return huggingface_model.HuggingFaceModel

def _lazy_import_groq():
    from . import groq_model
    return groq_model.GroqModel

# Export classes for direct import if needed
__all__ = [
    "BaseModelInterface",
    "ModelFactory",
    "create_model",
    "HuggingFaceModel",
    "GroqModel",
]

# Lazy property access
def __getattr__(name):
    if name == "HuggingFaceModel":
        return _lazy_import_huggingface()
    elif name == "GroqModel":
        return _lazy_import_groq()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

