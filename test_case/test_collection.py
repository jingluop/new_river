# -*- coding: UTF-8 -*-
"""
@File    ：data_load.py
@Author  ：taofangpeng
@Date    ：2022/9/13 11:28
"""
import os
import pytest
import requests

from common.data_load import ReadFileData, get_yaml_data
from api.collection_details import collection

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_file_path = os.path.join(BASE_PATH, "config", "config.ini")
api_root_url = ReadFileData().load_ini(data_file_path)["host"]["api_root_url"]


class TestCollection:

    @pytest.mark.skip('非1.3版本迭代')
    @pytest.mark.parametrize('test_data', get_yaml_data('test_collection.yaml', 'count_collection_num'))
    def test_collection(self, test_data):
        res = collection.count_collection_num()
        assert res['data'] == test_data['count_num']

    @pytest.mark.skip('非1.3版本迭代')
    @pytest.mark.parametrize('test_data', get_yaml_data('test_collection.yaml', 'ethereum'))
    def test_ethereum(self, test_data):
        res = collection.ethereum(params={"timeRange": test_data['timeRange'], "type": test_data['type']})
        assert res['message'] == test_data['message']
        assert res['code'] == test_data['code']
        assert res['data'][0]['countValue'] == test_data['countValue']
        assert res['data'][0]['type'] == test_data['type']
        assert res['data'][0]['date'] == test_data['date']

    @pytest.mark.skip('非1.3版本迭代')
    @pytest.mark.parametrize("test_data", get_yaml_data('test_collection.yaml', 'buy_and_trade_app'))
    def test_buy_and_trade_app(self, test_data):
        res = collection.buy_and_trade_app(params={"collectionUuid": test_data['collectionUuid']})
        print(test_data)
        assert res['message'] == test_data['message']
        assert test_data['sql_data'][1]['chain'] == 'ETH'

    def test_select_collection_details(self):
        res = collection.select_collection_details(json={})
        print(res)


if __name__ == '__main__':
    pytest.main(['-sv'])