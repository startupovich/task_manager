FROM python:3.11-slim as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim as final

WORKDIR /app

# Копируем только установленные пакеты из стадии builder
COPY --from=builder /root/.local /root/.local
COPY ./app ./app

# Делаем установленные пакеты доступными в PATH
ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000

# Запускаем от непривилегированного пользователя для безопасности
USER 1000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]