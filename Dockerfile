
FROM python:3.13-slim
WORKDIR /app
COPY . .

RUN pip install --no-cache-dir poetry

RUN poetry install --no-root

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
