"""API server entry point."""

import logging
import uvicorn
import os
from chatbruti.config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    """Run the API server."""
    settings = get_settings()
    
    # Get host and port from environment or use defaults
    host = os.getenv("API_HOST", "0.0.0.0")  # Listen on all interfaces
    port = int(os.getenv("API_PORT", "8000"))
    
    logger.info(f"Starting Chatbruti API server on http://{host}:{port}")
    logger.info(f"API documentation available at http://{host}:{port}/docs")
    logger.info(f"Using backend: {settings.backend}")
    
    uvicorn.run(
        "chatbruti.api.server:app",
        host=host,
        port=port,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )


if __name__ == "__main__":
    main()

