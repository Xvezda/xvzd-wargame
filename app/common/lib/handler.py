#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

import functools

from flask import abort
from flask import request
from flaskext.mysql import *


def db_error_wrapper(original_func):
  @functools.wraps(original_func)
  def wrapper_func(*args, **kwargs):
    try:
      ret = original_func(*args, **kwargs)
    except pymysql.InternalError:
    #except pymysql.OperationalError:
      return abort(503, 'Looks like db server is dead.')
    return ret
    #return original_func(*args, **kwargs)
  return wrapper_func
