# Dockerfile für Django + MariaDB
FROM python:3.12-slim

# System-Abhängigkeiten
RUN apt-get update && apt-get install -y build-essential default-libmysqlclient-dev pkg-config && rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis
WORKDIR /app

# Kopiere Projektdateien
COPY . /app/

# Installiere Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Django-Settings: Production
ENV DJANGO_SETTINGS_MODULE=viastore_project.settings

# Port für Gunicorn/Django
EXPOSE 8000

# Startbefehl
CMD ["gunicorn", "viastore_project.wsgi:application", "--bind", "0.0.0.0:8000"]
