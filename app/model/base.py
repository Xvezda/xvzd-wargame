#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

from common.db import db_connect


def select(table, fields, conds):
  """Always return one row"""
  conn, cursor = db_connect()
  cursor.execute('select {} from {} where {}'.format(
    ', '.join(fields),
    table,
    ' and '.join([
      '{} = %s'.format(field) if value else '{} is %s'.format(field)
      for field, value in conds.iteritems()
    ])
  ), conds.values())
  result = cursor.fetchone()
  result = result if result else []
  cursor.close()

  row = {}
  for field, column in zip(fields, result):
    row[field] = column
  return row


def select_all(table, fields, conds={}, limit=10, order='asc'):
  """Return all result"""
  conn, cursor = db_connect()
  cursor.execute('select {} from {} {} order by 1 {} limit {}'.format(
    ', '.join(fields), table,
    'where ' + ' and '.join([
      '{} = %s'.format(field) if value else '{} is %s'.format(field)
      for field, value in conds.iteritems()
    ]) if conds else '',
    order, limit
  ), conds.values())
  result = cursor.fetchall()
  cursor.close()

  result = result if result else []
  rows = [{field.split(' as ')[-1]  # If field is alias
           if isinstance(field.split(' as '), list)
           else field: column
           for field, column in zip(fields, columns)}
          for columns in result]
  return rows


def update(table, set_values, conds={}):
  conn, cursor = db_connect()
  arguments = set_values.values() + conds.values()
  cursor.execute('update {} set {} {}'.format(
    table, ', '.join([
      '{} = %s'.format(field) for field, _ in set_values.iteritems()
    ]),
    'where ' + ' and '.join([
      '{} = %s'.format(field) for field, _ in conds.iteritems()
    ]) if conds else ''
  ), arguments)
  conn.commit()
  cursor.close()


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

