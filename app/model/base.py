#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

from common.db import db_connect


def select(table, fields, conds):
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

def select_all(table, fields):
  conn, cursor = db_connect()
  cursor.execute('select {} from {}'.format(', '.join(fields), table))
  result = cursor.fetchall()
  cursor.close()

  result = result if result else []
  rows = [{field: column for field, column in zip(fields, columns)}
          for columns in result]
  return rows

def insert(table, fields, values):
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

