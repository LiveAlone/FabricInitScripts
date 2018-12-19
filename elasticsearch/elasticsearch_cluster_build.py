#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'yaoqijun'
__mail__ = 'yaoqijunmail@foxmail.com'

'''
description: service 集群group 构建es 集群方式
'''
from fabric import SerialGroup

file_load_path = '/data/deploy/cellar'
deploy_hosts = ['sns-es6-node07', 'sns-es6-node08', 'sns-es6-node09', 'sns-es6-node10', 'sns-es6-node11']


if __name__ == '__main__':
    print 'start to config elasticsearch cluster'
    ctx = SerialGroup(*deploy_hosts)
    # ctx.run('mkdir -p %s' % file_load_path)
    ctx.cd(file_load_path)
    # ctx.run('cd %s' % file_load_path)
    ctx.run('pwd')
    # ctx.run('wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.2.2.tar.gz'
    #         ' -e use_proxy=yes -e http_proxy=rec-httpproxy01:3128')
    # init cluster content
    print 'end to config elasticsearch cluster'
