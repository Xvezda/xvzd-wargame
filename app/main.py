#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>


import re
import os
import hashlib

from flask import Flask
from flask import session
from flask import abort
from flask import render_template, request, redirect, escape
from flask import send_from_directory
from flask import make_response
from flask_minify import minify
from flaskext.mysql import MySQL

app = Flask(__name__)
#minify(app=app)

# NOTE: This is NOT a flag! >:)
app.secret_key = os.getenv('SECRET_KEY', os.urandom(32))

mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'xvzd'
app.config['MYSQL_DATABASE_PASSWORD'] = 'xvzd'
app.config['MYSQL_DATABASE_DB'] = 'xvzd_wargame'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

pages = ['notice', 'items', 'support']


def check_hack(target):
  pattern = r'\.|\.\.|#|--|:|\\|//|`|\$|_|\*|\||' + \
            r'union|collation|proc|php|system'
  return bool(re.findall(pattern, target, re.I))

@app.route('/favicon.ico')
def favicon():
  return send_from_directory(
    os.path.join(app.root_path, 'static'),
    'favicon.ico', mimetype='image/vnd.microsoft.icon'
  )

@app.route('/home')
def redir_home():
  return redirect('/', code=302)

@app.route('/logout')
def logout():
  if session.get('is_logged'):
    session.clear()
  return redirect('/', code=302)

@app.route('/login')
def login():
  context = {
    'title': 'Login',
    'current_page': 'login',
    'pages': pages
  }
  return render_template('skeleton.html', **context)

@app.route('/login-check', methods=['GET', 'POST'])
def login_check():
  if request.method == 'POST':
    # TODO: Add login process
    require = ['user_id', 'user_pw']
    if not all(field in request.form for field in require):
      return abort(400, 'Something is missing!')

    user_id = request.form['user_id'].strip()
    user_pw = request.form['user_pw'].strip()

    if check_hack(user_id+user_pw):
      return abort(400, '')

    cursor.execute('select name, password from xvzd_users where id = %s',
                   (user_id))

    result = cursor.fetchone()
    name = result[0] if result else None
    password = result[1] if result else None

    pw_hash = hashlib.sha512(user_pw.encode('utf-8')).hexdigest()
    if password == pw_hash:
      session['is_logged'] = True
      session['user_id'] = user_id
      session['user_name'] = name

      resp = make_response(redirect('/', code=302))
      if user_id == 'admin':
        session['is_admin'] = True
      if session.get('is_admin', False):
        # If admin
        # NOTE: Admin will set flag here
        resp.set_cookie('flag',
                        os.getenv('WARGAME_FLAG', 'NO_FLAG'), httponly=True)
      else:
        resp.set_cookie('flag', 'admin_has_flag_here', httponly=True)
      return resp
    else:
      return abort(400, """
        <script>alert('ID, PW not match!');history.back();</script>
      """)
  else:
    return redirect('/', code=302)

@app.route('/join')
def join():
  context = {
    'title': 'Join',
    'current_page': 'join',
    'pages': pages
  }
  return render_template('skeleton.html', **context)

@app.route('/join-check', methods=['GET', 'POST'])
def join_check():
  if request.method == 'POST':
    require = ['user_id', 'user_name', 'user_pw']
    if not all(field in request.form for field in require):
      return abort(400, 'Something is missing!')

    user_id = request.form['user_id'].strip()[:0x80]
    user_name = request.form['user_name'].strip()[:0x80]
    user_pw = request.form['user_pw'].strip()[:0x80]

    user_pw = hashlib.sha512(user_pw.encode('utf-8')).hexdigest()

    try:
      cursor.execute('''
        insert into xvzd_users (id, name, password) values (%s, %s, %s)
      ''', (user_id, user_name, user_pw))
    except:
      return abort(400, """
        <script>alert('ID Already exists!');history.back();</script>
      """)
    conn.commit()

    return 'join', 200
  else:
    return redirect('/', code=302)

@app.route('/')
@app.route('/<page>')
def main(page='home'):
  if check_hack(page):
    return abort(400, '')
  context = {
    'title': page.title(),
    'current_page': page,
    'pages': pages
  }
  return render_template('skeleton.html', **context)

@app.errorhandler(400)
def not_found(error):
  context = {
    'title': 'Error 400',
    'current_page': '400',
    'pages': pages,
    'content': error.description
  }
  return render_template('skeleton.html', **context), 400

@app.errorhandler(404)
def not_found(error):
  context = {
    'title': 'Error 404',
    'current_page': '404',
    'pages': pages
  }
  return render_template('skeleton.html', **context), 404

@app.errorhandler(403)
def not_allowed(error):
  context = {
    'title': 'Error 403',
    'current_page': '403',
    'pages': pages
  }
  return render_template('skeleton.html', **context), 403


if __name__ == "__main__":
  # Only for debugging while developing
  app.run(host='0.0.0.0', debug=True, port=8080)
  # Close mysql connection
  cursor.close()
  conn.close()
