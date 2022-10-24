# -*- coding: UTF-8 -*-
"""
@File    ：test_top_collections.py
@Author  ：taofangpeng
@Date    ：2022/10/17 17:51 
"""
import pytest
from api.top_collections import top_collections
from common.data_load import get_yaml_data
from common.logger import logger


class TestHotCollection:

    @pytest.mark.parametrize('test_data', get_yaml_data('test_top_collections.yaml', 'get_type_str'))
    def test_get_type_str(self, test_data):
        logger.info("获取筛选类型测试数据为：{}".format(test_data))
        res = top_collections.get_type_str()
        assert test_data['code'] == res['code']
        assert test_data['sql_data'][0][0]['CONFIG_VALUE'].split(',') == res['data']['categories']
        assert test_data['sql_data'][1][0]['CONFIG_VALUE'].split(',') == res['data']['chains']
        assert test_data['sql_data'][2][0]['CONFIG_VALUE'].split(',') == res['data']['ranks']

    @pytest.mark.parametrize('test_data', get_yaml_data('test_top_collections.yaml', 'select_collection_info'))
    def test_select_collection_info(self, test_data):
        logger.info("获取筛选类型测试数据为：{}".format(test_data))
