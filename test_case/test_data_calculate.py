# -*- coding: UTF-8 -*-
"""
@File    ：test_data_calculate.py
@Author  ：taofangpeng
@Date    ：2022/10/11 16:09 
"""
import random

import pytest

from common.db import db_mysql
from common.logger import logger
from data_calculate.overview_page import OverViewCal
from data_calculate.collection_details import CollectionDetailCal
from data_calculate.hot_collections_page import HotCollectionsCal
from data_calculate.sql import Sql
from data_calculate.top_collections_page import TopCollectionsCal
from data_calculate.top_sales_page import TopSalesCal


class TestCalculate:
    collection_uuid = [collection['collection_uuid'] for collection in db_mysql.select_db(Sql.collection_uuid)]
    # 随机取50个集合
    start_index = random.randint(0, len(collection_uuid) - 20)
    collection_uuid = collection_uuid[start_index: start_index + 1]
    logger.info("选取到的集合的uuid为：{}, start_index为：{}".format(collection_uuid, start_index))

    @pytest.mark.parametrize("time_type", [0])
    @pytest.mark.parametrize("page_size,page_num", [(random.randint(5, 10), random.randint(1, 3))])
    def test_top_sales(self, time_type, page_size, page_num):
        results = TopSalesCal().calculate_top_collection(time_type, page_size, page_num)
        for i in range(len(results)):
            logger.info("top sales页面测试数据为(接口返回，数据库查询)：{}------>{}".format(i, results[i]))
            for result in results[i]:
                assert result[0] == result[1]

    @pytest.mark.parametrize("time_type", [0, 1, 2, 3])
    @pytest.mark.parametrize("page_size,page_num", [(random.randint(10, 30), random.randint(1, 50))])
    def test_top_collections(self, time_type, page_size, page_num):
        results = TopCollectionsCal().calculate_top_collection(time_type, page_size, page_num)
        for i in range(len(results)):
            logger.info("top sales页面测试数据为(接口返回，数据库查询)：{}------>{}".format(i, results[i]))
            for result in results[i]:
                assert result[0] == result[1]

    @pytest.mark.parametrize("time_type", [0, 1, 2, 3])
    @pytest.mark.parametrize("page_size,page_num", [(20, 1)])
    def test_hot_collections(self, time_type, page_size, page_num):
        results = HotCollectionsCal().calculate_hot_collection(time_type, page_size, page_num)
        for i in range(len(results)):
            logger.info("top sales页面测试数据为(接口返回，数据库查询)：{}------>{}".format(i, results[i]))
            for result in results[i]:
                assert result[0] == result[1]

    @pytest.mark.parametrize("time_type", [0, 1, 2, 3])
    @pytest.mark.parametrize("collection_uuid", collection_uuid)
    def test_collection_detail(self, time_type, collection_uuid):
        results = CollectionDetailCal().calculate_collection_details(collection_uuid)
        for result in results:
            logger.info("集合详情接口测试数据接口返回：{}".format(result[0]))
            logger.info("集合详情接口测试数据sql查询：{}".format(result[1]))
            assert result[0] == result[1]

    @pytest.mark.parametrize('time_type', [0, 1, 2, 3])
    def test_sales_top_10(self, time_type):
        result = OverViewCal().calculate_sales_top_10(time_type)
        collection_name_interface = result[0]
        collection_sales_interface = result[1]
        collection_name_sql = result[2]
        collection_sales_sql = result[3]
        logger.info("overview页面sales top10测试数据接口返回：{},{}".format(result[0], result[1]))
        logger.info("overview页面sales top10测试数据sql查询：{},{}".format(result[2], result[3]))
        assert collection_name_interface == collection_name_sql
        assert collection_sales_interface == collection_sales_sql

    @pytest.mark.parametrize('time_type', [0, 1, 2, 3])
    def test_volume_top_10(self, time_type):
        result = OverViewCal().calculate_sales_top_10(time_type)
        collection_name_interface = result[0]
        collection_sales_interface = result[1]
        collection_name_sql = result[2]
        collection_sales_sql = result[3]
        logger.info("overview页面volume top10测试数据接口返回：{},{}".format(result[0], result[1]))
        logger.info("overview页面volume top10测试数据sql查询：{},{}".format(result[2], result[3]))
        assert collection_name_interface == collection_name_sql
        assert collection_sales_interface == collection_sales_sql

    @pytest.mark.parametrize('time_type', [0, 1, 2, 3])
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
        logger.info("热力图测试数据接口返回：{}".format(rise_list_interface))
        logger.info("热力图测试数据sql查询：{}".format(rise_list_sql))
        assert rise_collection_name_interface == rise_collection_name_sql
        assert rise_volume_interface == rise_volume_sql
        assert rise_change_interface == rise_change_sql
        assert fall_collection_name_interface == fall_collection_name_sql
        assert fall_volume_interface == fall_volume_sql
        assert fall_change_interface == fall_change_sql

    @pytest.mark.parametrize('collection_uuid', collection_uuid)
    def test_recent_transactions(self, collection_uuid):
        result = CollectionDetailCal().calculate_recent_transactions(collection_uuid)
        logger.info("最近交易列表测试数据接口返回：{},{}".format(result[0], result[1]))
        logger.info("最近交易列表测试数据sql查询：{},{}".format(result[2], result[3]))
        assert result[0] == result[2]
        assert result[1] == result[3]

    @pytest.mark.parametrize('time_type', [0, 1])
    @pytest.mark.parametrize('collection_uuid', collection_uuid)
    def test_floor_price_chart(self, time_type, collection_uuid):
        result = CollectionDetailCal().calculate_floor_price_chart(collection_uuid, time_type)
        logger.info("集合详情地板价图表测试数据接口返回：{},{}".format(result[0], result[1]))
        logger.info("集合详情地板价图表测试数据sql查询：{},{}".format(result[2][0], result[3][0]))
        assert result[0] == result[2][0]
        assert result[1] == result[3][0]

    @pytest.mark.parametrize('collection_uuid', collection_uuid)
    def test_analytics(self, collection_uuid):
        res = CollectionDetailCal().calculate_analytics(collection_uuid)
        res_interface = res[8]
        logger.info("集合详情analytics测试数据：{}".format(res))
        if 'blueChipVo' in res_interface['data']:
            total_holders = res[4]
            total_blue_chip_address = res[5]
            if total_holders == 0:
                total_blue_chip_address_rate = 0
                not_blue_chip_address_rate = 0
            else:
                total_blue_chip_address_rate = total_blue_chip_address / total_holders
                not_blue_chip_address_rate = (total_holders - total_blue_chip_address) / total_holders
            assert total_blue_chip_address == res['data']['holdersQuantity']
            assert total_holders - total_blue_chip_address == res['data']['noHoldersQuantity']
            assert total_blue_chip_address_rate == res['data']['holdersPercentage']
            assert not_blue_chip_address_rate == res['data']['noHoldersPercentage']
        if 'belowFloorPriceVo' in res_interface['data']:
            below_floor_price = res[0]
            above_floor_price = res[1]
            if below_floor_price + above_floor_price == 0:
                below_floor_price_rate = above_floor_price_rate = 0
            else:
                below_floor_price_rate = below_floor_price / (below_floor_price + above_floor_price)
                above_floor_price_rate = above_floor_price / (below_floor_price + above_floor_price)
            assert below_floor_price == res['data']['holdersQuantity']
            assert above_floor_price == res['data']['noHoldersQuantity']
            assert below_floor_price_rate == res['data']['holdersPercentage']
            assert above_floor_price_rate == res['data']['noHoldersPercentage']
        if 'listingVo' in res_interface['data']:
            total_listing_price = res[6]
            total_nft = res[7]
            if total_nft == 0:
                total_listing_price_rate = no_listing_price_rate = 0
            else:
                total_listing_price_rate = total_listing_price / total_nft
                no_listing_price_rate = (total_nft - total_listing_price) / total_nft
            assert total_listing_price == res['data']['holdersQuantity']
            assert total_nft - total_listing_price == res['data']['noHoldersQuantity']
            assert total_listing_price_rate == res['data']['holdersPercentage']
            assert no_listing_price_rate == res['data']['noHoldersPercentage']
        if 'tradeVO' in res_interface['data']:
            nerve_trade = res[2]
            sale_total = res[3]
            if nerve_trade + sale_total == 0:
                nerve_trade_rate = sale_total_rate = 0
            else:
                nerve_trade_rate = nerve_trade / (nerve_trade + sale_total)
                sale_total_rate = sale_total / (nerve_trade_rate + sale_total)
            assert nerve_trade == res['data']['holdersQuantity']
            assert sale_total == res['data']['noHoldersQuantity']
            assert nerve_trade_rate == res['data']['holdersPercentage']
            assert sale_total_rate == res['data']['noHoldersPercentage']

    @pytest.mark.parametrize('time_type', [0, 1, 2, 3])
    @pytest.mark.parametrize('collection_uuid', collection_uuid)
    def test_collection_details_market_cap_and_volume(self, time_type, collection_uuid):
        last_price = float(db_mysql.select_db(Sql.last_price)[0]['last_price'])
        result = CollectionDetailCal().calculate_market_cap_and_volume_one_collection(collection_uuid, time_type)
        logger.info("集合详情总市值和交易量图表测试数据接口返回：{}".format(result))
        assert (result[0] - result[1]) * last_price == result[-1]['data']['marketCapTotal']
        assert result[2] == result[-1]['data']['marketCapChange']
        assert (result[0][3] - result[4]) * last_price == result[-1]['data']['volumeTotal']
        assert result[5] == result[-1]['data']['volumeChange']

    @pytest.mark.parametrize('time_type', [0, 1, 2, 3])
    def test_overview_market_cap_and_volume(self, time_type):
        last_price = float(db_mysql.select_db(Sql.last_price)[0]['last_price'])
        result = OverViewCal().calculate_calculate_market_cap_total(time_type)
        logger.info("overview页面得总市值和交易量图表测试数据接口返回：{}".format(result))
        assert (result[0] - result[1]) * last_price == result[-1]['data']['marketCapTotal']
        assert result[2] == result[-1]['data']['marketCapChange']
        assert (result[0][3] - result[4]) * last_price == result[-1]['data']['volumeTotal']
        assert result[5] == result[-1]['data']['volumeChange']
