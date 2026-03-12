import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DEFAULT_SQLITE_PATH = os.path.join(BASE_DIR, "resume_optimizer.db")


def _build_database_uri() -> str:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    db_username = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME")

    if db_username and db_password and db_name:
        return f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

    return f"sqlite:///{DEFAULT_SQLITE_PATH}"


SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
SQLALCHEMY_DATABASE_URI = _build_database_uri()
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", os.path.join(BASE_DIR, "uploads"))
MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 5 * 1024 * 1024))
AUTO_CREATE_TABLES = os.getenv("AUTO_CREATE_TABLES", "false").lower() == "true"
