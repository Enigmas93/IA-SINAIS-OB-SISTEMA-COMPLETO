#!/usr/bin/env python3
"""
WSGI entry point for the trading bot application.
"""

import os
import sys
import logging

# Add current directory to Python path
base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_path)

# Application is now in project root - no need for src path

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    # Import the main application
    from app import app as application
    
    # Templates and static files are now in project root
    logger.info(f"Application imported successfully from project root")
    logger.info(f"Template folder: {application.template_folder}")
    logger.info(f"Static folder: {application.static_folder}")
    
    logger.info("Main application imported successfully")
except Exception as e:
    logger.error(f"Failed to import main application: {e}")
    # Create a minimal fallback app
    from flask import Flask
    app = Flask(
    __name__,
    template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates")),
    static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))
    )

    
    @application.route('/')
    def fallback():
        return {'error': 'Application failed to start', 'message': str(e)}

# For compatibility
app = application

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    application.run(host='0.0.0.0', port=port, debug=False)