import os

import pandas as pd

from fastapi import APIRouter


router = APIRouter()

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )
    )
)

VACANCY_DIR = os.path.join(BASE_DIR, "data", "vacancies")


@router.get("/api/vacancies")
def list_vacancies():
    if not os.path.exists(VACANCY_DIR):
        return []

    df = pd.read_csv(os.path.join(VACANCY_DIR, "vacancies.csv"))

    return df.to_dict(orient="records")
