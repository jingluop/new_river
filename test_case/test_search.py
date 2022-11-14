# -*- coding: UTF-8 -*-
"""
@File    ：test_search.py
@Author  ：taofangpeng
@Date    ：2022/9/14 16:11 
"""
import pytest

from api.search import Search
from common.data_load import get_yaml_data
from common.logger import logger


class TestSearch:

    @pytest.mark.parametrize('test_data', get_yaml_data('test_search.yaml', 'like_collect_name'))
    def test_like_collection_name(self, test_data):
        logger.info("全局搜索的测试数据为：{}".format(test_data))
        res = Search().like_collection_name(
            params={"collectName": test_data['collectName']} if 'collectName' in test_data else '')
        collect_name_interface = []
        if 'collectName' in test_data:
            # 接口返回的集合名称列表
            collect_name_interface = [i['collectionName'] for i in res['data']]
        # 数据库查询的集合名称列表
        collect_name_sql = []
        if 'execute_sql' in test_data:
            collect_name_sql = [i['collect_name'] for i in test_data['sql_data'][0]]
            assert collect_name_sql == collect_name_interface
        elif 'collect_name_list' in test_data:
            collect_name_sql = test_data['collect_name_list']
            assert collect_name_sql == collect_name_interface
        if 'code' in test_data:
            assert test_data['code'] == res['code']
        else:
            assert test_data['status'] == res['status']
