#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>


import time
from common.conf import *
from model.base import select, select_all
from model.base import insert


def get_articles(board):
  order = 'desc'
  fields = ['no', 'title', 'uid']
  return select_all(XVZD_PREFIX__+board, fields, order=order)

def get_article(board, no):
  fields = ['no', 'title', 'content', 'uid']
  return select(XVZD_PREFIX__+board, fields, {'no': no})

def write_article(board, title, content, uid):
  insert(XVZD_PREFIX__+board,
         ['title', 'content', 'uid', 'regdate'],
         [title, content, uid, time.strftime('%Y-%m-%d %H:%M:%S')])
