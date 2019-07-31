#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

from flask import Blueprint
from flask import abort
from flask import render_template
from flask import request
from flask import redirect
from flask import escape
from flask import session

from common.lib import security
from model.board import get_articles
from model.account import get_user_info


writable = ['notice', 'support']
board_blueprint = Blueprint('board', __name__)

@board_blueprint.route('/notice')
def notice():
  articles = get_articles('xvzd_notice')
  users = [get_user_info(['name'], {'uid': article['uid']})
           for article in articles]
  datas = [{'article': article, 'user': user}
           for article, user in zip(articles, users)]
  return render_template('notice.html', datas=datas)

@board_blueprint.route('/items')
def items():
  return render_template('items.html')

@board_blueprint.route('/support')
def support():
  return render_template('support.html')

@board_blueprint.route('/<board>/write')
def board_write(board):
  if board not in writable:
    return abort(400, '')
  session['csrf_token'] = security.csrf_token()
  return render_template('board_write.html', board=board)

@board_blueprint.route('/<board>/write-check', methods=['GET', 'POST'])
@security.csrf_check_wrapper
def board_write_check(board):
  if board not in writable:
    return abort(400, '')

  ref = request.referrer if request.referrer else '/'
  if 'user_id' not in session or not session.get('is_logged'):
    return abort(400, """
      <script>
        alert('You are not logged in!');
        location = '/login';
      </script>
  """)

  # Notice board admin only
  if (board == 'notice' and session.get('user_id') != 'admin'
      or not session.get('is_admin') or request.remote_addr != '127.0.0.1'):
    return abort(400, '')

  require = ['title', 'content']
  if not all(field in require for field in request.form):
    return abort(400, 'Something is missing!')
  return 'write'

