#-*- coding: utf-8 -*-
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

from model.base import select, select_all


def get_articles(board):
  fields = ['no', 'title', 'uid']
  return select_all(board, fields)

