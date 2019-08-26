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
    token = session.pop('csrf_token', None)
    if request.method == 'POST':
      if ('csrf_token' not in request.form or not token
          or request.form.get('csrf_token') != token):
        return abort(400, 'CSRF Attack detected!')
    else:
      return redirect('/', code=302)
    return original_func(*args, **kwargs)
  return wrapper_func


def check_hack(*args):
  # NOTE: Can you bypass these? ;)
  limit = 25
  target = ''.join([arg for arg in args])

  # Check abnormal numbers of special chracters
  if any(target.count(c) > limit for c in '[]()!?,.~%&=/:'):
    return True

  # Blacklist pattern
  pattern = r'@|[^\w\.]\.|\$|\+|#|-|\\|`|\'|"|_|\{|\}|\*|\||;|\^|' + \
            r'<[/\!\?%\[-]?(no)?(script|head|body|meta|form|style|php|' + \
            r'i?frame|link|object|(in|out)put|source|template|option|'  + \
            r'canvas|svg|entity|time|doc|embed|applet|html|datalist|'   + \
            r'button|keygen|(is)?index|text|map|marquee|xmp|progress)|' + \
            r'on(before|after)?((un)?load|error|focus|(hash)?change|'   + \
            r'mouse|key|(on|off)line|page|re|se|message|storage|blur|'  + \
            r'(dbl)?click|drag|scroll|wheel|context|invalid|submit|'    + \
            r'copy|cut|paste|play|stall|suspend|time|volume)|auto|src|' + \
            r'collation|proc|union|select|sys|import|ord|mid|column|'   + \
            r'insert|replace|alter|delete|update|sleep|benchmark|join|' + \
            r'esc|uri|eval|loc|limit|glob|cast|schema|group|dump|cat|'  + \
            r'dev|root|conv|base|sudo|(de)?comp|char|ascii|apache|rel|' + \
            r'chrome|console|debug|view|source|nginx|host|referr?er|'   + \
            r'into|vbs|ecma|passwd|\.(p[ly]|sh|js(on)?|css|exe)|0[bx]|' + \
            r'regexp|sub|new|string|xml|jquery|curl|gopher|[bx][0-9]|'  + \
            r'(class|id|style|role|type|target|(aria|data|attr)-\w+)='

  return bool(re.findall(pattern, target, re.I))


def purify(string):
  string = string.replace('&', '&amp;')
  string = string.replace('\n', '<br>')
  string = string.replace('  ', ' &nbsp;')
  string = re.sub(r'\.([^\s])', r'.<wbr>\1', string, re.M)
  return re.sub(r'\.\s+', r'.&nbsp;', string, re.M)


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

