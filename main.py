#!/usr/bin/env python3
"""
🚀 MYTHIQ.AI - Railway Deployment Entry Point
The Ultimate Self-Learning AI Empire
"""

import os
import sys
import logging
from mythiq_ai_backend import app, socketio

# Configure logging for Railway
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Main entry point for Railway deployment"""
    
    # Get port from environment (Railway sets this automatically)
    port = int(os.environ.get("PORT", 5000))
    
    logger.info("🚀 Starting MYTHIQ.AI on Railway...")
    logger.info(f"📡 Port: {port}")
    logger.info("🧠 Self-learning AI system initializing...")
    
    try:
        # Start the MYTHIQ.AI system
        socketio.run(
            app, 
            host='0.0.0.0', 
            port=port, 
            debug=False,  # Disable debug in production
            allow_unsafe_werkzeug=True,
            log_output=True
        )
    except Exception as e:
        logger.error(f"❌ Failed to start MYTHIQ.AI: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

