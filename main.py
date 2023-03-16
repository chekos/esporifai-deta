import random
import string
import requests
from requests.auth import HTTPBasicAuth
from deta import Base
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from constants import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from urllib import parse

app = FastAPI()

auth_base = Base("esporifai-auth")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    context = {
        "request": request,
        "data": {
            "page_title": "Login",
            "page_content": '<main class="login-container"><a class="login-button" href="/login">this works</a></main>',
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


@app.get("/callback", response_class=HTMLResponse)
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
        for key, value in auth_response.items():
            auth_base.insert(key=key, data=value)
        page_content = f'<main class="login-container"><h1>Success!</h1><pre>{res.json()}</pre></main>'
    else:
        page_content = f'<main class="login-container"><p>{res.text}</p></main>'

    context = {
        "request": request,
        "data": {
            "page_title": "Callback",
            "page_content": page_content,
        },
    }
    return templates.TemplateResponse("page.html", context)
