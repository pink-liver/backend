from flask import Blueprint

heartbeat_bp = Blueprint("heartbeat", __name__)


@heartbeat_bp.route("/", methods=["GET"])
def health_check():
    return "alive", 200
