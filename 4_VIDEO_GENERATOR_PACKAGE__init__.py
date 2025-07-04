"""
MYTHIQ.AI Video Generator Branch  
Phase 3: Video Generation - Text-to-Video & Animation

This branch handles all video AI capabilities including:
- Text-to-video generation
- Animation creation
- Frame interpolation
- Video style transfer
- Short clip generation

Technologies:
- ModelScope for text-to-video
- RunwayML for advanced generation
- Pika Labs for animation
- FFmpeg for video processing

Version: 3.0
Status: Active
"""

from .controller import video_api

__version__ = "3.0"
__status__ = "active"
__capabilities__ = [
    "text_to_video",
    "animation_creation",
    "frame_interpolation",
    "style_transfer",
    "clip_generation"
]

__all__ = ["video_api"]

