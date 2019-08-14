#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>


import sys
import time
from common.conf import *
from model.base import select, select_all
from model.base import insert


def get_endpage(board, limit=10):
  fields = ['count(*) as cnt']
  result = select_all(XVZD_PREFIX__+board, fields)
  return (int(result[0].get('cnt')) - 1) / limit + 1


def get_list(board, page=1, limit=10):
  page -= 1
  if page < 0:
    page = 1
  order = 'desc'
  page_offset = page * limit
  if page_offset > sys.maxint:
    page_offset = 0
  fields = ['no', 'title', 'uid', 'regdate', 'pinned']
  return select_all(XVZD_PREFIX__+board, fields,
                    order=order, limit='%d, %d'%(page_offset, limit))


def get_pinned(board):
  order = 'desc'
  fields = ['no', 'title', 'uid', 'regdate', 'pinned']
  return select_all(XVZD_PREFIX__+board, fields,
                    conds={'pinned': 1}, order=order)

def get_articles(board):
  order = 'desc'
  fields = ['no', 'title', 'uid', 'regdate', 'pinned']
  return select_all(XVZD_PREFIX__+board, fields, order=order)

def get_article(board, no):
  fields = ['no', 'title', 'content', 'uid', 'regdate', 'pinned']
  return select(XVZD_PREFIX__+board, fields, {'no': no})

def write_article(board, title, content, uid, ip):
  insert(XVZD_PREFIX__+board,
         ['title', 'content', 'uid', 'ip', 'regdate'],
         [title, content, uid, ip, time.strftime('%Y-%m-%d %H:%M:%S')])
