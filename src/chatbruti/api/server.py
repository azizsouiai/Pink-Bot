"""FastAPI server for Chatbruti API."""

import logging
import uuid
from typing import Dict, List, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from ..config import get_settings
from ..models import create_model
from ..utils import get_system_prompt, ConversationHistory

logger = logging.getLogger(__name__)

# Global model instance
_model = None
_system_prompt = None
_conversations: Dict[str, ConversationHistory] = {}


def get_model():
    """Get or initialize the model."""
    global _model
    if _model is None:
        settings = get_settings()
        logger.info(f"Initializing model with backend: {settings.backend}")
        _model = create_model(backend=settings.backend, settings=settings)
        _model.load()
        logger.info("Model loaded successfully")
    return _model


def get_system_prompt_cached():
    """Get or load system prompt."""
    global _system_prompt
    if _system_prompt is None:
        _system_prompt = get_system_prompt()
    return _system_prompt


# Pydantic models for request/response
class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., description="User message")
    session_id: Optional[str] = Field(None, description="Conversation session ID")
    temperature: Optional[float] = Field(None, description="Sampling temperature")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens to generate")
    stream: bool = Field(False, description="Whether to stream the response")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str = Field(..., description="Model response")
    session_id: str = Field(..., description="Conversation session ID")
    message_count: int = Field(..., description="Number of messages in conversation")


class ConversationResponse(BaseModel):
    """Response model for conversation endpoint."""
    session_id: str
    messages: List[Dict[str, str]]
    message_count: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    backend: str
    model_name: str
    timestamp: str


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="Chatbruti API",
        description="REST API for Chatbruti LLM chatbot",
        version="0.1.0",
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify allowed origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/", tags=["General"])
    async def root():
        """Root endpoint."""
        return {
            "message": "Chatbruti API",
            "version": "0.1.0",
            "docs": "/docs",
            "health": "/health"
        }
    
    @app.get("/health", response_model=HealthResponse, tags=["General"])
    async def health_check():
        """Health check endpoint."""
        try:
            model = get_model()
            info = model.get_model_info()
            return HealthResponse(
                status="healthy",
                backend=info.get("backend", "unknown"),
                model_name=info.get("model_name", "unknown"),
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Service unavailable: {str(e)}"
            )
    
    @app.post("/chat", response_model=ChatResponse, tags=["Chat"])
    async def chat(request: ChatRequest):
        """
        Send a message and get a response from the model.
        
        Maintains conversation history using session_id.
        """
        try:
            model = get_model()
            system_prompt = get_system_prompt_cached()
            
            # Get or create conversation session
            session_id = request.session_id or str(uuid.uuid4())
            if session_id not in _conversations:
                _conversations[session_id] = ConversationHistory(session_id=session_id)
                if system_prompt:
                    _conversations[session_id].add_message("system", system_prompt)
            
            conversation = _conversations[session_id]
            
            # Add user message to history
            conversation.add_message("user", request.message)
            
            # Get conversation history for context
            history = conversation.get_messages(include_system=False)
            
            # Generate response
            response = model.generate(
                prompt=request.message,
                system_prompt=system_prompt,
                conversation_history=history,
                temperature=request.temperature,
                max_new_tokens=request.max_tokens,
                stream=request.stream,
            )
            
            # Add assistant response to history
            conversation.add_message("assistant", response)
            
            return ChatResponse(
                response=response,
                session_id=session_id,
                message_count=len(conversation.messages)
            )
            
        except Exception as e:
            logger.error(f"Error in chat endpoint: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error generating response: {str(e)}"
            )
    
    @app.get("/conversations/{session_id}", response_model=ConversationResponse, tags=["Conversations"])
    async def get_conversation(session_id: str):
        """Get conversation history for a session."""
        if session_id not in _conversations:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversation session not found: {session_id}"
            )
        
        conversation = _conversations[session_id]
        conv_dict = conversation.to_dict()
        
        return ConversationResponse(
            session_id=conv_dict["session_id"],
            messages=conv_dict["messages"],
            message_count=conv_dict["message_count"],
            created_at=conv_dict["messages"][0]["timestamp"] if conv_dict["messages"] else None,
            updated_at=conv_dict["messages"][-1]["timestamp"] if conv_dict["messages"] else None,
        )
    
    @app.delete("/conversations/{session_id}", tags=["Conversations"])
    async def delete_conversation(session_id: str):
        """Delete a conversation session."""
        if session_id not in _conversations:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversation session not found: {session_id}"
            )
        
        del _conversations[session_id]
        return {"message": f"Conversation {session_id} deleted"}
    
    @app.post("/conversations/{session_id}/clear", tags=["Conversations"])
    async def clear_conversation(session_id: str):
        """Clear conversation history (keeps system prompt)."""
        if session_id not in _conversations:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversation session not found: {session_id}"
            )
        
        conversation = _conversations[session_id]
        conversation.clear()
        
        # Re-add system prompt if available
        system_prompt = get_system_prompt_cached()
        if system_prompt:
            conversation.add_message("system", system_prompt)
        
        return {"message": f"Conversation {session_id} cleared", "session_id": session_id}
    
    @app.get("/conversations", tags=["Conversations"])
    async def list_conversations():
        """List all active conversation sessions."""
        return {
            "sessions": [
                {
                    "session_id": session_id,
                    "message_count": len(conv.messages),
                    "created_at": conv.messages[0]["timestamp"] if conv.messages else None,
                }
                for session_id, conv in _conversations.items()
            ],
            "total": len(_conversations)
        }
    
    return app


# Create the app instance
app = create_app()

