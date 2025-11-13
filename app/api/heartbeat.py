from flask import Blueprint, jsonify

heartbeat_bp = Blueprint("heartbeat", __name__)


@heartbeat_bp.route("/", methods=["GET", "OPTIONS"])
def health_check():
    return (
        jsonify(
            {"status": "ok", "message": "Server is running", "timestamp": "2025-11-13"}
        ),
        200,
    )
