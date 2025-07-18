import fastapi

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="src/app/templates")


@router.get("/vacancies/search_settings", response_class=HTMLResponse)
def search_settings(request: Request):
    return templates.TemplateResponse("vacancies/search_settings.html", {"request": request})

@router.post("/vacancies/search_settings")
def search_settings_post(request: Request, search_query: str = Form(...)):
    # Сохраняем параметры поиска
    return RedirectResponse("/vacancies/list", status_code=303)

@router.get("/vacancies/list", response_class=HTMLResponse)
def list_vacancies(request: Request):
    # Получаем параметры поиска, запускаем парсер, получаем вакансии (заглушка)
    fake_vacancies = [
        {
            "title": "Python Developer",
            "company": "ООО Рога и Копыта",
            "address": "Москва",
            "experience": "1-3 года",
            "link": "https://hh.ru/vacancy/123456"
        },
        {
            "title": "Data Scientist",
            "company": "��ОО Данные",
            "address": "Санкт-Петербург",
            "experience": "Нет опыта",
            "link": "https://hh.ru/vacancy/654321"
        }
    ]
    return templates.TemplateResponse("vacancies/vacancies_list.html", {"request": request, "vacancies": fake_vacancies})
