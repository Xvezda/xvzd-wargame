#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>


import sys
from common.conf import *
from model.base import select, select_all
from model.base import insert


def get_message_count(uid, limit=10):
  fields = ['count(*) as cnt']
  result = select_all(XVZD_PREFIX__+'message', fields)
  return result[0].get('cnt')


def get_messages(uid, page, limit=10):
  page -= 1
  if page < 0:
    page = 1
  page_offset = page * limit
  if page_offset > sys.maxint:
    page_offset = 0
  fields = ['no', 'recv_uid', 'send_uid', 'readed', 'title', 'content',
            'regdate']
  return select_all(XVZD_PREFIX__+'message', fields, {'recv_uid': uid},
                    limit='%d, %d'%(page_offset, limit))


def get_message(no):
  fields = ['no', 'recv_uid', 'send_uid', 'readed', 'title', 'content',
            'regdate']
  return select(XVZD_PREFIX__+'message', fields, {'no': no})


def send_message(send_uid, recv_uid, title, content, ip):
  insert(XVZD_PREFIX__+'message',
         ['recv_uid', 'send_uid', 'title', 'content', 'ip'],
         [recv_uid, send_uid, title, content, ip])
