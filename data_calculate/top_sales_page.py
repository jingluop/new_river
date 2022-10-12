# -*- coding: UTF-8 -*-
"""
@File    ：top_sales_page.py
@Author  ：taofangpeng
@Date    ：2022/9/30 10:57 
"""
import random
import pytest
from common.db import db_mysql, db_proxy
from api.top_collections import top_collections
from common.logger import logger
from data_calculate.sql import Sql


class TopSalesCal:

    def calculate_top_collection(self, time_type, page_size, page_num):
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
            json={"timeType": time_type, "pageSize": page_size, "hot": "0", "pageNum": page_num})
        result = []
        for collection in res['data']['list']:
            collection_uuid = collection['collectionUuid']

            # 1. 地板价
            logger.info(f"选取到的集合名称：{collection['collectName']}，uuid：{collection_uuid}")
            floor_price_interface = float(collection['floorPrice'])
            floor_price_sql = float(
                db_mysql.select_db(Sql.history_floor_price.format(collection_uuid, time_now))[0]['floor_price'])
            result.append([floor_price_interface, floor_price_sql])

            # 交易量
            volume_interface = float(collection['volume'])
            volume_sql = float(
                db_mysql.select_db(Sql.one_collection_volume.format(time_now, collection_uuid))[0]['volume'])
            result.append([volume_interface, volume_sql])

            # 地板价的变化率
            floor_price_change_rate_interface = float(res['data']['floorChange'])
            floor_price_now = db_mysql.select_db(Sql.history_floor_price.format(collection_uuid, time_now))[0][
                'floor_price']
            floor_price_before = db_mysql.select_db(Sql.history_floor_price.format(collection_uuid, time_before))[0][
                'floor_price']
            floor_price_change_rate_sql = float((floor_price_now - floor_price_before) / floor_price_before)
            result.append([floor_price_change_rate_interface, floor_price_change_rate_sql])

            # sales
            sales_interface = float(res['data']['sales'])
            sales_sql = db_mysql.select_db(Sql.one_collection_sales.format(collection_uuid, time_type))[0]['sales']
            result.append([sales_interface, sales_sql])
            return result