# -*- coding: UTF-8 -*-
"""
@File    ：data_load.py
@Author  ：taofangpeng
@Date    ：2022/9/13 11:28 
"""
import pytest
from common.logger import logger
import yaml
import json
from configparser import ConfigParser
import os


class MyConfigParser(ConfigParser):
    # 重写 configparser 中的 optionxform 函数，解决 .ini 文件中的 键option 自动转为小写的问题
    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


class ReadFileData:

    def __init__(self):
        pass

    def load_yaml(self, file_path):
        logger.info("加载 {} 文件......".format(file_path))
        with open(file_path, encoding='utf-8') as f:
            data = yaml.safe_load(f)
        logger.info("读到数据 ==>>  {} ".format(data))
        return data

    def load_json(self, file_path):
        logger.info("加载 {} 文件......".format(file_path))
        with open(file_path, encoding='utf-8') as f:
            data = json.load(f)
        logger.info("读到数据 ==>>  {} ".format(data))
        return data

    def load_ini(self, file_path):
        logger.info("加载 {} 文件......".format(file_path))
        config = MyConfigParser()
        config.read(file_path, encoding="UTF-8")
        data = dict(config._sections)
        logger.info("读到数据 ==>>  {} ".format(data))
        return data


BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def get_yaml_data(yaml_file_name, interface_name, db_type='mysql'):
    try:
        data_file_path = os.path.join(BASE_PATH, "data", yaml_file_name)
        yaml_data = ReadFileData().load_yaml(data_file_path)
        for data in yaml_data[interface_name]:
            if 'execute_sql' in data:
                if db_type == 'mysql':
                    from common.db import db_mysql
                    mysql = db_mysql
                elif db_type == 'proxy':
                    from common.db import db_proxy
                    mysql = db_proxy
                data['sql_data'] = []
                for sql in data['execute_sql']:
                    db_data = mysql.select_db(sql)
                    data['sql_data'].append(db_data[0])
    except Exception as ex:
        pytest.skip(str(ex))
    else:
        return yaml_data[interface_name]
