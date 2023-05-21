FROM python:3.11

WORKDIR /app

COPY ./ /app

RUN pip3 install -r req.txt --no-cache-dir

CMD ["gunicorn", "kristall.wsgi:application", "--bind", "0:8000" ]