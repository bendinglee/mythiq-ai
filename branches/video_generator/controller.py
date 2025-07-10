from branches.video_generator.multimodal_synth import synthesize_scene
from branches.video_generator.video_exporter import export_video

def generate_video_clip(prompt, style="cinematic", duration=5):
    scene = synthesize_scene(prompt, style, duration)
    video_path = export_video(scene)
    return {
        "success": True,
        "video_url": video_path,
        "style": style,
        "duration": duration
    }
