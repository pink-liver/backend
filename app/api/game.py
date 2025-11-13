from flask import Blueprint, request, jsonify
from app.caches.games_cache import get_game_cache
from datetime import datetime

game_bp = Blueprint("game", __name__)

# Get the global cache instance
cache = get_game_cache()


@game_bp.route("/list", methods=["GET", "OPTIONS"])
def get_games():
    """取得所有遊戲列表"""
    try:
        games = cache.get_all_games()
        return (
            jsonify({"status": "success", "data": list(games), "count": len(games)}),
            200,
        )
    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"Failed to get games: {str(e)}"}),
            500,
        )


@game_bp.route("/<game_id>/ranks", methods=["GET", "OPTIONS"])
def get_ranks(game_id):
    """取得指定遊戲的排行榜"""
    try:
        order = request.args.get("order", "desc")
        limit = request.args.get("limit", 10, type=int)
        rankings = cache.get_game_rankings(game_id)

        # Sort rankings by score
        sort_descending = order.lower() != "asc"
        rankings.sort(key=lambda x: float(x["score"]), reverse=sort_descending)

        # apply limit
        if limit > 0:
            rankings = rankings[:limit]

        # parse rankings to add timeStr (only for debugging purposes)
        parsed_rankings = []
        for entry in rankings:
            parsed_entry = entry.copy()
            parsed_entry["timeStr"] = datetime.fromtimestamp(entry["time"]).isoformat()
            parsed_rankings.append(parsed_entry)

        return (
            jsonify(
                {
                    "status": "success",
                    "data": parsed_rankings,
                    "count": len(parsed_rankings),
                    "game_id": game_id,
                }
            ),
            200,
        )
    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": f"Failed to get rankings: {str(e)}"}
            ),
            500,
        )


@game_bp.route("/<game_id>/rank", methods=["GET", "POST", "OPTIONS"])
def add_rank(game_id):
    """新增排行紀錄"""
    try:
        if request.method == "POST":
            data = request.get_json()
            name = data.get("name", "Guest")
            score = data.get("score")
        else:
            name = request.args.get("name", "Guest")
            score = request.args.get("score", type=int)

        if not name or score is None:
            return (
                jsonify({"status": "error", "message": "Name and score are required"}),
                400,
            )

        success = cache.add_rank_entry(game_id, name, score)

        if success:
            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "Rank added successfully",
                        "data": {"game_id": game_id, "name": name, "score": score},
                    }
                ),
                200,
            )
        else:
            return (
                jsonify({"status": "error", "message": "Failed to add rank entry"}),
                500,
            )

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"Failed to add rank: {str(e)}"}),
            500,
        )


@game_bp.route("/<game_id>/clear", methods=["DELETE", "OPTIONS"])
def clear_game_rankings(game_id):
    """清除指定遊戲的排行榜"""
    try:
        success = cache.clear_game_rankings(game_id)
        if success:
            return (
                jsonify(
                    {
                        "status": "success",
                        "message": f"Rankings cleared for game {game_id}",
                        "game_id": game_id,
                    }
                ),
                200,
            )
        else:
            return (
                jsonify(
                    {"status": "error", "message": f"No data found for game {game_id}"}
                ),
                404,
            )
    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": f"Failed to clear rankings: {str(e)}"}
            ),
            500,
        )


@game_bp.route("/stats", methods=["GET", "OPTIONS"])
def get_cache_stats():
    """取得統計資料"""
    try:
        all_games = cache.get_all_games()

        stats = {
            "total_games": cache.get_game_count(),
            "total_rankings": sum(cache.get_rank_count(game) for game in all_games),
            "rank_counts": {game: cache.get_rank_count(game) for game in all_games},
        }

        return jsonify({"status": "success", "data": stats}), 200
    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": f"Failed to get cache stats: {str(e)}"}
            ),
            500,
        )
