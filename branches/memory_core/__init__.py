"""
MYTHIQ.AI Memory Core Branch - Bulletproof Edition
Phase 4: Memory & Learning - Conversation Memory & User Learning
100% Compatible with main.py Blueprint registration

FILE LOCATION: branches/memory_core/__init__.py
"""

# Import with error handling for bulletproof loading
try:
    from .controller import memory_api
    IMPORT_SUCCESS = True
    IMPORT_ERROR = None
except ImportError as e:
    # Fallback for debugging
    memory_api = None
    IMPORT_SUCCESS = False
    IMPORT_ERROR = str(e)

# Metadata for main.py compatibility
__version__ = "4.0-bulletproof"
__branch_name__ = "memory_core"
__api_blueprint__ = "memory_api"

# Export exactly what main.py expects
__all__ = ["memory_api"]

# Status for debugging
STATUS = {
    "import_success": IMPORT_SUCCESS,
    "import_error": IMPORT_ERROR,
    "blueprint_name": __api_blueprint__,
    "version": __version__
}

