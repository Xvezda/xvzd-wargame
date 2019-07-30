#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

import os
from flask import Flask

from common.db import db_setup


pages = ['notice', 'items', 'support']

def create_app(__name__=__name__):
  app = Flask(__name__)

  # NOTE: This is NOT a flag! >:)
  app.secret_key = os.getenv('SECRET_KEY', os.urandom(32))
  db_setup(app)

  return app
