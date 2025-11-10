# config/settings.py
class BaseConfig:
    SECRET_KEY = "replace_me"
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    DATABASE_URI = "sqlite:///dev.db"


class ProductionConfig(BaseConfig):
    DATABASE_URI = "postgresql://user:password@db:5432/my_api"


def get_config(env):
    if env == "production":
        return ProductionConfig
    return DevelopmentConfig
