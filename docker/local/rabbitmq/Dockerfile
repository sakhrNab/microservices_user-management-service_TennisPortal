FROM python:3.10.0-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV APP_HOME=/app
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles

WORKDIR $APP_HOME

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app
