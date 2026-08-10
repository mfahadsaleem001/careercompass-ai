import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-key-not-secure"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

    UPLOAD_FOLDER = os.environ.get(
        "UPLOAD_FOLDER",
        os.path.join(basedir, "app", "uploads")
    )

    REPORTS_FOLDER = os.environ.get(
        "REPORTS_FOLDER",
        os.path.join(basedir, "app", "reports")
    )

    MAX_CONTENT_LENGTH = int(
        os.environ.get(
            "MAX_CONTENT_LENGTH",
            5 * 1024 * 1024
        )
    )

    ALLOWED_RESUME_EXTENSIONS = {"pdf", "docx"}

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    DATABASE_URL = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(basedir, "careercompass.db")
    )

    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://",
            "postgresql://",
            1
        )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL


class ProductionConfig(Config):
    DEBUG = False

    DATABASE_URL = os.environ.get("DATABASE_URL")

    # If PostgreSQL URL is provided, use PostgreSQL.
    # Otherwise use local SQLite for demo/testing deployment.
    if DATABASE_URL:
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace(
                "postgres://",
                "postgresql://",
                1
            )
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        SQLALCHEMY_DATABASE_URI = (
            "sqlite:///" +
            os.path.join(basedir, "careercompass.db")
        )

    @staticmethod
    def init_app(app):
        Config.init_app(app)


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}