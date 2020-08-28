FROM python:3.6.8

ENV PYTHONUNBUFFERED 1

WORKDIR /root

RUN apt-get update

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /code/
