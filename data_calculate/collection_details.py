# -*- coding: UTF-8 -*-
"""
@File    ：collection_details.py
@Author  ：taofangpeng
@Date    ：2022/9/30 10:58 
"""
import random
import pytest
from common.db import db_mysql, db_proxy
from api.collection_details import Collection
from data_calculate.sql import Sql


class CollectionDetailCal:

    def calculate_collection_details(self, collection_uuid):
        """计算集合详情页面的数据"""
        # 1.计算地板价
        # 接口返回值
        result = []
        res = Collection().select_collection_details_app(json={"collectionUuid": collection_uuid})
        floor_price_interface = float(res['data']['floorPrice'])
        # 数据库查询的值
        floor_price_sql = float(db_mysql.select_db(Sql.floor_price.format(collection_uuid))[0]['floor_price'])
        result.append([floor_price_interface, floor_price_sql])

        # 2.计算24h总交易量
        volume_interface = float(res['data']['oneDayVolume'])
        volume_now = float(
            db_mysql.select_db(Sql.one_collection_volume.format(0, collection_uuid))[0]['volume'])
        volume_24 = float(
            db_mysql.select_db(Sql.one_collection_volume.format(23, collection_uuid))[0]['volume'])
        volume_sql = volume_now - volume_24
        result.append([volume_interface, volume_sql])

        # 3. 计算总市值
        market_cap_interface = float(res['data']['marketCap'])
        market_cap_sql = float(
            db_mysql.select_db(Sql.one_collection_market_cap.format(0, collection_uuid))[0]['market_cap'])
        result.append([market_cap_sql, market_cap_interface])

        # 4. 计算holders
        holders_interface = float(res['data']['numOwners'])
        holders_sql = float(
            db_mysql.select_db(Sql.one_collection_holders.format(0, collection_uuid))[0]['holders'])
        result.append([holders_sql, holders_interface])

        # 5. 计算地板价24h的变化率
        floor_price_change_rate_interface = float(res['data']['floorPriceChange'])
        floor_price_now = db_mysql.select_db(Sql.history_floor_price.format(collection_uuid, 0))[0]['floor_price']
        floor_price_24 = db_mysql.select_db(Sql.history_floor_price.format(collection_uuid, 23))[0]['floor_price']
        floor_price_change_rate_sql = float((floor_price_now - floor_price_24) / floor_price_24)
        result.append([floor_price_change_rate_interface, floor_price_change_rate_sql])

        # 6. 计算24h volume变化率
        volume_change_rate_interface = float(res['data']['volumeChange'])
        volume_change_rate_sql = (volume_now - volume_24) / volume_24
        result.append([volume_change_rate_interface, volume_change_rate_sql])

        # 7. 计算24h总市值的变化率
        market_cap_change_rate_interface = float(res['data']['marketCapChange'])
        market_cap_now = market_cap_sql
        market_cap_24 = float(
            db_mysql.select_db(Sql.one_collection_market_cap.format(23, collection_uuid))[0]['market_cap'])
        market_cap_change_rate_sql = (market_cap_now - market_cap_24) / market_cap_24
        result.append([market_cap_change_rate_interface, market_cap_change_rate_sql])

        # 8. 计算24h持有人的变化率
        holders_sql_change_rate_interface = float(res['data']['ownersChange'])
        holders_now = holders_sql
        holders_24 = float(
            db_mysql.select_db(Sql.one_collection_holders.format(23, collection_uuid))[0]['holders'])
        holders_change_rate_sql = (holders_now - holders_24) / holders_24
        result.append([holders_sql_change_rate_interface, holders_change_rate_sql])

        # 9. last7days折线图数据

        return result

    def calculate_recent_transactions(self, collection_uuid, limit_num=30):
        """
        计算集合详情下面的最近交易
        :param collection_uuid:
        :param limit_num:app-30，web-10
        :return:
        """
        res = Collection().recent_transactions_app(params={"collectionUuid": collection_uuid})
        recent_transactions_interface = res['data']
        recent_transactions_sql = db_proxy.select_db(Sql.recent_transactions.format(collection_uuid, limit_num))
        return recent_transactions_interface, recent_transactions_sql
