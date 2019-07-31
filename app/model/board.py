#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

from model.base import select, select_all


def get_articles(board):
  fields = ['no', 'title', 'uid']
  return select_all(board, fields)

def get_article(board, no):
  fields = ['no', 'title', 'content', 'uid']
  return select(board, fields, {'no': no})
