#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

import functools

from flask import abort
from flask import request


def db_error_wrapper(original_func):
  @functools.wraps(original_func)
  def wrapper_func(*args, **kwargs):
    try:
      ret = original_func(*args, **kwargs)
    except:
      return abort(503, 'Looks like db server is dead.')
    return ret
  return wrapper_func
