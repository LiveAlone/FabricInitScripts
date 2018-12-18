#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'yaoqijun'
__mail__ = 'yaoqijunmail@foxmail.com'

'''
description: 执行命令 fab -H sns-es6-node07,sns-es6-node08,sns-es6-node09,sns-es6-node10,sns-es6-node11 touchVimrc
不同的task 命令
'''

from fabric import task


@task
def settingVmMaxMapCount(ctx):
    ctx.sudo('sysctl -w vm.max_map_count=262144')


@task
def appendBashProfile(ctx):
    """
    添加 es 原型上下文配置
    :param ctx:
    :return:
    """
    result = ctx.run("echo 'export ES_JAVA_OPTS=\"-Xms28g -Xmx28g\"\n"
                     "export ES_HEAP_SIZE=28G' >> /home/app/.bash_profile ")
    print result


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


@task
def touchVimrc(ctx):
    print ctx.run("echo 'set nu\nset incsearch\nset hlsearch\nset background=dark\n' >> /home/app/.vimrc ")


@task
def validateApplimitsContent(ctx):
    pass