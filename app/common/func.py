#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

import os
from flask import session
from flask import request
from flask import current_app
from flask import render_template as flask_render_template

import collections
import functools

# https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
class memoize(object):
  '''Decorator. Caches a function's return value each time it is called.
  If called later with the same arguments, the cached value is returned
  (not reevaluated).
  '''
  def __init__(self, func):
    self.func = func
    self.cache = {}
  def __call__(self, *args):
    if not isinstance(args, collections.Hashable):
       # uncacheable. a list, for instance.
       # better to not cache than blow up.
       return self.func(*args)
    if args in self.cache:
       return self.cache[args]
    else:
       value = self.func(*args)
       self.cache[args] = value
       return value
  def __repr__(self):
    '''Return the function's docstring.'''
    return self.func.__doc__
  def __get__(self, obj, objtype):
    '''Support instance methods.'''
    return functools.partial(self.__call__, obj)


def static_path():
  return os.path.join(current_app.root_path, 'static')


def giveme_flag():
  if session.get('is_admin', False) and request.remote_addr == '127.0.0.1':
    return os.getenv('WARGAME_FLAG', 'ERROR_NO_FLAG_ASK_ADMIN')
  return 'no cheating! please report admin about this bug.'


def render_template(*args, **kwargs):
  import time
  import model
  return flask_render_template(*args, time=time, model=model, **kwargs)
