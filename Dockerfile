FROM alpine

MAINTAINER Bartek Kryza <bkryza@gmail.com>

RUN apk add --no-cache bash git python3 \
        && pip3 install --upgrade pip \
        && pip3 install connexion

ADD . /luma

WORKDIR /luma

ENTRYPOINT python3 app.py
