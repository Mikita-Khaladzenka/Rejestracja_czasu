from flask import Blueprint, send_from_directory

from config import Config



frontend_bp = Blueprint(
    "frontend",
    __name__
)



@frontend_bp.route("/")
def index():

    return send_from_directory(
        Config.FRONTEND,
        "index.html"
    )



@frontend_bp.route("/<path:path>")
def static_files(path):

    return send_from_directory(
        Config.FRONTEND,
        path
    )
