"""System prompt loading utilities."""

import os
import logging
from pathlib import Path
from typing import Optional

from ..config import get_settings

logger = logging.getLogger(__name__)

# Cache for system prompt
_system_prompt_cache: Optional[str] = None


def load_system_prompt(file_path: Optional[str] = None) -> Optional[str]:
    """
    Load system prompt from file.
    
    Args:
        file_path: Path to system prompt file. If None, uses settings default.
        
    Returns:
        System prompt text or None if file doesn't exist
    """
    global _system_prompt_cache
    
    settings = get_settings()
    prompt_file = file_path or settings.system_prompt_file
    
    # Try to resolve the file path
    # First, try as absolute path
    if os.path.isabs(prompt_file):
        full_path = Path(prompt_file)
    else:
        # Try relative to project root (where .env file is)
        # Look for .env file to find project root
        current_dir = Path.cwd()
        project_root = current_dir
        
        # Check if we're in the project directory
        if (current_dir / ".env").exists() or (current_dir / "system_prompt.txt").exists():
            project_root = current_dir
        else:
            # Try parent directories
            for parent in current_dir.parents:
                if (parent / ".env").exists() or (parent / "system_prompt.txt").exists():
                    project_root = parent
                    break
        
        full_path = project_root / prompt_file
    
    if not full_path.exists():
        logger.warning(f"System prompt file not found: {full_path}")
        return None
    
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            prompt = f.read().strip()
        
        if prompt:
            _system_prompt_cache = prompt
            logger.info(f"Loaded system prompt from: {full_path}")
            return prompt
        else:
            logger.warning(f"System prompt file is empty: {full_path}")
            return None
            
    except Exception as e:
        logger.error(f"Error loading system prompt from {full_path}: {e}")
        return None


def get_system_prompt(reload: bool = False) -> Optional[str]:
    """
    Get system prompt, using cache if available.
    
    Args:
        reload: Force reload from file instead of using cache
        
    Returns:
        System prompt text or None
    """
    global _system_prompt_cache
    
    if reload or _system_prompt_cache is None:
        return load_system_prompt()
    
    return _system_prompt_cache

