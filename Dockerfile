FROM python:3.9-slim

WORKDIR /code

COPY ./requirements.txt /code/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./api /code/api
COPY ./tp.xlsx /code
