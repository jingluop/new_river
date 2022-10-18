# -*- coding: UTF-8 -*-
"""
@File    ：test_search.py
@Author  ：taofangpeng
@Date    ：2022/9/14 16:11 
"""
import pytest

from api.search import search
from common.data_load import get_yaml_data
from common.logger import logger


class TestSearch:

    @pytest.mark.parametrize('test_data', get_yaml_data('test_search.yaml', 'like_collect_name'))
    def test_like_collection_name(self, test_data):
        logger.info("全局搜索的测试数据为：{}".format(test_data))
        res = search.like_collection_name(params={"collectName": test_data['collectName']})
        # 接口返回的集合名称列表
        collect_name_interface = [i['collectionName'] for i in res['data']]
        # 数据库查询的集合名称列表
        collect_name_sql = [i['collect_name'] for i in test_data['sql_data']]
        assert collect_name_sql == collect_name_interface
