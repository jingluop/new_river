# -*- coding: UTF-8 -*-
"""
@File    ：test_data_calculate.py
@Author  ：taofangpeng
@Date    ：2022/10/11 16:09 
"""
import random

import pytest

from common.db import db_mysql
from data_calculate.overview_page import OverViewCal
from data_calculate.collection_details import CollectionDetailCal
from data_calculate.hot_collections_page import HotCollectionsCal
from data_calculate.sql import Sql
from data_calculate.top_collections_page import TopCollectionsCal
from data_calculate.top_sales_page import TopSalesCal


@pytest.mark.parametrize("time_type", [0, 1, 2, 3])
@pytest.mark.parametrize("page_size,page_num", [(20, 1)])
class TestCalculate:
    collection_uuid = [collection['collection_uuid'] for collection in db_mysql.select_db(Sql.collection_uuid)]
    # 随机取10个集合
    start_index = random.randint(0, len(collection_uuid) - 20)
    collection_uuid = collection_uuid[start_index: start_index + 10]

    @pytest.mark.parametrize("time_type", [0, 1, 2, 3])
    @pytest.mark.parametrize("page_size,page_num", [(random.randint(10, 30), random.randint(1, 3))])
    def test_top_sales(self, time_type, page_size, page_num):
        result = TopSalesCal().calculate_top_collection(time_type, page_size, page_num)
        print(result)

    @pytest.mark.parametrize("time_type", [0, 1, 2, 3])
    @pytest.mark.parametrize("page_size,page_num", [(random.randint(10, 30), random.randint(1, 50))])
    def test_top_collections(self, time_type, page_size, page_num):
        result = TopCollectionsCal().calculate_top_collection(time_type, page_size, page_num)
        print(result)

    @pytest.mark.parametrize("time_type", [0, 1, 2, 3])
    @pytest.mark.parametrize("page_size,page_num", [(20, 1)])
    def test_hot_collections(self, time_type, page_size, page_num):
        result = HotCollectionsCal().calculate_hot_collection(time_type, page_size, page_num)
        print(result)

    @pytest.mark.parametrize("time_type", [0, 1, 2, 3])
    @pytest.mark.parametrize("collection_uuid", collection_uuid)
    def test_collection_detail(self, time_type, collection_uuid):
        result = CollectionDetailCal().calculate_collection_details(collection_uuid)
        print(result)

    def test_market_cap(self):
        result = OverViewCal().calculate_calculate_market_cap_total()
        print(result)
