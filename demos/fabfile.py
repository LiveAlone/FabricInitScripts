#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'yaoqijun'
__mail__ = 'yaoqijunmail@foxmail.com'

'''
description: 
'''

from fabric import Connection
from fabric import task

user = 'app'
host = 'sns-es6-node01'
port = 22


@task
def uname(ctx):
    # 远程连接方式, 接口执行操作方式
    con = Connection(host=host, user=user, port=port)
    result = con.run('uname -s')
    print result

