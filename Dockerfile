FROM python:3.6.8

ENV PYTHONUNBUFFERED 1

WORKDIR /root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libxslt-dev \
        libssl1.0-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /code/
