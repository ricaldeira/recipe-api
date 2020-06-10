FROM python:3.7-alpine
LABEL Ricardo Caldeira

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache postgresql-client

RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt

RUN apk del .tmp-build-deps

RUN mkdir /backend
WORKDIR /backend
COPY ./backend /backend

RUN adduser -D user
USER user

