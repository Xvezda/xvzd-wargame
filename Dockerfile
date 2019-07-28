FROM tiangolo/uwsgi-nginx-flask:python2.7
MAINTAINER xvezda@naver.com

RUN groupadd -r mysql && useradd -r -g mysql mysql

ARG DEBIAN_FRONTEND=noninteractive
ARG DB_ROOT_PASSWORD
RUN echo mysql-community-server \
        mysql-community-server/root-pass password "$DB_ROOT_PASSWORD" \
        | debconf-set-selections
RUN echo mysql-community-server \
        mysql-community-server/re-root-pass password "$DB_ROOT_PASSWORD" \
        | debconf-set-selections
RUN apt-get update -qq -y
RUN apt-get install -qq -y mysql-server

COPY ./app /app

