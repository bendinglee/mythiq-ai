from flask import Blueprint
from .controller import synthesize_image_route

image_api = Blueprint("image_synth", __name__)

@image_api.route("/api/synthesize-image", methods=["POST"])
def synth_image(): return synthesize_image_route()
