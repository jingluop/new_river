# -*- coding: UTF-8 -*-
"""
@File    ：test_overview.py
@Author  ：taofangpeng
@Date    ：2022/10/8 10:30 
"""
import os
import pytest
from api.overview import overview
from common.data_load import ReadFileData, get_yaml_data
from common.logger import logger

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_file_path = os.path.join(BASE_PATH, "config", "config.ini")
api_root_url = ReadFileData().load_ini(data_file_path)["host"]["api_root_url"]


class TestOverview:

    @pytest.mark.parametrize('test_data', get_yaml_data('test_overview.yaml', 'count_collection_num'))
    def test_count_collection_num(self, test_data):
        logger.info("测试数据为：{}".format(test_data))
        res = overview.count_collection_num()
        assert res['code'] == test_data['code']
        count_interface = res['data']
        count_sql = test_data['sql_data'][0]['count']
        logger.info("首页overview统计集合总数接口测试数据为（数据库查询，接口返回）：[{}，{}]".format(count_sql, count_interface))
        assert count_sql == count_interface

    @pytest.mark.parametrize('test_data', get_yaml_data('test_overview.yaml', 'market_cap_and_volume'))
    def test_market_cap_and_volume(self, test_data):
        logger.info("测试数据为：{}".format(test_data))
        res = overview.market_cap_and_volume_app(params={"timeRange": test_data['timeRange']} if 'timeRange' in test_data else '')
        if 'code' in test_data:
            assert test_data['code'] == res['code']
        else:
            assert test_data['status'] == res['status']

    @pytest.mark.parametrize('test_data', get_yaml_data('test_overview.yaml', 'heat_map'))
    def test_heat_map(self, test_data):
        logger.info("测试数据为：{}".format(test_data))
        res = overview.heat_map_app(params={"timeRange": test_data['timeRange']} if 'timeRange' in test_data else '')
        if 'code' in test_data:
            assert test_data['code'] == res['code']
        else:
            assert test_data['status'] == res['status']