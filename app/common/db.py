#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

from flaskext.mysql import MySQL


mysql = MySQL()

def db_setup(app):
  app.config['MYSQL_DATABASE_USER'] = 'xvzd'
  app.config['MYSQL_DATABASE_PASSWORD'] = 'xvzd'
  app.config['MYSQL_DATABASE_DB'] = 'xvzd_wargame'
  app.config['MYSQL_DATABASE_HOST'] = 'localhost'
  mysql.init_app(app)

def db_connect():
  conn = mysql.connect()
  cursor = conn.cursor()
  return (conn, cursor)
