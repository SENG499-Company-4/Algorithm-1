FROM python:3.9-slim

WORKDIR /code

COPY ./requirements.txt /code/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./api /code/api
COPY ./tp.xlsx /code

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0"]
