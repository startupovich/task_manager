# Менеджер задач (Task Manager API)

FastAPI приложение для управления задачами с полным CRUD функционалом.

## Быстрый старт

```bash
# 1. Клонирование и установка
git clone <task_manager>
cd task_manager
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# 2. Запуск приложения
uvicorn app.main:app --reload

# 3. Тестирование
pytest tests/
```

## Документация API

После запуска откройте в браузере:
http://localhost:8000/docs - интерактивная документация Swagger
http://localhost:8000/redoc - альтернативная документация

## Основные эндпоинты

GET /tasks - список всех задач
POST /tasks - создание новой задачи
GET /tasks/{id} - получение задачи по ID
PUT /tasks/{id} - обновление задачи
DELETE /tasks/{id} - удаление задачи

## Docker запуск

```bash
docker build -t task-manager .
docker run -p 8000:8000 task-manager
```
## Структура проекта
```text
task_manager/
├── app/
│   ├── main.py      # FastAPI приложение
│   ├── models.py    # Модели данных
│   └── database.py  # Хранилище в памяти
├── tests/
│   └── test_api.py  # Тесты
├── requirements.txt # Зависимости
└── Dockerfile       # Конфигурация Docker
```
Приложение использует in-memory хранилище. Данные сохраняются до перезапуска.

