#!/usr/bin/env python3
"""
Startup script for the trading bot application.
This script handles dependency installation and graceful startup.
"""

import os
import sys
import subprocess
import logging
import importlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def install_package(package):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        logger.info(f"Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install {package}: {e}")
        return False

def check_and_install_dependencies():
    """Check for required dependencies and install if missing."""
    required_packages = {
        'flask': 'Flask==2.3.3',
        'flask_sqlalchemy': 'Flask-SQLAlchemy==3.0.5',
        'flask_jwt_extended': 'Flask-JWT-Extended==4.5.2',
        'flask_cors': 'Flask-CORS==4.0.0',
        'psycopg2': 'psycopg2-binary==2.9.7',
        'sqlalchemy': 'SQLAlchemy==2.0.21',
        'requests': 'requests==2.31.0',
        'gunicorn': 'gunicorn==21.2.0'
    }
    
    missing_packages = []
    
    for module_name, package_spec in required_packages.items():
        try:
            importlib.import_module(module_name)
            logger.info(f"✓ {module_name} is available")
        except ImportError:
            logger.warning(f"✗ {module_name} is missing")
            missing_packages.append(package_spec)
    
    if missing_packages:
        logger.info(f"Installing {len(missing_packages)} missing packages...")
        for package in missing_packages:
            install_package(package)
    else:
        logger.info("All required packages are available")

def start_application():
    """Start the Flask application."""
    try:
        # Try to import the main application
        from wsgi import application
        logger.info("Application imported successfully")
        return application
    except ImportError as e:
        logger.error(f"Failed to import application: {e}")
        # Create a minimal Flask app as fallback
        from flask import Flask
        app = Flask(__name__)
        
        @app.route('/')
        def health():
            return {'status': 'minimal', 'message': 'Application running in minimal mode'}
        
        logger.info("Running in minimal mode")
        return app

if __name__ == '__main__':
    logger.info("Starting Trading Bot Application...")
    
    # Check and install dependencies
    check_and_install_dependencies()
    
    # Start the application
    app = start_application()
    
    # Run the application
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)