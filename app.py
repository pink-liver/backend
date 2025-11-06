from flask import Flask, jsonify, request
import datetime


app = Flask(__name__)


@app.route("/")
def health_check():
    return "alive", 200


@app.route("/rank")
def greet():
    game = request.args.get("game")
    name = request.args.get("name", "Guest")
    score = request.args.get("score")
    return "OK", 200


@app.route("/ranks", methods=["GET"])
def get_ranks():
    game = request.args.get("game")
    return (
        jsonify(
            [
                {"name": "Guest", "score": 100, "time": "2025-11-06T12:00:00"},
                {"name": "Player1", "score": 90, "time": "2025-11-06T12:05:00"},
            ]
        ),
        200,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
