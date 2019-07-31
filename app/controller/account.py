#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

from flask import Blueprint
from flask import abort
from flask import escape
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import session

from common.lib import security
from common.func import giveme_flag
from model.account import validate_login
from model.account import insert_user
from model.account import get_user_info


account_blueprint = Blueprint('account_blueprint', __name__)

@account_blueprint.route('/logout')
def logout():
  resp = make_response(redirect('/', code=302))
  resp.set_cookie('flag', '', expires=0)
  if session.get('is_logged'):
    session.clear()
  return resp

@account_blueprint.route('/login')
@security.csrf_token_wrapper
def login():
  return render_template('login.html')

@account_blueprint.route('/login-check', methods=['GET', 'POST'])
@security.csrf_check_wrapper
def login_check():
  require = ['user_id', 'user_pw']
  if not all(field in request.form for field in require) \
      or any(request.form[field] == '' for field in request.form):
    return abort(400, 'Something is missing!')

  user_id = request.form['user_id'].strip()
  user_pw = request.form['user_pw'].strip()

  if security.check_hack(user_id+user_pw):
    return abort(400, '')

  if validate_login(user_id, user_pw):
    session['is_logged'] = True
    session['user_id'] = user_id

    name = get_user_info(['name'], {'id': user_id}).get('name')
    session['user_name'] = name

    if user_id == 'admin' and request.remote_addr == '127.0.0.1':
      session['is_admin'] = True

    resp = make_response(redirect('/', code=302))

    # NOTE: Admin will set flag here
    resp.set_cookie('flag', giveme_flag())
    return resp
  else:
    return abort(400, """
      <script>alert('ID, PW not match!');history.back();</script>
    """)

@account_blueprint.route('/join')
@security.csrf_token_wrapper
def join():
  return render_template('join.html')

@account_blueprint.route('/join-check', methods=['GET', 'POST'])
@security.csrf_check_wrapper
def join_check():
  require = ['user_id', 'user_name', 'user_pw']
  if not all(field in request.form for field in require) \
      or any(request.form[field] == '' for field in request.form):
    return abort(400, 'Something is missing!')

  user_id = request.form['user_id'].strip()[:0x80]
  user_name = request.form['user_name'].strip()[:0x80]
  user_pw = request.form['user_pw'].strip()[:0x80]

  if security.check_hack(user_id+user_name+user_pw):
    return abort(400, '')

  ref = request.referrer if request.referrer else '/'
  if not all(security.is_valid(r'^[a-zA-Z0-9_-]+$', item)
             for item in [user_id, user_name, user_pw]):
    return abort(400, """
      <script>
        alert('ID, NAME, PW should be alpha-numeric: [a-zA-Z0-9_-]');
        location.href = '%s';
      </script>
    """ % (escape(ref)))

  user_pw = security.crypt(user_pw)

  try:
    insert_user(user_id, user_name, user_pw)
  except:
    return abort(400, """
      <script>
        alert('ID Already exists!');
        location.href = '%s';
      </script>
    """ % (escape(ref)))

  return """
    <script>alert('Welcome %s!');location.href='/';</script>
  """ % (escape(user_name))

