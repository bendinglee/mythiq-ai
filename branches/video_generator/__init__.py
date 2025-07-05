"""
MYTHIQ.AI Video Generator Branch - Bulletproof Edition
Phase 3: Video Creation - Text-to-Video Generation & Editing
100% Compatible with main.py Blueprint registration

FILE LOCATION: branches/video_generator/__init__.py
"""

# Import with error handling for bulletproof loading
try:
    from .controller import video_api
    IMPORT_SUCCESS = True
    IMPORT_ERROR = None
except ImportError as e:
    # Fallback for debugging
    video_api = None
    IMPORT_SUCCESS = False
    IMPORT_ERROR = str(e)

# Metadata for main.py compatibility
__version__ = "3.0-bulletproof"
__branch_name__ = "video_generator"
__api_blueprint__ = "video_api"

# Export exactly what main.py expects
__all__ = ["video_api"]

# Status for debugging
STATUS = {
    "import_success": IMPORT_SUCCESS,
    "import_error": IMPORT_ERROR,
    "blueprint_name": __api_blueprint__,
    "version": __version__
}

