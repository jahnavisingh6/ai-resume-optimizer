import os

# Database credentials
DB_USERNAME = "your_username"  # Replace with your PostgreSQL username
DB_PASSWORD = "your_password"  # Replace with your PostgreSQL password
DB_HOST = "localhost"  # Change if PostgreSQL is hosted on a different server
DB_PORT = "5432"  # Default port for PostgreSQL
DB_NAME = "resume_parser_db"  # Your target database name

# SQLAlchemy database URI
SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Disable tracking modifications for performance reasons
SQLALCHEMY_TRACK_MODIFICATIONS = False
