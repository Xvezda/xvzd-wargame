#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

import os
import re
import hashlib
import base64

from flask import session


def giveme_flag():
  if session.get('is_admin', False):
    return os.getenv('WARGAME_FLAG', 'NO_FLAG')
  else:
    return 'admin_has_real_flag_here'


def csrf_token():
  return base64.b64encode(hashlib.md5(os.urandom(32)).hexdigest())


def check_hack(target):
  pattern = r'\.|\.\.|#|--|:|\\|//|`|\$|_|\*|\||' + \
            r'union|collation|proc|php|system'
  return bool(re.findall(pattern, target, re.I))


def crypt(pw):
  return hashlib.sha512(pw.encode('utf-8')).hexdigest()
