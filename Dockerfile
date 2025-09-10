FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential && \
    rm -rf /var/lib/apt/lists/*

# зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# если используете poetry:
# COPY pyproject.toml poetry.lock* ./
# RUN pip install poetry && poetry install --no-root --no-interaction --no-ansi

# код
COPY . .

EXPOSE 8000

# указать правильный модуль — у вас main.py внутри src
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
