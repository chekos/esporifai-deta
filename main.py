import json
import random
import string
from urllib import parse

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from constants import CLIENT_ID, REDIRECT_URI, BASE_URL
from data import get_auth_code, get_refreshed_token, retrieve_token, get_user_profile

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    access_token = retrieve_token()
    if access_token:
        page_content = '<main class="login-container"><a class="login-button" href="/me">let\'s go</a></main>'
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
async def callback(code: str = ""):
    access_code = get_auth_code(code=code)

    if access_code:
        return f"{BASE_URL}/me"
    else:
        return f"{BASE_URL}/login"


@app.get("/refresh", response_class=RedirectResponse)
def refresh(token: str):
    access_token = get_refreshed_token(token=token)
    if access_token:
        return f"{BASE_URL}/me"
    else:
        return f"{BASE_URL}/login"


@app.get("/me", response_class=HTMLResponse)
def get_me(request: Request):
    data = get_user_profile()
    data_html = f"<pre>{json.dumps(data, default=str, indent=4)}</pre>"
    page_content = f'<main class="login-container"><h1>Me!</h1>{data_html}</main>'
    context = {
        "request": request,
        "data": {
            "page_title": "Login",
            "page_content": page_content,
        },
    }
    return templates.TemplateResponse("page.html", context)
