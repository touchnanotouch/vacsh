from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.app.routers import vacancies, resume, about


app = FastAPI()
app.include_router(vacancies.router)
app.include_router(resume.router)
app.include_router(about.router)

app.mount("/static", StaticFiles(directory="src/app/static"), name="static")

templates = Jinja2Templates(directory="src/app/templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
