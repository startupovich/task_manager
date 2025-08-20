# Менеджер задач (Task Manager API)

FastAPI приложение для управления задачами с полным CRUD функционалом.

## 🚀 Быстрый старт

```bash
# 1. Клонирование и установка
git clone <ваш-репозиторий>
cd task_manager
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# 2. Запуск приложения
uvicorn app.main:app --reload

# 3. Тестирование
pytest tests/