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

    @pytest.mark.parametrize('time_type', ['ONE_DAY', 'ONE_WEEK', 'ONE_MONTH', 'THREE_MONTHS'])
    def test_sales_top_10(self, time_type):
        result = OverViewCal().calculate_sales_top_10(time_type)
        collection_name_interface = result[0]
        collection_sales_interface = result[1]
        collection_name_sql = result[2]
        collection_sales_sql = result[3]
        assert collection_name_interface == collection_name_sql
        assert collection_sales_interface == collection_sales_sql

    @pytest.mark.parametrize('time_type', ['ONE_DAY', 'ONE_WEEK', 'ONE_MONTH', 'THREE_MONTHS'])
    def test_volume_top_10(self, time_type):
        result = OverViewCal().calculate_sales_top_10(time_type)
        collection_name_interface = result[0]
        collection_sales_interface = result[1]
        collection_name_sql = result[2]
        collection_sales_sql = result[3]
        assert collection_name_interface == collection_name_sql
        assert collection_sales_interface == collection_sales_sql

    @pytest.mark.parametrize('time_type', ['ONE_DAY', 'ONE_WEEK', 'ONE_MONTH', 'THREE_MONTHS'])
    def test_heat_map(self, time_type):
        result = OverViewCal().calculate_heat_map(time_type)
        rise_list_interface = result[0][0]
        fall_list_interface = result[1][0]
        rise_list_sql = result[2]
        fall_list_sql = result[3]
        last_price = float(result[4])
        rise_collection_name_interface = [i['name'] for i in rise_list_interface]
        rise_volume_interface = [float(i['volume']) for i in rise_list_interface]
        rise_change_interface = [float(i['quoteChange']) for i in rise_list_interface]
        fall_collection_name_interface = [i['name'] for i in fall_list_interface]
        fall_volume_interface = [float(i['volume']) for i in fall_list_interface]
        fall_change_interface = [float(i['quoteChange']) for i in fall_list_interface]

        rise_collection_name_sql = [i['collect_name'] for i in rise_list_sql]
        # 截取两位小数
        rise_volume_sql = [int(float(i['volume']) * last_price * 100) / 100 for i in rise_list_sql]
        rise_change_sql = [float(i['volume_change']) for i in rise_list_sql]
        fall_collection_name_sql = [i['collect_name'] for i in fall_list_sql]
        # 截取两位小数
        fall_volume_sql = [int(float(i['volume']) * last_price * 100) / 100 for i in fall_list_sql]
        fall_change_sql = [float(i['volume_change']) for i in fall_list_sql]
        assert rise_collection_name_interface == rise_collection_name_sql
        assert rise_volume_interface == rise_volume_sql
        assert rise_change_interface == rise_change_sql
        assert fall_collection_name_interface == fall_collection_name_sql
        assert fall_volume_interface == fall_volume_sql
        assert fall_change_interface == fall_change_sql
