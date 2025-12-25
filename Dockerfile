# syntax=docker/dockerfile:1.6

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    TZ=Africa/Abidjan

# Dépendances système (psycopg2, compilation, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Installer les dépendances Python en amont (cache docker)
COPY requirements*.txt /app/
RUN pip install --upgrade pip \
 && if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Copier le code
COPY . /app/

# Dossiers attendus par volumes (même si montés ensuite)
RUN mkdir -p /app/static /app/staticfiles /app/media /app/logs /app/dbbackup

# Ajouter un user non-root
RUN useradd -m -u 10001 appuser \
 && chown -R appuser:appuser /app

# Entrypoint
COPY /entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER appuser

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "rhpartnersafric.wsgi:application", "--bind", "0.0.0.0:8000"]