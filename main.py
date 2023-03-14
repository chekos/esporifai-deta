from deta import Base
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
# Connect to a Base for storing todo items.
auth = Base("esporifai-auth")


@app.get("/")
async def index():
    with open("./static/index.html") as file:
        return HTMLResponse(file.read())

@app.get("/login")
async def login():
    with open("./static/login.html") as file:
        return HTMLResponse(file.read())

