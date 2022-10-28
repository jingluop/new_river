# -*- coding: UTF-8 -*-
"""
@File    ：overview_page.py
@Author  ：taofangpeng
@Date    ：2022/9/30 10:57 
"""
from common.db import db_mysql
from api.overview import Overview
from data_calculate.sql import BaseSql


class OverViewCal:
    time_dict = {0: 'ONE_DAY', 1: 'ONE_WEEK', 2: 'ONE_MONTH', 3: 'THREE_MONTHS'}

    def calculate_calculate_market_cap_total(self, time_type):
        """
        计算24小时的总市值
        :param time_type：0-ONE_DAY,1-ONE_WEEK,2-ONE_MONTH,3-THREE_MONTHS
        """
        last_price = float(db_mysql.select_db(BaseSql.last_price)[0]['last_price'])
        hour_dict = {0: 24, 1: 24 * 7 - 1, 2: 30 * 24, 3: 90 * 24}
        res = Overview().market_cap_and_volume_app(params={"timeRange": self.time_dict[time_type]})
        result = []
        # 1. 计算总市值
        market_cap_sql_now = float(
            db_mysql.select_db(BaseSql.total_market.format(0))[0]['market_cap'])
        market_cap_sql_before = float(
            db_mysql.select_db(BaseSql.total_market.format(hour_dict[time_type]))[0]['market_cap'])
        # 2. 总市值的变化率
        if market_cap_sql_now == market_cap_sql_before == 0:
            market_cap_rate = 0
        elif market_cap_sql_now != 0 and market_cap_sql_before == 0:
            market_cap_rate = 1
        else:
            market_cap_rate = (market_cap_sql_now - market_cap_sql_before) / market_cap_sql_before
        # 3.计算总交易量
        volume_now = float(
            db_mysql.select_db(BaseSql.total_volume.format(0))[0]['volume'])
        volume_before = float(
            db_mysql.select_db(BaseSql.total_volume.format(hour_dict[time_type]))[0]['volume'])
        # 4. 总交易量的变化率
        if volume_now == volume_before == 0:
            volume_rate = 0
        elif volume_now != 0 and volume_before == 0:
            volume_rate = 1
        else:
            volume_rate = (volume_now - volume_before) / volume_before
        result.append([(market_cap_sql_now - market_cap_sql_before) * last_price, res['data']['marketCapTotal']])
        result.append([market_cap_rate, res['data']['marketCapChange']])
        result.append([(volume_now - volume_before) * last_price, res['data']['volumeTotal']])
        result.append([volume_rate, res['data']['volumeChange']])
        return result

    def calculate_sales_top_10(self, time_type):
        """
        计算sales top10
        :param time_type：0-ONE_DAY,1-ONE_WEEK,2-ONE_MONTH,3-THREE_MONTHS
        :return:
        collection_name_interface 接口返回的集合名称
        collection_sales_interface 接口返回的交易数量
        collection_name_sql 数据库查询的集合名称
        collection_sales_sql 数据库查询的交易数量
        """
        res = Overview().top_ten_app(params={"type": "SALES", "timeRange": self.time_dict[time_type]})
        sales_top_10_interface = res['data']['sales']
        collection_name_interface = []
        collection_sales_interface = []
        for collection in sales_top_10_interface:
            collection_name_interface.append(collection['collectionName'])
            collection_sales_interface.append(collection['statisticValue'])

        sales_top_10_sql = db_mysql.select_db(BaseSql.sales_top_10.format(time_type))
        collection_name_sql = []
        collection_sales_sql = []
        for collection in sales_top_10_sql:
            collection_name_sql.append(collection['collect_name'])
            collection_sales_sql.append(collection['sales'])
        return collection_name_interface, collection_sales_interface, collection_name_sql, collection_sales_sql

    def calculate_volume_top_10(self, time_type):
        """
        计算volume top10
        :param time_type：0-ONE_DAY,1-ONE_WEEK,2-ONE_MONTH,3-THREE_MONTHS
        """
        res = Overview().top_ten_app(params={"type": "VOLUME", "timeRange": self.time_dict[time_type]})
        volume_top_10_interface = res['data']['sales']
        collection_name_interface = []
        collection_sales_interface = []
        for collection in volume_top_10_interface:
            collection_name_interface.append(collection['collectionName'])
            collection_sales_interface.append(collection['statisticValue'])

        sales_top_10_sql = db_mysql.select_db(BaseSql.sales_top_10.format(time_type))
        collection_name_sql = []
        collection_sales_sql = []
        for collection in sales_top_10_sql:
            collection_name_sql.append(collection['collect_name'])
            collection_sales_sql.append(collection['sales'])
        return collection_name_interface, collection_sales_interface, collection_name_sql, collection_sales_sql

    def calculate_heat_map(self, time_type, total_num=20):
        """
        计算首页热力图
        :param time_type：0-ONE_DAY,1-ONE_WEEK,2-ONE_MONTH,3-THREE_MONTHS
        :param total_num: 热力图总数
        :return:
        """
        res = Overview().heat_map_app(params={"dataNum": total_num, "timeRange": self.time_dict[time_type]})
        rise_list_interface = []
        fall_list_interface = []
        rise_list_interface.append(res['data']['riseList'])
        fall_list_interface.append(res['data']['fallList'])
        rise_num_sql = int(db_mysql.select_db(BaseSql.heat_map_rise_count.format(time_type))[0]['rise_count'])
        fall_num_sql = int(db_mysql.select_db(BaseSql.heat_map_fall_count.format(time_type))[0]['fall_count'])
        min_num = min(rise_num_sql, fall_num_sql)
        if min_num >= total_num / 2:
            rise_num = total_num / 2
            fall_num = total_num / 2
        else:
            if rise_num_sql == min_num:
                rise_num = rise_num_sql
                fall_num = total_num - rise_num
            else:
                fall_num = fall_num_sql
                rise_num = total_num - fall_num

        rise_list_sql = db_mysql.select_db(BaseSql.heat_map_rise.format(time_type, int(rise_num)))
        fall_list_sql = db_mysql.select_db(BaseSql.heat_map_fall.format(time_type, int(fall_num)))
        last_price = db_mysql.select_db(BaseSql.last_price)[0]['last_price']
        return rise_list_interface, fall_list_interface, rise_list_sql, fall_list_sql, last_price
