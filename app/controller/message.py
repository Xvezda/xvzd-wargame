#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

import json
import datetime

from flask import Blueprint
from flask import request
from flask import session
from flask import abort
from flask import render_template
from common.lib import security
from model.account import get_user_info
from model.message import send_message, get_message


import model
context = {}
context['model'] = model

message_blueprint = Blueprint('message_blueprint', __name__)

def json_default(value):
  if isinstance(value, datetime.date):
    return value.strftime('%Y-%m-%d %H:%M:%S')
  raise


@message_blueprint.route('/message')
def message():
  if not session.get('is_logged'):
    return abort(403, 'Login please')
  return render_template('message.html', **context)


@message_blueprint.route('/message/get-ajax', methods=['POST'])
@security.form_validate_wrapper(require=['no'])
def message_get():
  if not session.get('is_logged'):
    return json.dumps({
      'result': 'error',
      'data': {
        'message': 'Login please'
      }
    }), 403

  no = request.form.get('no')
  message = get_message(no)

  if not message:
    return json.dumps({
      'result': 'error',
      'data': {
        'message': 'No message!'
      }
    })

  my_uid = get_user_info(['uid'], {'id': session.get('user_id')}).get('uid')
  if message['recv_uid'] != my_uid:
    return json.dumps({
      'result': 'error',
      'data': {
        'message': 'Not your message!'
      }
    })

  return json.dumps({
    'result': 'ok',
    'data': {
      'message': message
    }
  }, default=json_default)


@message_blueprint.route('/message/send')
@security.csrf_token_wrapper
def send():
  if not session.get('is_logged'):
    return abort(403, 'Login please')
  return render_template('message_send.html', **context)


@message_blueprint.route('/message/send-check', methods=['GET', 'POST'])
@security.form_validate_wrapper(require=['to', 'content'])
@security.csrf_check_wrapper
def send_check():
  if not session.get('is_logged'):
    return abort(403, 'Login please')

  title = request.form['title'] if request.form.get('title') else 'Untitled'
  content = request.form['content']

  if session.get('user_id') != 'admin':
    content = content.replace('<', '&lt;').replace('>', '&gt;')

  if security.check_hack(title, content):
    return abort(400, '')

  target = request.form['to']
  target_type = ''

  if target[:1] == '@':  # If target identifier is name
    target = target[1:]
    target_type = 'name'
  else:
    target_type = 'id'
  cond = {target_type: target}

  target_info = get_user_info(['uid', 'id', 'name'], cond)
  target_uid = target_info.get('uid')
  if not target_uid:
    return abort(403, 'User not found!')

  sender_result = get_user_info(['uid'], {'id': session.get('user_id')})
  sender_uid = sender_result.get('uid')
  ip = request.remote_addr

  send_message(sender_uid, target_uid, title, content, ip)

  return render_template('redirect.html', script="""
    <script>
      alert('Send success!');
      location.href = '/message';
    </script>
   """)

