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
  h = ''.join([hashlib.md5(os.urandom(0x80)).hexdigest() for _ in range(3)])
  return base64.b64encode(h)

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

def check_hack(*args):
  # Blacklist pattern
  pattern = r'\.|\.\.|\$|\+|#|--|\\|`|_|\*|\||;|:|[box][\'"]|0[bx]|'  + \
            r'union|collation|proc|php|py|sys|style|import|select|'   + \
            r'script|src|embed|frame|object|esc|uri|eval|loc|limit|'  + \
            r'meta|input|form|html|head|body|button|table|glob|cast|' + \
            r'schema|ord|mid|column|group|dump|var|dev|root|conv|base'
  target = ''.join([arg for arg in args])
  return bool(re.findall(pattern, target, re.I))

def is_valid(pattern, target):
  return bool(re.match(pattern, target))

def form_validate_wrapper(require=[]):
  def wrapper(original_func):
    @functools.wraps(original_func)
    def wrapper_func(*args, **kwargs):
      if (not all(field in request.form for field in require)
          or any(request.form.get(field) == '' for field in require)):
        return abort(400, 'Something is missing!')
      return original_func(*args, **kwargs)
    return wrapper_func
  return wrapper

def crypt(pw):
  return hashlib.sha512(pw.encode('utf-8')).hexdigest()

