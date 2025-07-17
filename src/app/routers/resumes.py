import os
import re

from fastapi import APIRouter, UploadFile, File

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

VACANCIES_PATH = os.path.join(BASE_DIR, "data", "vacancies", "vacancies.csv")


@router.post("/api/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    resume_text = (
        await file.read()
    ).decode('utf-8').replace('\r\n', '\n').replace('\r', '\n')

    lines = [line.strip() for line in resume_text.split('\n') if line.strip()]

    block_titles = [
        "Желаемая должность и зарплата",
        "Специализации:",
        "Занятость:",
        "График работы:",
        "Желательное время в пути до работы:",
        "Образование",
        "Навыки",
        "Знание языков",
        "Дополнительная информация",
        "Обо мне"
    ]

    # Индексы начала блоков
    block_indices = {}
    for i, line in enumerate(lines):
        for title in block_titles:
            if line.startswith(title):
                block_indices.setdefault(title, []).append(i)

    def get_block(start_title, end_title=None, after_idx=0):
        starts = block_indices.get(start_title)

        if not starts:
            return []


        start = next((idx for idx in starts if idx >= after_idx), starts[-1])

        if end_title:
            ends = block_indices.get(end_title)
            if ends:
                end = next((idx for idx in ends if idx > start), len(lines))
            else:
                end = len(lines)
        else:
            end = len(lines)

        return lines[start+1:end]

    result = {}

    # Должность и зарплата
    pos_block = get_block("Желаемая должность и зарплата", "Специализации:")
    if pos_block:
        result["position"] = pos_block[0]
        if len(pos_block) > 1:
            result["salary"] = pos_block[1]

    # Специализации
    spec_block = get_block("Специализации:", "Занятость:")
    if spec_block:
        result["specializations"] = [s.strip() for s in spec_block if s.strip()]

    def get_value_from_title_line(title):
        idxs = block_indices.get(title)

        if not idxs:
            return ""

        idx = idxs[0]
        line = lines[idx]
        parts = line.split(":", 1)

        if len(parts) > 1 and parts[1].strip():
            return parts[1].strip()

        if idx + 1 < len(lines) and lines[idx + 1] not in block_titles:
            return lines[idx + 1]

        return ""

    # Занятость
    result["employment"] = get_value_from_title_line("Занятость:")

    # График работы
    result["schedule"] = get_value_from_title_line("График работы:")

    # Образование
    edu_block = get_block("Образование", "Навыки")
    if edu_block:
        result["education"] = "\n".join(edu_block)

    # Навыки (берём последний блок "Навыки" после "Знание языков", если есть)
    skill_indices = block_indices.get("Навыки", [])
    lang_indices = block_indices.get("Знание языков", [])
    last_skill_idx = skill_indices[-1] if skill_indices else None
    last_lang_idx = lang_indices[-1] if lang_indices else -1

    # Если есть "Знание языков" и после него "Навыки" — берём этот блок
    if last_skill_idx is not None and last_skill_idx > last_lang_idx:
        skills = []

        for line in lines[last_skill_idx+1:]:
            if line in block_titles:
                break
            skills.append(line)

        result["skills"] = "; ".join(skills)
    # Если нет языков, берём просто последний блок "Навыки"
    elif last_skill_idx is not None:
        skills = []
        for line in lines[last_skill_idx+1:]:
            if line in block_titles:
                break
            skills.append(line)

        result["skills"] = "; ".join(skills)

    # Языки (между "Знание языков" и следующим "Навыки")
    if lang_indices:
        lang_start = lang_indices[-1] + 1

        next_skill = next((idx for idx in skill_indices if idx > lang_start), None)
        lang_end = next_skill if next_skill else len(lines)

        languages = []
        for line in lines[lang_start:lang_end]:
            if line in block_titles:
                break
            languages.append(line)

        result["languages"] = "; ".join(languages)

    # "Обо мне"
    about_block = get_block("Обо мне")
    if about_block:
        result["about"] = "\n".join(about_block)

    return result
