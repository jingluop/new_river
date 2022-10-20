# -*- coding: UTF-8 -*-
"""
@File    ：top_sales_page.py
@Author  ：taofangpeng
@Date    ：2022/9/30 10:57 
"""
import random
import pytest

from api.top_sales import top_sales
from common.db import db_mysql
from common.logger import logger
from data_calculate.sql import Sql


class TopSalesCal:
    time_dict = {0: 'ONE_DAY', 1: 'ONE_WEEK', 2: 'ONE_MONTH', 3: 'THREE_MONTHS'}

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
        res = top_sales.select_collection_info(
            params={"timeRange": self.time_dict[time_type], "pageSize": page_size, "pageNum": page_num})
        result_total = []
        for collection in res['data']['list']:
            result = []
            collection_uuid = collection['collectionUuid']

            # 1. 地板价
            logger.info(f"选取到的集合名称：{collection['collectName']}，uuid：{collection_uuid}")
            floor_price_interface = float(collection['floorPrice'])
            floor_price_sql = float(
                db_mysql.select_db(Sql.history_floor_price.format(collection_uuid, time_now))[0]['floor_price'])
            # 四舍五入保留3位小数位数
            floor_price_interface = round(floor_price_interface, 3)
            floor_price_sql = round(floor_price_sql, 3)
            result.append([collection['collectName'], collection['collectName']])
            result.append([collection_uuid, collection_uuid])
            result.append([floor_price_interface, floor_price_sql])

            # 交易量
            volume_interface = float(collection['volume'])
            volume_now = float(
                db_mysql.select_db(Sql.one_collection_volume.format(time_now, collection_uuid))[0]['volume'])
            volume_before = float(
                db_mysql.select_db(Sql.one_collection_volume.format(time_before, collection_uuid))[0]['volume'])
            volume_sql = volume_now - volume_before
            # # 截取小数位数
            # volume_sql = int(volume_sql * 100000) / 100000
            # 四舍五入保留5位小数位数
            volume_sql = round(volume_sql, 5)
            volume_interface = round(volume_interface, 5)
            result.append([volume_interface, volume_sql])

            # 地板价的变化率
            floor_price_change_rate_interface = float(collection['floorChange'])
            floor_price_now = float(db_mysql.select_db(Sql.history_floor_price.format(collection_uuid, time_now))[0][
                'floor_price'])
            floor_price_before = float(db_mysql.select_db(Sql.history_floor_price.format(collection_uuid, time_before))[0][
                'floor_price'])
            if floor_price_before == floor_price_now == 0:
                floor_price_change_rate_sql = 0.0
            elif floor_price_now != 0 and floor_price_before == 0:
                floor_price_change_rate_sql = 1.0
            else:
                floor_price_change_rate_sql = float((floor_price_now - floor_price_before) / floor_price_before)
            # 四舍五入保留5位小数位数
            floor_price_change_rate_sql = round(floor_price_change_rate_sql, 5)
            floor_price_change_rate_interface = round(floor_price_change_rate_interface, 5)
            result.append([floor_price_change_rate_interface, floor_price_change_rate_sql])

            # sales
            sales_interface = int(collection['sales'])
            sales_sql = int(db_mysql.select_db(Sql.one_collection_sales.format(collection_uuid, time_type))[0]['sales'])
            result.append([sales_interface, sales_sql])
            result_total.append(result)
        return result_total
