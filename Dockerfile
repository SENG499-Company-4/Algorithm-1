FROM python:3.9-slim

WORKDIR /code

COPY ./requirements.txt /code/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./.env /code/
COPY ./algo1 /code/algo1
COPY ./tp.xlsx /code

CMD ["python", "-m", "algo1.api.run"]
