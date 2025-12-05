"""Conversation history management."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class ConversationHistory:
    """Manages conversation history for maintaining context."""
    
    def __init__(self, session_id: Optional[str] = None, max_history: int = 20):
        """
        Initialize conversation history.
        
        Args:
            session_id: Unique identifier for this conversation session
            max_history: Maximum number of message pairs to keep in memory
        """
        self.session_id = session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.max_history = max_history
        self.messages: List[Dict[str, str]] = []
        self.history_file: Optional[Path] = None
    
    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to the conversation history.
        
        Args:
            role: Message role ('user', 'assistant', or 'system')
            content: Message content
        """
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only the last max_history message pairs (user + assistant)
        if len(self.messages) > self.max_history * 2:
            # Keep system message if present, then recent messages
            system_msgs = [m for m in self.messages if m["role"] == "system"]
            recent_msgs = self.messages[-self.max_history * 2:]
            self.messages = system_msgs + recent_msgs
    
    def get_messages(self, include_system: bool = True) -> List[Dict[str, str]]:
        """
        Get conversation messages in API format.
        
        Args:
            include_system: Whether to include system messages
            
        Returns:
            List of message dictionaries with 'role' and 'content'
        """
        if include_system:
            return [{"role": msg["role"], "content": msg["content"]} 
                   for msg in self.messages]
        else:
            return [{"role": msg["role"], "content": msg["content"]} 
                   for msg in self.messages if msg["role"] != "system"]
    
    def clear(self) -> None:
        """Clear conversation history (keeps system messages)."""
        system_msgs = [m for m in self.messages if m["role"] == "system"]
        self.messages = system_msgs
    
    def to_dict(self) -> Dict:
        """Convert conversation to dictionary."""
        return {
            "session_id": self.session_id,
            "messages": self.messages,
            "message_count": len(self.messages)
        }
    
    def save_to_file(self, file_path: Optional[str] = None) -> Path:
        """
        Save conversation history to a JSON file.
        
        Args:
            file_path: Path to save the history file
            
        Returns:
            Path to the saved file
        """
        if file_path:
            self.history_file = Path(file_path)
        elif not self.history_file:
            # Default to conversations directory
            conversations_dir = Path("conversations")
            conversations_dir.mkdir(exist_ok=True)
            self.history_file = conversations_dir / f"{self.session_id}.json"
        
        data = {
            "session_id": self.session_id,
            "messages": self.messages,
            "created_at": self.messages[0]["timestamp"] if self.messages else None,
            "updated_at": datetime.now().isoformat()
        }
        
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Conversation saved to {self.history_file}")
        return self.history_file
    
    def load_from_file(self, file_path: str) -> None:
        """
        Load conversation history from a JSON file.
        
        Args:
            file_path: Path to the history file
        """
        history_file = Path(file_path)
        if not history_file.exists():
            raise FileNotFoundError(f"History file not found: {file_path}")
        
        with open(history_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        self.session_id = data.get("session_id", self.session_id)
        self.messages = data.get("messages", [])
        self.history_file = history_file
        
        logger.info(f"Conversation loaded from {history_file}")

