import fastapi

from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="src/app/templates")


@router.get("/resume/upload", response_class=HTMLResponse)
def upload_resume_form(request: Request):
    return templates.TemplateResponse("resume/upload_resume.html", {"request": request})

@router.post("/resume/upload")
async def upload_resume(request: Request, file: UploadFile = File(...)):
    # ... ваш парсинг ...
    # Сохраняем данные в сессию или временное хранилище
    # Редирект на /resume/edit
    return RedirectResponse("/resume/edit", status_code=303)

@router.get("/resume/edit", response_class=HTMLResponse)
def edit_resume(request: Request):
    # Получаем данные из сессии (заглушка)
    fake_resume_data = {
        "position": "Python Developer",
        "salary": "100000",
        "specializations": ["Backend", "AI"],
        "employment": "Полная занятость",
        "schedule": "Полный день",
        "education": "МГУ, 2020",
        "skills": "Python; FastAPI; SQL",
        "languages": "Русский, Английский",
        "about": "Ответственный и мотивированный разработчик."
    }
    return templates.TemplateResponse("resume/edit_resume.html", {"request": request, "resume_data": fake_resume_data})

@router.post("/resume/edit")
def save_resume_edits(request: Request):
    # Сохраняем изменения (заглушка)
    return RedirectResponse("/resume/confirm", status_code=303)

@router.get("/resume/confirm", response_class=HTMLResponse)
def confirm_resume(request: Request):
    # Получаем данные из сессии (заглушка)
    fake_resume_data = {
        "position": "Python Developer",
        "salary": "100000",
        "specializations": ["Backend", "AI"],
        "employment": "Полная занятость",
        "schedule": "Полный день",
        "education": "МГУ, 2020",
        "skills": "Python; FastAPI; SQL",
        "languages": "Русский, Английский",
        "about": "Ответственный и мотивированный разработчик."
    }
    return templates.TemplateResponse("confirm_resume.html", {"request": request, "resume_data": fake_resume_data})

@router.post("/resume/confirm")
def confirm_resume_post(request: Request):
    # Подтверждаем, редирект на /vacancies/search_settings
    return RedirectResponse("/vacancies/search_settings", status_code=303)