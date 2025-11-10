from flask import Blueprint, request, jsonify
from app.caches.games_cache import get_game_cache

game_bp = Blueprint("game", __name__)

# Get the global cache instance
cache = get_game_cache()


@game_bp.route("list", methods=["GET"])
def get_games():
    return jsonify(list(cache.get_all_games())), 200


@game_bp.route("/<game_id>/ranks", methods=["GET"])
def get_ranks(game_id):
    order = request.args.get("order", "desc")
    sort_descending = order.lower() != "asc"
    rankings = cache.get_game_rankings(game_id, sort_descending)
    return jsonify(rankings), 200


@game_bp.route("/<game_id>/rank")
def greet(game_id):
    name = request.args.get("name", "Guest")
    score = request.args.get("score")
    cache.add_rank_entry(game_id, name, score)
    return "OK", 200


@game_bp.route("/<game_id>/clear")
def clear_game_rankings(game_id):
    success = cache.clear_game_rankings(game_id)
    if success:
        return "Cleared", 200
    else:
        return "No Data Found", 404


@game_bp.route("/stats", methods=["GET"])
def get_cache_stats():
    try:
        stats = {
            "total_games": cache.get_game_count(),
            "total_rankings": sum(
                cache.get_rank_count(game) for game in cache.get_all_games()
            ),
            "rank_counts": {
                game: cache.get_rank_count(game) for game in cache.get_all_games()
            },
        }
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": f"Failed to get cache stats: {str(e)}"}), 500
