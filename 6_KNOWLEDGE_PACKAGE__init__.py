"""
MYTHIQ.AI Knowledge Branch - Bulletproof Edition
Enhanced Knowledge Base with Advanced AI Capabilities
100% Compatible with main.py Blueprint registration

FILE LOCATION: branches/knowledge/__init__.py
"""

# Import with error handling for bulletproof loading
try:
    from .controller import knowledge_api
    IMPORT_SUCCESS = True
    IMPORT_ERROR = None
except ImportError as e:
    # Fallback for debugging
    knowledge_api = None
    IMPORT_SUCCESS = False
    IMPORT_ERROR = str(e)

# Metadata for main.py compatibility
__version__ = "4.0-bulletproof"
__branch_name__ = "knowledge"
__api_blueprint__ = "knowledge_api"

# Export exactly what main.py expects
__all__ = ["knowledge_api"]

# Status for debugging
STATUS = {
    "import_success": IMPORT_SUCCESS,
    "import_error": IMPORT_ERROR,
    "blueprint_name": __api_blueprint__,
    "version": __version__
}

