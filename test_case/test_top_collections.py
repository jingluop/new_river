# -*- coding: UTF-8 -*-
"""
@File    ：test_top_collections.py
@Author  ：taofangpeng
@Date    ：2022/10/17 17:51 
"""
import os
import pytest
from api.top_collections import top_collections
from common.data_load import ReadFileData, get_yaml_data
from common.logger import logger

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_file_path = os.path.join(BASE_PATH, "config", "config.ini")
api_root_url = ReadFileData().load_ini(data_file_path)["host"]["api_root_url"]


class TestHotCollection:

    @pytest.mark.parametrize('test_data', get_yaml_data('test_hot_collections.yaml', 'get_type_str'))
    def test_get_type_str(self, test_data):
        logger.info("获取筛选类型测试数据为：{}".format(test_data))
        res = top_collections.get_type_str()
        assert test_data['code'] == res['code']
        assert test_data['sql_data'][0]['CONFIG_VALUE'].split(',') == res['data']['categories']
        assert test_data['sql_data'][1]['CONFIG_VALUE'].split(',') == res['data']['chains']
        assert test_data['sql_data'][2]['CONFIG_VALUE'].split(',') == res['data']['ranks']


