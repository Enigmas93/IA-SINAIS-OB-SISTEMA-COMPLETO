#!/usr/bin/env python3
"""
Startup check script for Render deployment
This script verifies that all critical components are working
"""

import sys
import os
import logging

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_imports():
    """Check if critical imports work"""
    try:
        from flask import Flask
        logger.info("✓ Flask import successful")
    except ImportError as e:
        logger.error(f"✗ Flask import failed: {e}")
        return False
    
    try:
        from database import db
        logger.info("✓ Database import successful")
    except ImportError as e:
        logger.error(f"✗ Database import failed: {e}")
        return False
    
    try:
        from models import User
        logger.info("✓ Models import successful")
    except ImportError as e:
        logger.error(f"✗ Models import failed: {e}")
        return False
    
    try:
        from services import IQOptionService
        logger.info("✓ Services import successful (with fallback)")
    except ImportError as e:
        logger.warning(f"⚠ Services import failed, using fallback: {e}")
    
    return True

def check_app_creation():
    """Check if app can be created"""
    try:
        from app import app
        logger.info("✓ App creation successful")
        return True
    except Exception as e:
        logger.error(f"✗ App creation failed: {e}")
        return False

def main():
    """Main startup check"""
    logger.info("Starting deployment checks...")
    
    if not check_imports():
        logger.error("Critical import checks failed")
        sys.exit(1)
    
    if not check_app_creation():
        logger.error("App creation failed")
        sys.exit(1)
    
    logger.info("✓ All startup checks passed!")
    return True

if __name__ == "__main__":
    main()