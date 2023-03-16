import os
from dotenv import load_dotenv


load_dotenv()

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")
REDIRECT_URI = f"{BASE_URL}/callback"
