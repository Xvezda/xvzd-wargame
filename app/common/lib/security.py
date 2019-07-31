#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

import os
import re
import hashlib
import base64
import functools

from flask import abort
from flask import session
from flask import request
from flask import redirect


def csrf_token():
  return base64.b64encode(hashlib.md5(os.urandom(32)).hexdigest())

def csrf_token_wrapper(original_func):
  @functools.wraps(original_func)
  def wrapper_func(*args, **kwargs):
    session['csrf_token'] = csrf_token()
    return original_func(*args, **kwargs)
  return wrapper_func

def csrf_check_wrapper(original_func):
  @functools.wraps(original_func)
  def wrapper_func(*args, **kwargs):
    if request.method == 'POST':
      if 'csrf_token' not in request.form \
          or 'csrf_token' not in session \
          or request.form.get('csrf_token') != session.get('csrf_token'):
        return abort(400, 'CSRF Attack detected!')
      session.pop('csrf_token')
    else:
      return redirect('/', code=302)
    return original_func(*args, **kwargs)
  return wrapper_func

def check_hack(target):
  pattern = r'\.|\.\.|#|--|:|\\|//|`|@|\$|_|\*|\||' + \
            r'0x|0b|x\'|b\'|union|collation|proc|php|system'
  return bool(re.findall(pattern, target, re.I))

def is_valid(pattern, target):
  return bool(re.match(pattern, target))

def crypt(pw):
  return hashlib.sha512(pw.encode('utf-8')).hexdigest()


