from deta import Base
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

auth = Base("esporifai-auth")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    context = {
        "request": request,
        "data": {"page_title": "Login", "page_content": '<div id="login-button">this works</div>'},
    }
    return templates.TemplateResponse("page.html", context)


@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    context = {"request": request,
                      "data": {
                          "page_title": "Home", 
                          "page_content": '<div id="login-button">Login</div><br/><a href="/">go back</a>'},
              }
    return templates.TemplateResponse("login.html", context)
