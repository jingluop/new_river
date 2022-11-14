# -*- coding: UTF-8 -*-
"""
@File    ：hot_collections_page.py
@Author  ：taofangpeng
@Date    ：2022/9/30 10:57 
"""
from common.db import db_mysql
from api.top_collections import TopCollections
from common.logger import logger
from data_calculate.sql import BaseSql


class HotCollectionsCal:

    def calculate_hot_collection(self, time_type, page_size, page_num):
        if time_type == 0:
            days = 1
        elif time_type == 1:
            days = 7
        elif time_type == 2:
            days = 30
        else:
            days = 90
        time_now = 0  # 取当前时间的数据就传0
        time_before = days * 24  # 根据时间类型取之前的时间
        # time_before = days * 24 - 1  # 根据时间类型取之前的时间
        # 这个时间用来计算交易量变化率
        time_rate_before = days * 2 *24
        # time_rate_before = days * 2 * 24 - 1
        res = TopCollections().select_collection_info(
            json={"timeType": time_type, "pageSize": page_size, "hot": "1", "pageNum": page_num})
        result_total = []
        for collection in res['data']['list']:
            result = []
            collection_uuid = collection['collectionUuid']

            # 1. 地板价
            logger.info(f"选取到的集合名称：{collection['collectName']}，uuid：{collection_uuid}")
            floor_price_interface = float(collection['floorPrice'])
            floor_price_sql = float(
                db_mysql.select_db(BaseSql.history_floor_price.format(collection_uuid, time_now))[0]['floor_price'])
            # 四舍五入保留4位小数位数
            floor_price_interface = round(floor_price_interface, 4)
            floor_price_sql = round(floor_price_sql, 4)
            result.append([collection['collectName'], collection['collectName']])
            result.append([collection_uuid, collection_uuid])
            result.append([floor_price_interface, floor_price_sql])

            # 2持有人
            owners_interface = int(collection['numOwners'])
            owners_sql = int(
                db_mysql.select_db(BaseSql.one_collection_holders.format(time_now + 1, collection_uuid))[0]['holders'])
            result.append([owners_interface, owners_sql])

            # 3持有人变化率
            owners_change_rate_interface = float(collection['ownerThen'])
            owners_now = owners_sql
            owners_before = float(
                db_mysql.select_db(BaseSql.one_collection_holders.format(time_before, collection_uuid))[0]['holders'])
            if owners_now == owners_before == 0:
                owners_change_rate_sql = 0.0
            elif owners_now != 0 and owners_before == 0:
                owners_change_rate_sql = 1.0
            else:
                owners_change_rate_sql = (owners_now - owners_before) / owners_before
            # 四舍五入保留4位小数位数
            owners_change_rate_interface = round(owners_change_rate_interface, 4)
            owners_change_rate_sql = round(owners_change_rate_sql, 4)
            result.append([owners_change_rate_interface, owners_change_rate_sql])

            # 4交易量
            volume_interface = float(collection['oneDayVolume'])
            volume_sql = volume_sql = float(db_mysql.select_db(BaseSql.one_collection_volume.format(time_now + 1, time_before, collection_uuid))[0]['volume'])
            # 四舍五入保留5位小数位数
            volume_interface = round(volume_interface, 5)
            volume_sql = round(volume_sql, 5)
            result.append([volume_interface, volume_sql])

            # 5交易量的变化率
            volume_change_interface = float(collection['dayChange'])
            increment_now = volume_sql
            increment_before = float(
                db_mysql.select_db(BaseSql.one_collection_volume.format(time_before + 1, time_rate_before, collection_uuid))[0]['volume'])
            if increment_now == increment_before == 0:
                volume_change_rate_sql = 0.0
            elif increment_now != 0 and increment_before == 0:
                volume_change_rate_sql = 1.0
            else:
                volume_change_rate_sql = (increment_now - increment_before) / increment_before
            # 四舍五入保留4位小数位数
            volume_change_interface = round(volume_change_interface, 4)
            volume_change_rate_sql = round(volume_change_rate_sql, 4)
            result.append([volume_change_interface, volume_change_rate_sql])

            # 6市值
            market_cap_interface = float(collection['marketCap'])
            market_cap_sql = float(
                db_mysql.select_db(BaseSql.one_collection_market_cap.format(time_now + 1, collection_uuid))[0]['market_cap'])
            # 四舍五入保留2位小数位数
            market_cap_interface = round(market_cap_interface, 2)
            market_cap_sql = round(market_cap_sql, 2)
            result.append([market_cap_interface, market_cap_sql])
            result_total.append(result)
        return result_total
