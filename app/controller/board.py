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
from common.lib import handler
from common.lib import security
from model.board import get_article, write_article
from model.account import get_user_info

import model.board as mboard
import model.account as maccount


boards = XVZD_BOARDS__
board_blueprint = Blueprint('board', __name__)

context = {}
context['mboard'] = mboard
context['maccount'] = maccount

@board_blueprint.route('/about')
@handler.db_error_wrapper
def about():
  return render_template('about.html', **context)


@board_blueprint.route('/notice')
@handler.db_error_wrapper
def notice():
  return render_template('notice.html', **context)


@board_blueprint.route('/pricing')
def pricing():
  return render_template('pricing.html', **context)


@board_blueprint.route('/qna')
@handler.db_error_wrapper
def qna():
  return render_template('qna.html', **context)


@board_blueprint.route('/forum')
@handler.db_error_wrapper
def forum():
  return render_template('forum.html', **context)


@board_blueprint.route('/<board>/write')
@security.csrf_token_wrapper
def board_write(board):
  if board not in boards:
    return abort(400, '')
  return render_template('board_write.html', board=board)


@board_blueprint.route('/<board>/write-check', methods=['GET', 'POST'])
@handler.db_error_wrapper
@security.form_validate_wrapper(require=['title', 'content'])
@security.csrf_check_wrapper
def board_write_check(board):
  if board not in boards:
    return abort(400, '')

  if not session.get('is_logged'):
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
  # Let's limit length to 128
  if len(content) >= 0x80:
    return abort(400, 'Max length of content limited to 128 bytes!')
  uid = get_user_info(['uid'], {'id': session.get('user_id')}).get('uid')

  if security.check_hack(title, content):
    return abort(400, '')

  if not uid:
    return abort(400, 'What the hell??')

  ip = request.remote_addr
  write_article(board, title, content, uid, ip)

  return redirect('/'+board, code=302)


@board_blueprint.route('/<board>/<int:no>')
@handler.db_error_wrapper
def board_read(board, no):
  if (board not in boards or security.check_hack(board)
      or not security.is_valid(r'[a-zA-Z0-9_-]+', board)):
    return abort(400, '')
  article = get_article(board, no)
  if not article:
    return abort(404)

  # Check permission on qna board
  if board == 'qna':
    if not article.get('pinned'):
      user_id = get_user_info(['id'], {'uid': article.get('uid')}).get('id')
      is_writer = (session.get('user_id') == user_id)
      if not session.get('is_logged'):
        return abort(403, 'You are not logged in!')
      if (not session.get('is_admin') and request.remote_addr != '127.0.0.1'
          and not is_writer):
        return abort(403, 'You are not admin!')

  return render_template('board_read.html', article=article, board=board)
