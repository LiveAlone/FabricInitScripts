#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'yaoqijun'
__mail__ = 'yaoqijunmail@foxmail.com'

'''
description: 构建Es 集群配置, 确认ssh auth 链接方式
'''
from fabric import SerialGroup
from fabric import Connection
import time

# 需要部署的集群
deploy_hosts = ['sns-es6-node17']
# 安装目录
cellar_path = '/data/deploy/cellar'
# 需要安装文件的目录 1. es-6.2.2 2. ik-6.2.2 分词
software_path = '/data/scripts/soft'
es_file = 'elasticsearch-6.5.4.tar.gz'
es_untar_dir = 'elasticsearch-6.5.4'
es_ik_file = 'elasticsearch-analysis-ik-6.5.4.zip'
es_ik_unzip_dir = 'elasticsearch'
es_cluster_name = 'sns-cluster'
es_cluster_node_name = 'sns-cluster-node-'
es_home = '%s/%s' % (cellar_path, es_untar_dir)
es_config_yaml_file = '%s/%s' % (es_home, 'config/elasticsearch.yml')


# 机器部署上下文环境
def config_env():
    ctx = SerialGroup(*deploy_hosts)
    ctx.run("whoami")
    ctx.run("hostname")
    ctx.run("echo 'set nu\nset incsearch\nset hlsearch\nset background=dark\n' >> ~/.vimrc ")
    ctx.run("echo 'export ES_JAVA_OPTS=\"-Xms28g -Xmx28g\"\n"
            "export ES_HEAP_SIZE=28G' >> /home/app/.bash_profile ")
    ctx.run('sudo sysctl -w vm.max_map_count=262144')


# 远程文件拷贝
def file_scp():
    for host in deploy_hosts:
        conn = Connection(host)
        conn.run('mkdir -p %s' % cellar_path)
        conn.put('%s/%s' % (software_path, es_file), cellar_path)
        conn.put('%s/%s' % (software_path, es_ik_file), cellar_path)
        conn.run('tar -zxvf %s -C %s' % ('%s/%s' % (cellar_path, es_file), cellar_path))
        conn.run('unzip %s -d %s' % ('%s/%s' % (cellar_path, es_ik_file), '%s/%s' % (cellar_path, es_ik_unzip_dir)))
        conn.run('mv %s %s' % ('%s/%s' % (cellar_path, es_ik_unzip_dir),
                               '%s/%s/plugins/ik' % (cellar_path, es_untar_dir)))
        # clear
        conn.run('rm %s/%s' % (cellar_path, es_file))
        conn.run('rm %s/%s' % (cellar_path, es_ik_file))


# 集群文件配置
def cluster_config_update():
    for (i, host) in enumerate(deploy_hosts):
        conn = Connection(host)
        # result = conn.run('source .bash_profile && echo $ES_JAVA_OPTS')
        conn.run('echo "http.max_content_length: 500mb\n" >> %s' % es_config_yaml_file)
        conn.run('echo "cluster.name: %s\n" >> %s' % (es_cluster_name, es_config_yaml_file))
        conn.run('echo "node.name: %s%s\n" >> %s' % (es_cluster_node_name, i + 1, es_config_yaml_file))
        conn.run('echo "transport.tcp.port: 9300\n" >> %s' % es_config_yaml_file)
        conn.run('echo "discovery.zen.ping.unicast.hosts: %s\n" >> %s'
                 % (str(['%s:%s' % (deploy_host, 9300) for deploy_host in deploy_hosts]), es_config_yaml_file))
        conn.run('echo "discovery.zen.minimum_master_nodes: %s\n" >> %s'
                 % (str(len(deploy_hosts) / 2 + 1), es_config_yaml_file))
        conn.run('echo "bootstrap.memory_lock: true\n" >> %s' % es_config_yaml_file)
        conn.run('echo "network.host: 0.0.0.0\n" >> %s\n' % es_config_yaml_file)
        conn.run('echo "indices.requests.cache.size: 8%%\n" >> %s' % es_config_yaml_file)
        conn.run('echo "indices.queries.cache.size: 40%%\n" >> %s' % es_config_yaml_file)


# 启动集群服务
def es_cluster_start():
    for host in deploy_hosts:
        conn = Connection(host)
        # start server
        conn.run('source .bash_profile && %s/bin/elasticsearch -d' % es_home)
    # 等待节点启动成功
    time.sleep(60)
    conn = Connection(deploy_hosts[0])
    result = conn.run(" curl -XGET 'http://localhost:9200/_cluster/health?pretty=true'")
    print result


# 结束集群
def es_cluster_stop():
    for host in deploy_hosts:
        conn = Connection(host)
        process_id = conn.run("jps | grep Elasticsearch | awk '{print $1}'").stdout.strip()
        if process_id:
            print 'to process kill host: %s, process_id: %s' % (host, process_id)
            conn.run('kill %s' % process_id)


if __name__ == '__main__':
    print 'start build elasticsearch cluster build'
    # config_env()
    # file_scp()
    # cluster_config_update()
    es_cluster_start()
    # es_cluster_stop()
    print 'finish build elasticsearch cluster build'


