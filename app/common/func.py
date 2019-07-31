#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

import os
from flask import session
from flask import request
from flask import current_app


def favicon_path():
  return os.path.join(current_app.root_path, 'static')

def giveme_flag():
  if session.get('is_admin', False) and request.remote_addr == '127.0.0.1':
    return os.getenv('WARGAME_FLAG', 'NO_FLAG')
  else:
    return 'admin_has_real_flag_here'

