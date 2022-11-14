# -*- coding: UTF-8 -*-
"""
@File    ：redisdb.py
@Author  ：taofangpeng
@Date    ：2022/11/14 10:27 
"""
import os
import redis


class RedisDb:
    def __init__(self, db_conf, db):
        """
        @param db: 要选择的库的index
        @param db_conf: 配置文件键名称的前缀
        """
        from common.data_load import ReadFileData
        base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        data_file_path = os.path.join(base_path, "config", "config.ini")
        db_conf = db_conf + '-' + ReadFileData().load_ini(data_file_path)['env']['env']
        data = ReadFileData().load_ini(data_file_path)[db_conf]
        host = data['REDIS_HOST']
        port = data['REDIS_PORT']
        password = data['REDIS_PASSWD']
        conn_pool = redis.ConnectionPool(host=host, password=password, port=port, db=db)
        self.redis_conn = redis.Redis(connection_pool=conn_pool)

    def redis_get(self, key_name):
        """
        获取单个值
        @param key_name:键名称
        @return:
        """
        return self.redis_conn.get(key_name)

    def redis_mget(self, *args):
        """
        获取多个值
        @param args:键名称
        @return:
        """
        return self.redis_conn.get(args)

print(RedisDb('redis', 6).redis_get('GAS_PRICE_RECORD_KEY'))
