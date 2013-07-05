#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'

'''
A WSGI app for dev.
'''

from wsgiref.simple_server import make_server

import os, logging
logging.basicConfig(level=logging.INFO)

from transwarp import web, db

def create_app():
#    from conf import dbconf
#    kwargs = dict([(s, getattr(dbconf, s)) for s in dir(dbconf) if s.startswith('DB_')])
#    dbargs = kwargs.pop('DB_ARGS', {})
    db.init(db_type = 'sqlite3', db_schema = 'weibo.db', db_host=False)
    if not os.path.isfile('weibo.db'):
      db.update('create table settings (id varchar(50) not null, value varchar(1000) not null, primary key(id))')
      db.update('create table users (id varchar(200) not null, name varchar(50) not null, image_url varchar(1000) not null, statuses_count bigint not null, friends_count bigint not null, followers_count bigint not null, verified bool not null, verified_type int not null, auth_token varchar(2000) not null, expired_time real not null, primary key(id))')
    return web.WSGIApplication(('urls',), document_root=os.path.dirname(os.path.abspath(__file__)), template_engine='jinja2', DEBUG=True)

if __name__=='__main__':
    logging.info('application will start...')
    server = make_server('127.0.0.1', 8080, create_app())
    server.serve_forever()
