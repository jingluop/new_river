# -*- coding: UTF-8 -*-
"""
@File    ：collection_details.py
@Author  ：taofangpeng
@Date    ：2022/9/30 10:58 
"""
import random
import pytest
from common.db import db_mysql, db_proxy
from api.collection import Collection
from data_calculate.sql import Sql


class TestOverView:
    collection_uuid = [collection['collection_uuid'] for collection in db_mysql.select_db(Sql.collection_uuid)]
    start_index = random.randint(0, len(collection_uuid) - 20)
    collection_uuid = collection_uuid[start_index: start_index + 10]

    @pytest.mark.parametrize("collection_uuid", collection_uuid)
    def test_collection_details(self, collection_uuid):
        """计算集合详情页面的数据"""
        # 1.计算地板价
        # 接口返回值
        res = Collection().select_collection_details_app(json={"collectionUuid": collection_uuid})
        floor_price_interface = float(res['data']['floorPrice'])
        # 数据库查询的值
        floor_price_sql = float(db_mysql.select_db(Sql.floor_price.format(collection_uuid))[0]['floor_price'])
        assert floor_price_sql == floor_price_interface

        # 2.计算24h总交易量
        volume_interface = float(res['data']['oneDayVolume'])
        volume_now = float(
            db_mysql.select_db(Sql.one_collection_volume.format(8, collection_uuid))[0]['volume'])
        volume_24 = float(
            db_mysql.select_db(Sql.one_collection_volume.format(31, collection_uuid))[0]['volume'])
        volume_sql = volume_now - volume_24
        print(volume_interface)
        print(volume_sql)
        assert volume_interface == volume_sql

        # 3. 计算总市值
        market_cap_interface = float(res['data']['marketCap'])
        market_cap_sql = float(
            db_mysql.select_db(Sql.one_collection_market_cap.format(8, collection_uuid))[0]['market_cap'])
        print(market_cap_sql)
        print(market_cap_interface)
        assert market_cap_interface == market_cap_sql

        # 4. 计算holders
        holders_interface = float(res['data']['numOwners'])
        holders_sql = float(
            db_mysql.select_db(Sql.one_collection_holders.format(8, collection_uuid))[0]['holders'])
        print(holders_sql)
        print(holders_interface)
        assert holders_interface == holders_sql

        # 5. 计算地板价24h的变化率
        floor_price_change_rate_interface = float(res['data']['floorPriceChange'])
        floor_price_now = db_mysql.select_db(Sql.history_floor_price.format(collection_uuid, 8))[0]['floor_price']
        floor_price_24 = db_mysql.select_db(Sql.history_floor_price.format(collection_uuid, 31))[0]['floor_price']
        floor_price_change_rate_sql = float((floor_price_now - floor_price_24) / floor_price_24)
        print(floor_price_change_rate_interface)
        print(floor_price_change_rate_sql)
        assert floor_price_change_rate_interface == floor_price_change_rate_sql

        # 6. 计算24h volume变化率
        volume_change_rate_interface = float(res['data']['volumeChange'])
        volume_change_rate_sql = (volume_now - volume_24) / volume_24
        assert volume_change_rate_interface == volume_change_rate_sql

        # 7. 计算24h总市值的变化率
        market_cap_change_rate_interface = float(res['data']['marketCapChange'])
        market_cap_now = market_cap_sql
        market_cap_24 = float(
            db_mysql.select_db(Sql.one_collection_market_cap.format(31, collection_uuid))[0]['market_cap'])
        market_cap_change_rate_sql = (market_cap_now - market_cap_24) / market_cap_24
        print(market_cap_change_rate_interface)
        print(market_cap_change_rate_sql)
        assert market_cap_change_rate_sql == market_cap_change_rate_interface

        # 8. 计算24h持有人的变化率



