# -*- coding: UTF-8 -*-
"""
@File    ：data_load.py
@Author  ：taofangpeng
@Date    ：2022/9/13 11:28
"""
import datetime
import random

import pytest

from common.data_load import get_yaml_data
from api.collection_details import collection_detail
from common.db import db_mysql
from common.logger import logger
from data_calculate.sql import BaseSql


class TestCollection:
    collection_uuid = [collection['collection_uuid'] for collection in db_mysql.select_db(BaseSql.collection_uuid)]
    # 随机取50个集合
    start_index = random.randint(0, len(collection_uuid) - 20)
    collection_uuid = collection_uuid[start_index: start_index + 50]
    logger.info("选取到的集合的uuid为：{}, start_index为：{}".format(collection_uuid, start_index))

    @pytest.mark.parametrize('test_data', get_yaml_data('test_collection_details.yaml', 'ethereum'))
    def test_ethereum(self, test_data):
        res = collection_detail.ethereum(params={"timeRange": test_data['timeRange'], "type": test_data['type']})
        assert res['message'] == test_data['message']
        assert res['code'] == test_data['code']
        assert res['data'][0]['countValue'] == test_data['countValue']
        assert res['data'][0]['type'] == test_data['type']
        assert res['data'][0]['date'] == test_data['date']

    @pytest.mark.parametrize("test_data", get_yaml_data('test_collection_details.yaml', 'buy_and_trade_app'))
    def test_buy_and_trade_app(self, test_data):
        res = collection_detail.buy_and_trade_app(params={"collectionUuid": test_data['collectionUuid']})
        print(test_data)
        assert res['message'] == test_data['message']
        assert test_data['sql_data'][1]['chain'] == 'ETH'

    @pytest.mark.parametrize('collection_uuid', collection_uuid)
    def test_select_collection_details(self, collection_uuid):
        st = datetime.datetime.now()
        res = collection_detail.select_collection_details_app(json={"collectionUuid": collection_uuid})
        end = datetime.datetime.now()
        print(end - st)
