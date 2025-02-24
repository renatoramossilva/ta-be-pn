FROM python:3.10-slim

WORKDIR /app

ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml poetry.lock* ./

# Install Poetry and dependencies
RUN pip install --no-cache-dir poetry && \
    poetry install --no-root

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
