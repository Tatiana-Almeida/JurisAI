FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME=/app
ENV APP_USER=appuser
ENV APP_GROUP=appgroup
ENV APP_UID=10001
ENV APP_GID=10001
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    libpq-dev \
    poppler-utils \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid ${APP_GID} ${APP_GROUP} \
    && useradd --uid ${APP_UID} --gid ${APP_GID} --create-home --shell /bin/sh ${APP_USER} \
    && mkdir -p ${APP_HOME}/staticfiles ${APP_HOME}/media ${APP_HOME}/logs \
    && chown -R ${APP_USER}:${APP_GROUP} ${APP_HOME} /home/${APP_USER}
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh \
    && chown -R ${APP_USER}:${APP_GROUP} ${APP_HOME}

USER ${APP_USER}

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "jurisai.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
