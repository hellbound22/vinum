import os
from src.main import start_server

os.environ["FLASK_ENV"] = "development"

start_server("127.0.0.1", True)
