FROM ubuntu:18.04

WORKDIR /data

ADD . /data

RUN apt update && apt -y upgrade && \
    apt install -y nginx curl cron socat

RUN mkdir -p /etc/letsencrypt/nginx

EXPOSE 80 443
