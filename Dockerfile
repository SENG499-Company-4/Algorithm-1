FROM python:3.9-slim

WORKDIR /code

COPY ./requirements.txt /code/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt \
    # install ray 3.0.0dev wheel
    pip install -U https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-3.0.0.dev0-cp39-cp39-manylinux2014_x86_64.whl 

COPY ./.env /code/
COPY ./api /code/api
COPY ./tp.xlsx /code
COPY ./rl  /code/rl/

#CMD ["python", "-m", "api.run"]
CMD ["python", "rl/tuner.py"]
