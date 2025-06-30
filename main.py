#!/usr/bin/env python3
"""
MYTHIQ.AI Railway Deployment Entry Point
Starts the complete AI system on Railway cloud platform
"""

import os
import sys
import logging

# Configure logging for Railway
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Main entry point for Railway deployment"""
    try:
        logger.info("🚀 Starting MYTHIQ.AI on Railway...")
        
        # Import and start the main application
        from mythiq_ai_backend import app, socketio
        
        # Get port from Railway environment
        port = int(os.environ.get("PORT", 5000))
        
        logger.info(f"📡 Starting server on port {port}")
        logger.info("🌐 MYTHIQ.AI will be accessible via Railway URL")
        
        # Start the application
        socketio.run(
            app, 
            host='0.0.0.0', 
            port=port, 
            debug=False,
            allow_unsafe_werkzeug=True
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to start MYTHIQ.AI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

