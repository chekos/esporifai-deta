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
    context = {
        "request": request,
        "title": "Profile",
    }
    return templates.TemplateResponse("profile.html", context)


@app.get("/htmx/me", response_class=HTMLResponse)
async def get_html_me(request: Request):
    profile = get_user_profile()
    playlists = get_user_playlists()
    context = {"request": request, "profile": profile, "playlists": playlists}
    return templates.TemplateResponse("partials/profile-header.html", context)


@app.get("/top-artists", response_class=HTMLResponse)
async def get_top_artists(request: Request):
    context = {
        "request": request,
        "title": "Top Artists",
    }
    return templates.TemplateResponse("top-artists.html", context)


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
    context = {
        "request": request,
        "title": "Top Tracks",
    }
    return templates.TemplateResponse("top-tracks.html", context)


@app.get("/htmx/top-tracks", response_class=HTMLResponse)
async def get_html_top_tracks(request: Request):
    data = get_user_top_tracks()
    context = {
        "request": request,
        "data": data,
    }
    return templates.TemplateResponse("partials/top-tracks.html", context)


@app.get("/playlists", response_class=HTMLResponse)
async def get_playlists(request: Request):
    context = {
        "request": request,
        "title": "Playlists",
    }
    return templates.TemplateResponse("playlists.html", context)


@app.get("/htmx/playlists", response_class=HTMLResponse)
async def get_html_playlists(request: Request):
    data = get_user_playlists()
    context = {
        "request": request,
        "data": data,
    }
    return templates.TemplateResponse("partials/playlists.html", context)


@app.get("/htmx/profile-top-artists", response_class=HTMLResponse)
async def get_html_profile_top_artists(request: Request, limit: int = 10):
    context = {
        "request": request,
        "title": "Top Artists",
        "see_all_link": "/top-artists",
        "htmx_endpoint": f"/htmx/artist-grid?limit={limit}",
    }
    return templates.TemplateResponse("partials/styled-section.html", context)


@app.get("/htmx/artist-grid", response_class=HTMLResponse)
async def get_html_artist_grid(request: Request, limit: int = 10):
    data = get_user_top_artists()
    artists = data["items"][0:limit]
    context = {
        "request": request,
        "artists": artists,
    }
    return templates.TemplateResponse("partials/artist-grid.html", context)


@app.get("/htmx/profile-top-tracks", response_class=HTMLResponse)
async def get_html_profile_top_tracks(request: Request, limit: int = 10):
    context = {
        "request": request,
        "title": "Top Tracks",
        "see_all_link": "/top-tracks",
        "htmx_endpoint": f"/htmx/tracklist?limit={limit}",
    }
    return templates.TemplateResponse("partials/styled-section.html", context)


@app.get("/htmx/tracklist", response_class=HTMLResponse)
async def get_html_artist_grid(request: Request, limit: int = 10):
    data = get_user_top_tracks()
    tracklist = data["items"][0:limit]
    context = {
        "request": request,
        "tracklist": tracklist,
    }
    return templates.TemplateResponse("partials/tracklist.html", context)


@app.get("/htmx/profile-playlists", response_class=HTMLResponse)
async def get_html_profile_playlists(request: Request, limit: int = 10):
    context = {
        "request": request,
        "title": "Playlists",
        "see_all_link": "/playlists",
        "htmx_endpoint": f"/htmx/playlist-grid?limit={limit}",
    }
    return templates.TemplateResponse("partials/styled-section.html", context)


@app.get("/htmx/playlist-grid", response_class=HTMLResponse)
async def get_html_playlist_grid(request: Request, limit: int = 10):
    data = get_user_playlists()
    playlists = data["items"][0:limit]
    context = {
        "request": request,
        "playlists": playlists,
    }
    return templates.TemplateResponse("partials/playlist-grid.html", context)
