// Stepper logic and state
const steps = [
    document.getElementById('step-0'),
    document.getElementById('step-1'),
    document.getElementById('step-2'),
    document.getElementById('step-3'),
    document.getElementById('step-4'),
];

const steppers = [
    document.getElementById('stepper-0'),
    document.getElementById('stepper-1'),
    document.getElementById('stepper-2'),
    document.getElementById('stepper-3'),
    document.getElementById('stepper-4'),
];

const stepBack = document.getElementById('step-back');
const stepNext = document.getElementById('step-next');

let currentStep = 0;

function showStep(idx) {
    steps.forEach((el, i) => el.style.display = i === idx ? '' : 'none');
    steppers.forEach((el, i) => {
        el.classList.remove('active', 'done');
        if (i < idx) el.classList.add('done');
        else if (i === idx) el.classList.add('active');
    });

    // Управление кнопками
    stepBack.style.display = idx === 0 ? 'none' : '';
    stepNext.style.display = idx === 4 ? 'none' : '';
    stepBack.textContent = idx === 1 ? 'Назад к загрузке' : 'Назад';
    stepNext.textContent = idx === 3 ? 'Откликнуться' : (idx === 2 ? 'Далее' : (idx === 4 ? 'Готово' : 'Далее'));
    currentStep = idx;
}

showStep(0);

stepBack.onclick = () => {
    if (currentStep > 0) showStep(currentStep - 1);
};
stepNext.onclick = () => {
    if (currentStep === 0) {
        form.requestSubmit();
    } else if (currentStep === 1) {
        resumeData.searchQuery = document.getElementById('searchQuery').value;
        renderConfirmTable();
        showStep(2);
    } else if (currentStep === 2) {
        renderVacancies();
        showStep(3);
    } else if (currentStep === 3) {
        renderAiLetters();
        showStep(4);
    } else if (currentStep === 4) {
        showAlert('Спасибо! Ваши отклики готовы.', 'success');
    }
};

// Step 1: Загрузка и разбор резюме
const form = document.getElementById('resumeForm');
const alertBox = document.getElementById('alert');
const loading = document.getElementById('loading');

const blockTitles = {
    position: 'Желаемая должность',
    skills: 'Навыки',
    education: 'Образование',
    about: 'О себе',
    salary: 'Желаемая зарплата',
    languages: 'Знание языков',
    specializations: 'Специализации',
    employment: 'Занятость',
    schedule: 'График работы',
};

let resumeData = {};
let selectedVacancies = [];

form.onsubmit = async function(e) {
    e.preventDefault();
    alertBox.style.display = 'none';
    loading.style.display = 'block';
    const formData = new FormData(form);
    try {
        const response = await fetch('/api/upload_resume', {
            method: 'POST',
            body: formData
        });
        loading.style.display = 'none';
        if (!response.ok) {
            const err = await response.json();
            showAlert(err.error || 'Ошибка загрузки', 'danger');
            return;
        }
        resumeData = await response.json();
        renderResumeEditTable();
        showStep(1);
    } catch (err) {
        loading.style.display = 'none';
        showAlert('Ошибка соединения с сервером.', 'danger');
    }
};

// Step 2: Редактирование и параметры поиска
function renderResumeEditTable() {
    const tableDiv = document.getElementById('resume-edit-table');
    let html = '<table class="table table-borderless align-middle mb-0">';
    Object.entries(blockTitles).forEach(([key, title]) => {
        html += `<tr><th class="text-nowrap">${title}</th><td>` +
            (key === 'about' || key === 'education' || key === 'skills' || key === 'languages' || key === 'specializations'
                ? `<textarea class="form-control" id="input_${key}" rows="2">${escapeHtml(resumeData[key]||'')}</textarea>`
                : `<input class="form-control" id="input_${key}" value="${escapeHtml(resumeData[key]||'')}">`)
            + '</td></tr>';
    });
    html += '</table>';
    tableDiv.innerHTML = html;
    Object.keys(blockTitles).forEach(key => {
        const el = document.getElementById('input_' + key);
        if (el) {
            el.addEventListener('input', (e) => {
                resumeData[key] = e.target.value;
            });
        }
    });
}

