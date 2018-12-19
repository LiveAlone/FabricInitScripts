#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'yaoqijun'
__mail__ = 'yaoqijunmail@foxmail.com'

'''
description: service 集群group 构建es 集群方式
'''
from fabric import SerialGroup
from fabric import Connection

file_load_path = '/data/deploy/cellar'
deploy_hosts = ['sns-es6-node07', 'sns-es6-node08', 'sns-es6-node09', 'sns-es6-node10', 'sns-es6-node11']
es_cluster_name = 'sns-cluster'
es_cluster_node_name = 'sns-cluster-node-'


def load_es_package():
    ctx = SerialGroup(*deploy_hosts)
    ctx.run('mkdir -p %s' % file_load_path)
    ctx.run('cd %s && wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.2.2.tar.gz'
            ' -e use_proxy=yes -e http_proxy=rec-httpproxy01:3128' % file_load_path)
    ctx.run('cd %s && tar -zxvf elasticsearch-6.2.2.tar.gz' % file_load_path)


def start_server():
    source_bash_profile = 'source .bash_profile && '
    for (i, host) in enumerate(deploy_hosts):
        conn = Connection(host)
        # result = conn.run('source .bash_profile && echo $ES_JAVA_OPTS')
        # conn.run('echo "http.max_content_length: 500mb\n" '
        #          '>> /data/deploy/cellar/elasticsearch-6.2.2/config/elasticsearch.yml ')
        # conn.run('echo "cluster.name: %s\n" '
        #          '>> /data/deploy/cellar/elasticsearch-6.2.2/config/elasticsearch.yml ' % es_cluster_name)
        # conn.run('echo "node.name: %s%s\n" '
        #          '>> /data/deploy/cellar/elasticsearch-6.2.2/config/elasticsearch.yml ' % (es_cluster_node_name, i + 1))
        # conn.run('echo "transport.tcp.port: 9300\n" '
        #          '>> /data/deploy/cellar/elasticsearch-6.2.2/config/elasticsearch.yml ')
        # conn.run('echo "discovery.zen.ping.unicast.hosts: %s\n" '
        #          '>> /data/deploy/cellar/elasticsearch-6.2.2/config/elasticsearch.yml '
        #          % str(['%s:%s' % (deploy_host, 9300) for deploy_host in deploy_hosts]))
        # conn.run('echo "discovery.zen.minimum_master_nodes: %s\n" '
        #          '>> /data/deploy/cellar/elasticsearch-6.2.2/config/elasticsearch.yml '
        #          % str(len(deploy_hosts) / 2 + 1))
        # conn.run('echo "bootstrap.memory_lock: true\n" '
        #          '>> /data/deploy/cellar/elasticsearch-6.2.2/config/elasticsearch.yml ')
        # conn.run('echo "network.host: 0.0.0.0\n" '
        #          '>> /data/deploy/cellar/elasticsearch-6.2.2/config/elasticsearch.yml ')

        # start server
        conn.run('%s /data/deploy/cellar/elasticsearch-6.2.2/bin/elasticsearch -d' % source_bash_profile)


if __name__ == '__main__':
    print 'start to config elasticsearch cluster'
    start_server()
    print 'end to config elasticsearch cluster'
