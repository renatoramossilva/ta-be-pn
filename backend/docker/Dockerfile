FROM python:3.10-slim

WORKDIR /app/backend

ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONUNBUFFERED=1

COPY . ./

# Install Poetry and dependencies
RUN pip install --no-cache-dir poetry && \
    poetry install --no-root

# Run tests
RUN coverage run -m pytest

# Export test coverage to HTML file
RUN coverage html

EXPOSE 8000 5001

CMD ["sh", "-c", "uvicorn app.main:app --host=0.0.0.0 & python -m http.server 5001 --directory htmlcov"]
