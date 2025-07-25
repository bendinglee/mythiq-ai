#!/usr/bin/env python3
"""
Mythiq: Full-Stack AI System
Main entry point for the Mythiq platform
"""

import os
import sys
import logging
from datetime import datetime

# Add project root to Python path
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

# Import configuration
from config import get_config

# Import core modules
from core.memory import MemoryManager
from core.diagnostics import DiagnosticsManager
from core.fallback import FallbackManager

# Import API blueprints
from api.chat import chat_bp
from api.generate import generate_bp
from api.feedback import feedback_bp
from api.status import status_bp

def create_app(config_name=None):
    """Create and configure the Flask application"""
    app = Flask(__name__, static_folder='ui/dist')
    
    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    # Enable CORS for all routes
    if app.config['ENABLE_CORS']:
        CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Set up logging
    logging.basicConfig(
        level=getattr(logging, app.config['LOG_LEVEL']),
        format=app.config['LOG_FORMAT'],
        handlers=[
            logging.FileHandler(os.path.join(app.config['LOGS_DIR'], 'mythiq.log')),
            logging.StreamHandler()
        ]
    )
    
    # Ensure data directories exist
    os.makedirs(app.config['DATA_DIR'], exist_ok=True)
    os.makedirs(app.config['LOGS_DIR'], exist_ok=True)
    os.makedirs(app.config['FEEDBACK_DIR'], exist_ok=True)
    
    # Initialize core managers
    app.memory_manager = MemoryManager(app.config['DATA_DIR'])
    app.diagnostics_manager = DiagnosticsManager()
    app.fallback_manager = FallbackManager()
    
    # Register API blueprints
    app.register_blueprint(chat_bp, url_prefix='/api')
    app.register_blueprint(generate_bp, url_prefix='/api')
    app.register_blueprint(feedback_bp, url_prefix='/api')
    app.register_blueprint(status_bp, url_prefix='/api')
    
    # Serve frontend
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        """Serve the frontend application"""
        static_folder_path = app.static_folder
        if static_folder_path is None:
            return jsonify({"error": "Frontend not configured"}), 404
            
        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                return jsonify({
                    "message": "Mythiq AI Platform",
                    "version": "1.0.0",
                    "status": "running",
                    "timestamp": datetime.now().isoformat()
                })
    
    return app

if __name__ == '__main__':
    config_name = os.environ.get('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    print("🌐 Starting Mythiq AI Platform...")
    print("🧠 Initializing core modules...")
    print("🎨 Loading creative generation engines...")
    print("💝 Activating emotional intelligence...")
    print(f"🚀 Server ready at http://{app.config['HOST']}:{app.config['PORT']}")
    
    app.run(
        host=app.config['HOST'], 
        port=app.config['PORT'], 
        debug=app.config['DEBUG']
    )

