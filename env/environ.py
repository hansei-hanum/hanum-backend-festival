import os
import dotenv

dotenv.load_dotenv()


class Env:
    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.environ.get("PORT", 80))
    DEBUG = os.environ.get("DEBUG", "False") == "True"


class MicroEnv:
    AUTH_HOST = os.environ.get("GRPC_AUTH_HOST")
    AUTH_PORT = int(os.environ.get("GRPC_AUTH_PORT"))


class DatabaseEnv:
    HOST = os.environ.get("DATABASE_HOST")
    PORT = int(os.environ.get("DATABASE_PORT"))
    USERNAME = os.environ.get("DATABASE_USERNAME")
    PASSWORD = os.environ.get("DATABASE_PASSWORD")
    DATABASE = os.environ.get("DATABASE_NAME")
