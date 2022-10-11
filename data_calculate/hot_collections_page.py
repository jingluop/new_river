# -*- coding: UTF-8 -*-
"""
@File    ：hot_collections_page.py
@Author  ：taofangpeng
@Date    ：2022/9/30 10:57 
"""
import random
import pytest
from common.db import db_mysql, db_proxy
from api.top_collections import top_collections
from common.logger import logger
from data_calculate.sql import Sql


class HotCollectionsCal:

    def calculate_hot_collection(self, time_type, page_size, page_num):
        if time_type == 0:
            days = 1
        elif time_type == 1:
            days = 3
        elif time_type == 2:
            days = 30
        else:
            days = 90
        time_now = 0  # 取当前时间的数据就传0
        time_before = days * 24 - 1  # 根据时间类型取之前的时间
        res = top_collections.select_collection_info(
            json={"timeType": time_type, "pageSize": page_size, "hot": "1", "pageNum": page_num})
        result = []
        for collection in res['data']['list']:
            collection_uuid = collection['collectionUuid']

            # 1. 地板价
            logger.info(f"选取到的集合名称：{collection['collectName']}，uuid：{collection_uuid}")
            floor_price_interface = float(collection['floorPrice'])
            floor_price_sql = float(
                db_mysql.select_db(Sql.history_floor_price.format(collection_uuid, time_now))[0]['floor_price'])
            result.append([floor_price_interface, floor_price_sql])

            # 持有人
            owners_interface = int(collection['numOwners'])
            owners_sql = float(
                db_mysql.select_db(Sql.one_collection_holders.format(time_now, collection_uuid))[0]['floor_price'])
            result.append([owners_interface, owners_sql])

            # 持有人变化率
            owners_change_rate_interface = int(collection['ownerThen'])
            owners_now = owners_sql
            owners_before = float(
                db_mysql.select_db(Sql.one_collection_holders.format(time_before, collection_uuid))[0]['holders'])
            owners_change_rate_sql = (owners_now - owners_before) / owners_before
            result.append([owners_change_rate_interface, owners_change_rate_sql])

            # 交易量
            volume_interface = float(collection['oneDayVolume'])
            volume_now = float(
                db_mysql.select_db(Sql.one_collection_volume.format(time_now, collection_uuid))[0]['volume'])
            volume_before = float(
                db_mysql.select_db(Sql.one_collection_volume.format(time_before, collection_uuid))[0]['volume'])
            volume_sql = volume_now - volume_before
            result.append([volume_interface, volume_sql])

            # 交易量的变化率
            volume_change_interface = float(collection['dayChange'])
            volume_change_rate_sql = (volume_now - volume_before) / volume_before
            result.append([volume_change_interface, volume_change_rate_sql])

            # 市值
            market_cap_interface = float(collection['marketCap'])
            market_cap_sql = float(
                db_mysql.select_db(Sql.one_collection_market_cap.format(time_now, collection_uuid))[0]['market_cap'])
            result.append([market_cap_interface, market_cap_sql])
            return result
