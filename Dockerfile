FROM python:3.11-slim

WORKDIR /app

COPY ./ /app

RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --vityual. .build-deps gcc musl-dev && \
    pip3 install -r req.txt --no-cache-dir

CMD ["gunicorn", "kristall.wsgi:application", "--bind", "0:8000" ]