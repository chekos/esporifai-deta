import json
import random
import string
from urllib import parse

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from constants import CLIENT_ID, REDIRECT_URI, BASE_URL, SCOPE
from data import (
    get_auth_code,
    get_refreshed_token,
    retrieve_token,
    get_user_profile,
    delete_auth_data,
    get_user_playlists,
    get_user_top_artists,
    get_user_top_tracks,
)

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

    scope = SCOPE
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "state": state,
        "scope": scope,
    }
    querystring = parse.urlencode(params)
    return f"https://accounts.spotify.com/authorize?{querystring}"


@app.get("/callback", response_class=RedirectResponse)
async def callback(code: str = ""):
    access_code = get_auth_code(code=code)
    if access_code:
        print(access_code)
        return f"{BASE_URL}/me"
    else:
        return f"{BASE_URL}/login"


@app.get("/refresh", response_class=RedirectResponse)
async def refresh(token: str):
    access_token = get_refreshed_token(token=token)
    if access_token:
        return RedirectResponse(f"{BASE_URL}/me")
    else:
        return RedirectResponse(f"{BASE_URL}/")


@app.get("/logout", response_class=RedirectResponse)
async def logout():
    delete_auth_data()
    return BASE_URL


@app.get("/me", response_class=HTMLResponse)
async def get_me(request: Request):
    data_html = f'<div hx-get="/htmx/me" hx-trigger="load"><div></div></div>'
    page_content = f'<main class="login-container"><button class="logout-button" onClick="location.href = \'{BASE_URL}/logout\';">Log out</button>{data_html}</main>'
    context = {
        "request": request,
        "data": {
            "page_title": "Profile",
            "page_content": page_content,
        },
    }
    return templates.TemplateResponse("page.html", context)


@app.get("/htmx/me", response_class=HTMLResponse)
async def get_html_me():
    profile = get_user_profile()
    html = f"""
        <div>
          <h1>{profile['display_name']}</h1>
          <p>{profile['followers']['total']} Followers</p>
            <img src={profile['images'][0]['url']} alt="Avatar"/>
        </div>
    """
    return html


@app.get("/top-artists", response_class=HTMLResponse)
async def get_top_artists(request: Request):
    data_html = f'<div hx-get="/htmx/top-artists" hx-trigger="load"><div></div></div>'
    page_content = f'<main class="login-container"><button class="logout-button" onClick="location.href = \'{BASE_URL}/\';">Log out</button>{data_html}</main>'
    context = {
        "request": request,
        "data": {
            "page_title": "Top Artists",
            "page_content": page_content,
        },
    }
    return templates.TemplateResponse("page.html", context)


@app.get("/htmx/top-artists", response_class=HTMLResponse)
async def get_html_top_artists(request: Request):
    data = get_user_top_artists()
    context = {
        "request": request,
        "data": data,
    }
    return templates.TemplateResponse("partials/top-artists.html", context)


@app.get("/top-tracks", response_class=HTMLResponse)
async def get_top_tracks(request: Request):
    data_html = f'<div hx-get="/htmx/top-tracks" hx-trigger="load"><div></div></div>'
    page_content = f'<main class="login-container"><button class="logout-button" onClick="location.href = \'{BASE_URL}/\';">Log out</button>{data_html}</main>'
    context = {
        "request": request,
        "data": {
            "page_title": "Top Tracks",
            "page_content": page_content,
        },
    }
    return templates.TemplateResponse("page.html", context)


@app.get("/htmx/top-tracks", response_class=HTMLResponse)
async def get_html_top_tracks():
    data = get_user_top_tracks()
    html = f"""<pre>{json.dumps(data, indent = 4, default=str)}</pre>"""
    return html


@app.get("/playlists", response_class=HTMLResponse)
async def get_playlists(request: Request):
    data_html = f'<div hx-get="/htmx/playlists" hx-trigger="load"><div></div></div>'
    page_content = f'<main class="login-container"><button class="logout-button" onClick="location.href = \'{BASE_URL}/\';">Log out</button>{data_html}</main>'
    context = {
        "request": request,
        "data": {
            "page_title": "Top Tracks",
            "page_content": page_content,
        },
    }
    return templates.TemplateResponse("page.html", context)


@app.get("/htmx/playlists", response_class=HTMLResponse)
async def get_html_playlists():
    data = get_user_playlists()
    html = f"""<pre>{json.dumps(data, indent = 4, default=str)}</pre>"""
    return html
