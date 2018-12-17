#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'yaoqijun'
__mail__ = 'yaoqijunmail@foxmail.com'

'''
description: 
'''

from fabric import task


@task
def printHostname(ctx):
    result = ctx.run('hostname')
    print result
