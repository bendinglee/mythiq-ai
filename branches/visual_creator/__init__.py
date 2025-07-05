"""
MYTHIQ.AI Visual Creator Branch - Bulletproof Edition
Phase 2: Visual Intelligence - Image Generation & Editing
100% Compatible with main.py Blueprint registration

FILE LOCATION: branches/visual_creator/__init__.py
"""

# Import with error handling for bulletproof loading
try:
    from .controller import visual_api
    IMPORT_SUCCESS = True
    IMPORT_ERROR = None
except ImportError as e:
    # Fallback for debugging
    visual_api = None
    IMPORT_SUCCESS = False
    IMPORT_ERROR = str(e)

# Metadata for main.py compatibility
__version__ = "2.0-bulletproof"
__branch_name__ = "visual_creator"
__api_blueprint__ = "visual_api"

# Export exactly what main.py expects
__all__ = ["visual_api"]

# Status for debugging
STATUS = {
    "import_success": IMPORT_SUCCESS,
    "import_error": IMPORT_ERROR,
    "blueprint_name": __api_blueprint__,
    "version": __version__
}
