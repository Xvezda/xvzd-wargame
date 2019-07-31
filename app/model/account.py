#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

from flask import abort

from common.db import db_connect
from common.func import crypt


def _select(table, fields, conds):
  conn, cursor = db_connect()
  cursor.execute('select {} from {} where {}'.format(
    ', '.join(fields),
    table,
    ' and '.join([
      '{} = %s'.format(field) for field, _ in conds.iteritems()
    ])
  ), *conds.values())
  result = cursor.fetchone()
  result = result if result else []
  cursor.close()

  row = {}
  for field, column in zip(fields, result):
    row[field] = column
  return row

def _select_all(table, fields):
  conn, cursor = db_connect()
  cursor.execute('select {} from {}'.format(', '.join(fields), table))
  result = cursor.fetchall()
  cursor.close()

  result = result if result else []
  rows = [{field: column for field, column in zip(fields, columns)}
          for columns in result]
  return rows

def _insert(table, fields, values):
  conn, cursor = db_connect()
  try:
    cursor.execute('''
      insert into {} ({}) values ({})
    '''.format(table, ', '.join(fields),
               ', '.join(['%s' for _ in values])
     ), tuple(values))
  except Exception as err:
    raise err
  conn.commit()
  cursor.close()

def get_user_info(fields, conds):
  return _select('xvzd_users', fields, conds)

def get_users():
  fields = ['uid', 'id', 'name', 'password']
  return _select_all('xvzd_users', fields)

def insert_user(user_id, user_name, user_pw):
  _insert('xvzd_users',
          ['id', 'name', 'password'],
          [user_id, user_name, user_pw])

def validate_login(user_id, user_pw):
  result = get_user_info(['password'], {'id': user_id})
  password = result.get('password') if result else None

  pw_hash = crypt(user_pw)

  return password == pw_hash

def get_all_notice():
  return _select_all('xvzd_notice', ['no', 'title', 'content', 'uid'])
