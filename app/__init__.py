from flask import Flask
from flask_cors import CORS
from config.settings import get_config
from app.caches.games_cache import initialize_game_cache


def create_app(env="development"):
    config = get_config(env)

    app = Flask(__name__)
    app.config.from_object(config)

    # 設定 CORS
    cors_origins = config.CORS_ORIGINS
    if cors_origins == "*":
        # 允許所有來源
        origins = "*"
    else:
        # 使用指定的來源列表
        origins = [origin.strip() for origin in cors_origins.split(",")]
    CORS(
        app,
        resources={
            r"/*": {
                "origins": origins,
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": [
                    "Content-Type",
                    "Authorization",
                    "Access-Control-Allow-Credentials",
                ],
                "supports_credentials": config.CORS_ALLOW_CREDENTIALS,
            }
        },
    )
    print(f"CORS configured with origins: {origins}")

    # 初始化遊戲 cache
    initialize_game_cache(
        auto_save_interval=config.AUTO_SAVE_INTERVAL,
    )

    # 註冊藍圖（Blueprints）
    from app.api.heartbeat import heartbeat_bp
    from app.api.game import game_bp

    app.register_blueprint(heartbeat_bp, url_prefix="/")
    app.register_blueprint(game_bp, url_prefix="/api/game")

    return app
