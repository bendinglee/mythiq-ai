"""
MYTHIQ.AI Branches Package
Multi-Branch AI Ecosystem Components

This package contains all AI capability branches for the MYTHIQ.AI platform.
Each branch represents a specialized AI capability that can be dynamically loaded.

Available Branches:
- visual_creator: Image generation and visual processing
- video_generator: Video creation and animation
- knowledge: Enhanced knowledge base and Q&A
- memory_core: Persistent memory and context management

Version: 6.0
Author: MYTHIQ.AI Team
"""

__version__ = "6.0"
__author__ = "MYTHIQ.AI Team"

# Available branch modules
AVAILABLE_BRANCHES = [
    "visual_creator",
    "video_generator", 
    "knowledge",
    "memory_core"
]

def get_available_branches():
    """Return list of available AI branches"""
    return AVAILABLE_BRANCHES

def get_branch_info():
    """Return detailed information about each branch"""
    return {
        "visual_creator": {
            "name": "Visual Creator",
            "description": "AI-powered image generation and visual processing",
            "capabilities": ["image_generation", "style_transfer", "inpainting", "upscaling"],
            "status": "active"
        },
        "video_generator": {
            "name": "Video Generator", 
            "description": "AI-powered video creation and animation",
            "capabilities": ["text_to_video", "animation", "frame_interpolation"],
            "status": "active"
        },
        "knowledge": {
            "name": "Knowledge Base",
            "description": "Enhanced knowledge retrieval and Q&A system",
            "capabilities": ["fact_retrieval", "question_answering", "context_search"],
            "status": "active"
        },
        "memory_core": {
            "name": "Memory Core",
            "description": "Persistent memory and context management",
            "capabilities": ["conversation_memory", "context_retrieval", "learning"],
            "status": "planned"
        }
    }