// Step 3: Подтверждение
function renderConfirmTable() {
    const tableDiv = document.getElementById('confirm-table');
    let html = '<table class="table table-borderless align-middle mb-0">';
    Object.entries(blockTitles).forEach(([key, title]) => {
        html += `<tr><th class="text-nowrap">${title}</th><td>${escapeHtml(resumeData[key]||'')}</td></tr>`;
    });
    html += '</table>';
    tableDiv.innerHTML = html;
    // Параметры поиска
    document.getElementById('confirm-search').innerHTML =
        `<div class="card"><div class="card-body"><b>Специальность:</b> ${escapeHtml(resumeData.searchQuery||'')}</div></div>`;
}

// Step 4: Вакансии (grid)
async function renderVacancies() {
    const vacancyList = document.getElementById('vacancy-list');
    vacancyList.innerHTML = '<div class="text-muted">Загрузка вакансий...</div>';
    let vacancies = [];
    try {
        const response = await fetch('/api/vacancies');
        if (response.ok) {
            vacancies = await response.json();
        } else {
            vacancyList.innerHTML = '<div class="text-danger">Ошибка загрузки вакансий</div>';
            return;
        }
    } catch (e) {
        vacancyList.innerHTML = '<div class="text-danger">Ошибка соединения с сервером</div>';
        return;
    }
    if (!Array.isArray(vacancies) || vacancies.length === 0) {
        vacancyList.innerHTML = '<div class="text-muted">Вакансии не найдены</div>';
        return;
    }
    let html = '';
    vacancies.forEach(v => {
        html += `<div class="card">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <div>
                        <b>${escapeHtml(v.title || v.Должность || '')}</b><br>
                        <span class="text-muted">${escapeHtml(v.company || v.Компания || '')}</span>
                    </div>
                    <input type="checkbox" class="form-check-input vacancy-check" data-id="${v.id || v.ID || ''}">
                </div>
                <div>${escapeHtml(v.description || v.Описание || '')}</div>
            </div>
        </div>`;
    });
    vacancyList.innerHTML = html;
    // Сброс выбора
    selectedVacancies = [];
    document.querySelectorAll('.vacancy-check').forEach(cb => {
        cb.onchange = function() {
            const id = cb.getAttribute('data-id');
            if (cb.checked) {
                if (selectedVacancies.length < 3) {
                    selectedVacancies.push(id);
                } else {
                    cb.checked = false;
                    showAlert('Можно выбрать не более 3 вакансий.', 'warning');
                }
            } else {
                selectedVacancies = selectedVacancies.filter(x => x !== id);
            }
        };
    });
}

// Step 5: Отклики (заглушка)
function renderAiLetters() {
    const aiDiv = document.getElementById('ai-letters');
    aiDiv.innerHTML = selectedVacancies.length === 0
        ? '<div class="alert alert-warning">Вы не выбрали ни одной вакансии.</div>'
        : selectedVacancies.map((id, idx) =>
            `<div class="card mb-2"><div class="card-body">
                <div class="fw-bold mb-1">Вакансия #${id}</div>
                <div class="mb-2">Сопроводительное письмо: <br><span class="text-muted">(пример текста от ИИ)</span></div>
                <a href="#" class="btn btn-outline-primary btn-sm">Перейти к вакансии</a>
            </div></div>`
        ).join('');
}

function escapeHtml(text) {
    if (typeof text !== 'string') return text;
    return text.replace(/[&<>"']/g, function (c) {
        return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;','\'':'&#39;'}[c];
    });
}

function showAlert(msg, type) {
    alertBox.className = `alert alert-${type}`;
    alertBox.textContent = msg;
    alertBox.style.display = 'block';
    setTimeout(() => { alertBox.style.display = 'none'; }, 3500);
}
