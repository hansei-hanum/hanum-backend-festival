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


class NeisEnv:
    API_KEY = os.environ.get("NEIS_API_KEY")
    SC_CODE = os.environ.get("NEIS_SC_CODE")
    SCHOOL_CODE = os.environ.get("NEIS_SCHOOL_CODE")
