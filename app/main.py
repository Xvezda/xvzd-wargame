# Copyright (C) 2019 Xvezda <https://xvezda.com/>

import os

from flask import Flask
from flask import render_template, request, redirect
from flask import send_from_directory
from flask_minify import minify
from flaskext.mysql import MySQL

app = Flask(__name__)
#minify(app=app)

mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'xvzd'
app.config['MYSQL_DATABASE_PASSWORD'] = 'xvzd'
app.config['MYSQL_DATABASE_DB'] = 'xvzd_wargame'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

hack = [
  '.', '..', '#', '--', ':', '\\', '//', '`',  '$',
  '_', '*', '|', '\n', '\r', '\b', '\0', 'php', 'system',
  'union', 'collation', 'proc',
]
pages = ['notice', 'items', 'support']


@app.route('/favicon.ico')
def favicon():
  return send_from_directory(
    os.path.join(app.root_path, 'static'),
    'favicon.ico', mimetype='image/vnd.microsoft.icon'
  )

@app.route('/home')
def redir_home():
  return redirect('/', code=302)

@app.route('/')
@app.route('/<page>')
def main(page='home'):
  if any(word in page.lower() for word in hack):
    return 'No hack!', 400
  context = {
    'title': page.title(),
    'current_page': page,
    'pages': pages
  }
  return render_template('skeleton.html', **context)
  #return "Hello World from Flask"


@app.errorhandler(404)
def not_found(error):
  print dir(error)
  context = {
    'title': 'Test',
    'current_page': 'error',
    'pages': pages
  }
  return render_template('skeleton.html', **context), 404


if __name__ == "__main__":
  # Only for debugging while developing
  app.run(host='0.0.0.0', debug=True, port=8080)
