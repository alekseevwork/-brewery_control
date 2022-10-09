FROM python:3.10.7-slim-buster
WORKDIR /server

ENV PIP_ROOT_USER_ACTION=ignore
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y upgrade
RUN pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000