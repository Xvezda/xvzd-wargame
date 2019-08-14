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

# https://github.com/joyzoursky/docker-python-chromedriver
# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

RUN apt-get update -qq -y
RUN apt-get install -qq -y apt-utils
RUN DEBIAN_FRONTEND=noninteractive apt-get install -qq -y mysql-server
RUN apt-get install -qq -y redis-server
RUN apt-get install -qq -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

COPY ./app /app

# install selenium
#RUN pip install selenium==3.8.0
WORKDIR /app
RUN pip install -r requirements.txt

