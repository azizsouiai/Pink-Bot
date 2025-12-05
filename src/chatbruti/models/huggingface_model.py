"""Hugging Face model implementation."""

import logging
from typing import Dict, Any, Optional
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    pipeline
)

from ..config import get_settings
from .base import BaseModelInterface

logger = logging.getLogger(__name__)


class HuggingFaceModel(BaseModelInterface):
    """Hugging Face model implementation for local inference."""
    
    def __init__(self, settings=None):
        """Initialize the Hugging Face model."""
        self.settings = settings or get_settings()
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self._device = None
        self._torch_dtype = None
        
    def _determine_device(self) -> str:
        """Determine the best device to use."""
        if self.settings.device != "auto":
            return self.settings.device
        
        if torch.cuda.is_available():
            return "cuda"
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"
    
    def _determine_dtype(self) -> torch.dtype:
        """Determine the best dtype to use."""
        if self.settings.torch_dtype != "auto":
            dtype_map = {
                "float16": torch.float16,
                "bfloat16": torch.bfloat16,
                "float32": torch.float32,
            }
            return dtype_map.get(self.settings.torch_dtype, torch.float32)
        
        device = self._determine_device()
        if device == "cuda":
            return torch.float16
        elif device == "mps":
            return torch.float32
        else:
            return torch.float32
    
    def _create_quantization_config(self) -> Optional[BitsAndBytesConfig]:
        """Create quantization config if needed."""
        if self.settings.load_in_8bit:
            return BitsAndBytesConfig(
                load_in_8bit=True,
            )
        elif self.settings.load_in_4bit:
            return BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
            )
        return None
    
    def load(self) -> None:
        """Load the model and tokenizer."""
        if self.is_loaded():
            logger.info("Model already loaded")
            return
        
        logger.info(f"Loading model: {self.settings.model_name}")
        logger.info(f"Device: {self._determine_device()}")
        logger.info(f"Dtype: {self._determine_dtype()}")
        
        try:
            # Load tokenizer
            logger.info("Loading tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.settings.model_name,
                trust_remote_code=True,
            )
            
            # Set pad token if not set
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Prepare model loading kwargs
            model_kwargs = {
                "trust_remote_code": True,
            }
            
            # Add quantization config if needed
            quantization_config = self._create_quantization_config()
            if quantization_config:
                model_kwargs["quantization_config"] = quantization_config
                logger.info(f"Using quantization: {quantization_config}")
            
            # Add device map for multi-GPU or CPU
            device = self._determine_device()
            if device == "cuda" and not quantization_config:
                model_kwargs["device_map"] = "auto"
                model_kwargs["torch_dtype"] = self._determine_dtype()
            elif device == "mps":
                model_kwargs["torch_dtype"] = self._determine_dtype()
            
            # Load model
            logger.info("Loading model...")
            self.model = AutoModelForCausalLM.from_pretrained(
                self.settings.model_name,
                **model_kwargs
            )
            
            # Move to device if not using device_map
            if device != "cuda" or quantization_config:
                self.model = self.model.to(device)
            
            self._device = device
            self._torch_dtype = self._determine_dtype()
            
            # Create pipeline for easier generation
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if device == "cuda" else -1,
            )
            
            logger.info("Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
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
        **kwargs
    ) -> str:
        """Generate a response from the model."""
        if not self.is_loaded():
            raise RuntimeError("Model not loaded. Call load() first.")
        
        # Use settings defaults if not provided
        max_new_tokens = max_new_tokens or self.settings.max_new_tokens
        temperature = temperature or self.settings.temperature
        top_p = top_p or self.settings.top_p
        top_k = top_k or self.settings.top_k
        do_sample = do_sample if do_sample is not None else self.settings.do_sample
        
        # Build full prompt with conversation history
        full_prompt_parts = []
        
        # Add conversation history if provided
        if conversation_history:
            for msg in conversation_history:
                if msg.get("role") == "user":
                    full_prompt_parts.append(f"User: {msg.get('content', '')}")
                elif msg.get("role") == "assistant":
                    full_prompt_parts.append(f"Assistant: {msg.get('content', '')}")
        
        # Add current prompt
        full_prompt_parts.append(f"User: {prompt}")
        
        # Combine all parts
        combined_prompt = "\n".join(full_prompt_parts)
        
        # Format prompt for Mistral Instruct (include system prompt if provided)
        if system_prompt:
            formatted_prompt = self._format_prompt_with_system(system_prompt, combined_prompt)
        else:
            formatted_prompt = self._format_prompt(combined_prompt)
        
        try:
            # Generate using pipeline
            outputs = self.pipeline(
                formatted_prompt,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                do_sample=do_sample,
                return_full_text=False,
                **kwargs
            )
            
            # Extract generated text
            generated_text = outputs[0]["generated_text"]
            return generated_text.strip()
            
        except Exception as e:
            logger.error(f"Error during generation: {e}")
            raise
    
    def _format_prompt(self, prompt: str) -> str:
        """Format prompt for Mistral Instruct model."""
        # Mistral Instruct uses a specific format
        return f"<s>[INST] {prompt} [/INST]"
    
    def _format_prompt_with_system(self, system_prompt: str, user_prompt: str) -> str:
        """Format prompt with system message for Mistral Instruct model."""
        # Mistral Instruct format with system prompt
        return f"<s>[INST] {system_prompt}\n\n{user_prompt} [/INST]"
    
    def is_loaded(self) -> bool:
        """Check if the model is loaded."""
        return self.model is not None and self.tokenizer is not None
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        if not self.is_loaded():
            return {"status": "not_loaded"}
        
        return {
            "status": "loaded",
            "model_name": self.settings.model_name,
            "device": self._device,
            "dtype": str(self._torch_dtype),
            "quantization": {
                "8bit": self.settings.load_in_8bit,
                "4bit": self.settings.load_in_4bit,
            },
        }

