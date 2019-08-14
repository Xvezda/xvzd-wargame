#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

import os
from flask import Flask
from flask_session import Session
from celery import Celery
from redis import Redis

from common.db import db_setup


XVZD_PREFIX__ = 'xvzd_'
XVZD_BOARDS__ = ['notice', 'qna', 'forum']

def create_app(__name__=__name__):
  app = Flask(__name__)

  # NOTE: This is NOT a flag! >:)
  app.secret_key = os.getenv('SECRET_KEY', os.urandom(32))
  db_setup(app)

  # Let's make session faster
  app.config['SESSION_TYPE'] = 'redis'
  app.config['SESSION_REDIS'] = Redis(host="127.0.0.1", port=6379)

  sess = Session()
  sess.init_app(app)

  return app


def make_celery(app):
  celery = Celery(
    'xvzd_wargame',
    backend=app.config['CELERY_RESULT_BACKEND'],
    broker=app.config['CELERY_BROKER_URL']
  )
  celery.conf.update(app.config)

  class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
      with app.app_context():
        return self.run(*args, **kwargs)

  celery.Task = ContextTask
  return celery

