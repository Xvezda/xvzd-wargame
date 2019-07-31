#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

from common.conf import *
from common.lib import security
from model.base import select, select_all
from model.base import insert


def get_user_info(fields, conds):
  return select(XVZD_PREFIX__+'users', fields, conds)

def get_users():
  fields = ['uid', 'id', 'name', 'password']
  return select_all(XVZD_PREFIX__+'users', fields)

def insert_user(user_id, user_name, user_pw):
  insert(XVZD_PREFIX__+'users',
          ['id', 'name', 'password'],
          [user_id, user_name, user_pw])

def validate_login(user_id, user_pw):
  result = get_user_info(['password'], {'id': user_id})
  password = result.get('password') if result else None

  pw_hash = security.crypt(user_pw)

  return password == pw_hash

def get_all_notice():
  return select_all(__XVDZ_PREFIX__+'notice',
                    ['no', 'title', 'content', 'uid'])
