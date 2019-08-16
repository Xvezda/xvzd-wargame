#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

import os
from flask import session
from flask import request
from flask import current_app


def static_path():
  return os.path.join(current_app.root_path, 'static')

def giveme_flag():
  if session.get('is_admin', False) and request.remote_addr == '127.0.0.1':
    return os.getenv('WARGAME_FLAG', 'ERROR_NO_FLAG_ASK_ADMIN')
  return 'no cheating! please report admin about this bug.'

