import random
import string
import requests
from requests.auth import HTTPBasicAuth
from deta import Base
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from constants import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, BASE_URL
from urllib import parse

app = FastAPI()

auth_base = Base("esporifai-auth")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    access_token = auth_base.get("access_token")
    refresh_token = auth_base.get("refresh_token")
    if access_token:
        page_content = '<main class="login-container"><a class="login-button" href="/me">let\'s go</a></main>'
    elif refresh_token:
        token = refresh_token["value"]
        page_content = f'<main class="login-container"><a class="login-button" href="/refresh?token={token}">let\'s go</a></main>'
    else:
        page_content = '<main class="login-container"><a class="login-button" href="/login">let\'s go</a></main>'

    context = {
        "request": request,
        "data": {
            "page_title": "Login",
            "page_content": page_content,
        },
    }
    return templates.TemplateResponse("page.html", context)


@app.get("/login", response_class=RedirectResponse)
async def login():
    state = "".join(random.choices(string.ascii_uppercase + string.digits, k=16))

    scope = "user-read-private user-read-email"
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "state": state,
        "scope": scope,
    }
    querystring = parse.urlencode(params)
    return f"https://accounts.spotify.com/authorize?{querystring}"


@app.get("/callback", response_class=RedirectResponse, status_code=200)
async def callback(request: Request, code: str = ""):
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
    }
    auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    res = requests.post(
        url="https://accounts.spotify.com/api/token",
        data=data,
        headers=headers,
        auth=auth,
    )

    if res.status_code == 200:
        auth_response = res.json()
        auth_base.put(
            key="access_code",
            data=auth_response["access_code"],
            expire_in=auth_response["expires_in"],
        )
        auth_base.put(key="refresh_token", data=auth_response["refresh_token"])
        auth_base.put(key="scope", data=auth_response["scope"])
        auth_base.put(key="token_type", data=auth_response["token_type"])

        return f"{BASE_URL}/me"
    else:
        return f"{BASE_URL}/login"


@app.get("/refresh", response_class=RedirectResponse)
def refresh(request: Request, token: str):
    data = {
        "grant_type": "refresh_token",
        "refresh_token": token,
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
    }
    auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    res = requests.post(
        url="https://accounts.spotify.com/api/token",
        data=data,
        headers=headers,
        auth=auth,
    )
    if res.status_code == 200:
        auth_response = res.json()
        for key, value in auth_response.items():
            auth_base.put(key=key, data=value)
        return f"{BASE_URL}/me"
    else:
        return f"{BASE_URL}/login"


@app.get("/me", response_class=HTMLResponse)
def get_me(request: Request):
    page_content = '<main class="login-container"><h1>Me!</h1></main>'
    context = {
        "request": request,
        "data": {
            "page_title": "Login",
            "page_content": page_content,
        },
    }
    return templates.TemplateResponse("page.html", context)
