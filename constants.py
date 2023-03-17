import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")
REDIRECT_URI = f"{BASE_URL}/callback"

basic_auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)

API_BASE_URL = "https://api.spotify.com/v1"
SCOPE = "user-read-private user-read-email user-top-read"