"""
WSGI configuration for presensi_mts project on PythonAnywhere.

This file is specifically configured for PythonAnywhere hosting.
Replace 'yourusername' with your actual PythonAnywhere username.
"""

import os
import sys

# Add your project directory to the Python path
# Replace 'yourusername' with your actual PythonAnywhere username
path = '/home/yourusername/presensi_mts'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'presensi_mts.settings'

# Set production environment variables
os.environ['SECRET_KEY'] = 'your-secret-key-here'  # Replace with your actual secret key
os.environ['DEBUG'] = 'False'
os.environ['PYTHONANYWHERE_DOMAIN'] = 'yourusername.pythonanywhere.com'  # Replace with your domain

# Import Django and get the WSGI application
try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except Exception as e:
    # Log the error for debugging
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.error(f"Failed to load WSGI application: {e}")
    raise 