import os
from src.main import start_server

os.environ["FLASK_ENV"] = "production"

start_server("0.0.0.0", False)
