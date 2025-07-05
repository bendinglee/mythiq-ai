"""
MYTHIQ.AI Branches Package - Bulletproof Edition
Main plugin discovery and loading system
100% Compatible with main.py Blueprint registration

GITHUB PATH: branches/__init__.py
"""

# Import with error handling for bulletproof loading
try:
    from .visual_creator import visual_api
    VISUAL_IMPORT_SUCCESS = True
    VISUAL_IMPORT_ERROR = None
except ImportError as e:
    visual_api = None
    VISUAL_IMPORT_SUCCESS = False
    VISUAL_IMPORT_ERROR = str(e)

try:
    from .video_generator import video_api
    VIDEO_IMPORT_SUCCESS = True
    VIDEO_IMPORT_ERROR = None
except ImportError as e:
    video_api = None
    VIDEO_IMPORT_SUCCESS = False
    VIDEO_IMPORT_ERROR = str(e)

try:
    from .knowledge import knowledge_api
    KNOWLEDGE_IMPORT_SUCCESS = True
    KNOWLEDGE_IMPORT_ERROR = None
except ImportError as e:
    knowledge_api = None
    KNOWLEDGE_IMPORT_SUCCESS = False
    KNOWLEDGE_IMPORT_ERROR = str(e)

try:
    from .memory_core import memory_api
    MEMORY_IMPORT_SUCCESS = True
    MEMORY_IMPORT_ERROR = None
except ImportError as e:
    memory_api = None
    MEMORY_IMPORT_SUCCESS = False
    MEMORY_IMPORT_ERROR = str(e)

# Metadata for main.py compatibility
__version__ = "6.0-bulletproof"
__package_name__ = "branches"

# Export exactly what main.py expects
__all__ = ["visual_api", "video_api", "knowledge_api", "memory_api"]

# Status for debugging
PLUGIN_STATUS = {
    "visual_creator": {
        "import_success": VISUAL_IMPORT_SUCCESS,
        "import_error": VISUAL_IMPORT_ERROR,
        "api_available": visual_api is not None
    },
    "video_generator": {
        "import_success": VIDEO_IMPORT_SUCCESS,
        "import_error": VIDEO_IMPORT_ERROR,
        "api_available": video_api is not None
    },
    "knowledge": {
        "import_success": KNOWLEDGE_IMPORT_SUCCESS,
        "import_error": KNOWLEDGE_IMPORT_ERROR,
        "api_available": knowledge_api is not None
    },
    "memory_core": {
        "import_success": MEMORY_IMPORT_SUCCESS,
        "import_error": MEMORY_IMPORT_ERROR,
        "api_available": memory_api is not None
    }
}
