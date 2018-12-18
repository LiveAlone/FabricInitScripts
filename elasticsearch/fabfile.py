#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'yaoqijun'
__mail__ = 'yaoqijunmail@foxmail.com'

'''
description: 
'''

from fabric import task


@task
def appendBashProfile(ctx):
    """
    添加 es 原型上下文配置
    :param ctx:
    :return:
    """
    print 'bash profile content'


@task
def printHostname(ctx):
    """
    测试链接成功数据 hostname
    :param ctx:
    :return:
    """
    result = ctx.run('hostname')
    print result


@task
def whoami(ctx):
    print ctx.run('whoami')
