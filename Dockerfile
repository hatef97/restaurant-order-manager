FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# copy first to leverage cache
COPY requirements.txt requirements-dev.txt /app/
RUN pip install --no-cache-dir -r requirements.txt \
    && if [ -f requirements-dev.txt ]; then pip install --no-cache-dir -r requirements-dev.txt; fi

COPY . /app

# default dev command (same as compose)
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
