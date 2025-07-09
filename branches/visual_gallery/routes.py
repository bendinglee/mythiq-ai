from flask import Blueprint
from .controller import render_gallery_html, api_gallery_json

gallery_api = Blueprint("visual_gallery", __name__)

@gallery_api.route("/gallery", methods=["GET"])
def gallery_view(): return render_gallery_html()

@gallery_api.route("/api/gallery", methods=["GET"])
def gallery_json(): return api_gallery_json()
