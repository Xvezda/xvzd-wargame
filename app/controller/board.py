#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

from flask import Blueprint
from flask import abort
from flask import render_template
from flask import request
from flask import redirect
from flask import escape
from flask import session

from common.conf import *
from common.lib import security
from model.board import get_article, get_articles
from model.board import write_article
from model.account import get_user_info


boards = XVZD_BOARDS__
board_blueprint = Blueprint('board', __name__)


@board_blueprint.route('/notice')
def notice():
  articles = get_articles('notice')
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
  articles = get_articles('support')
  users = [get_user_info(['name'], {'uid': article['uid']})
           for article in articles]
  datas = [{'article': article, 'user': user}
           for article, user in zip(articles, users)]
  return render_template('support.html', datas=datas)


@board_blueprint.route('/<board>/write')
@security.csrf_token_wrapper
def board_write(board):
  if board not in boards:
    return abort(400, '')
  return render_template('board_write.html', board=board)


@board_blueprint.route('/<board>/write-check', methods=['GET', 'POST'])
@security.form_validate_wrapper(require=['title', 'content'])
@security.csrf_check_wrapper
def board_write_check(board):
  if board not in boards:
    return abort(400, '')

  if 'user_id' not in session or not session.get('is_logged'):
    return abort(400, """
      <script>
        alert('You are not logged in!');
        location = '/login';
      </script>
    """)
  # Notice board admin only
  if (board == 'notice' and (session.get('user_id') != 'admin'
      or not session.get('is_admin') or request.remote_addr != '127.0.0.1')):
    return abort(400, '')

  title = request.form['title']
  content = request.form['content'].replace('\n', '<br>')
  uid = get_user_info(['uid'], {'id': session.get('user_id')}).get('uid')

  if security.check_hack(title, content):
    return abort(400, '')

  if not uid:
    return abort(400, 'What the hell??')

  write_article(board, title, content, uid)
  return redirect('/'+board, code=302)


@board_blueprint.route('/<board>/<int:no>')
def board_read(board, no):
  if (board not in boards or security.check_hack(board)
      or not security.is_valid(r'[a-zA-Z0-9_-]+', board)):
    return abort(400, '')
  article = get_article(board, no)
  if not article:
    return abort(404)
  return render_template('board_read.html', article=article)
