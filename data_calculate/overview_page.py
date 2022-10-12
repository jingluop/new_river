# -*- coding: UTF-8 -*-
"""
@File    ：overview_page.py
@Author  ：taofangpeng
@Date    ：2022/9/30 10:57 
"""
from common.db import db_mysql
from api.overview import Overview
from data_calculate.sql import Sql


class OverViewCal:
    time_dict = {'ONE_DAY': 0, 'ONE_WEEK': 1, 'ONE_MONTH': 2, 'THREE_MONTHS': 3}

    def calculate_calculate_market_cap_total(time_type):
        """
        计算24小时的总市值
        time_type：ONE_DAY,ONE_WEEK,ONE_MONTH,THREE_MONTHS
        """
        res = Overview().market_cap_and_volume_app(params={"timeRange": time_type})
        # 接口返回的总市值
        market_cap_total_interface = res['data']['marketCapTotal']
        # 从数据库拉数据计算的总市值

    def calculate_sales_top_10(self, time_type):
        """
        计算sales top10
        :param time_type：ONE_DAY,ONE_WEEK,ONE_MONTH,THREE_MONTHS
        :return:
        collection_name_interface 接口返回的集合名称
        collection_sales_interface 接口返回的交易数量
        collection_name_sql 数据库查询的集合名称
        collection_sales_sql 数据库查询的交易数量
        """
        res = Overview().top_ten_app(params={"type": "SALES", "timeRange": time_type})
        sales_top_10_interface = res['data']['sales']
        collection_name_interface = []
        collection_sales_interface = []
        for collection in sales_top_10_interface:
            collection_name_interface.append(collection['collectionName'])
            collection_sales_interface.append(collection['statisticValue'])

        sales_top_10_sql = db_mysql.select_db(Sql.sales_top_10.format(self.time_dict[time_type]))
        collection_name_sql = []
        collection_sales_sql = []
        for collection in sales_top_10_sql:
            collection_name_sql.append(collection['collect_name'])
            collection_sales_sql.append(collection['sales'])
        return collection_name_interface, collection_sales_interface, collection_name_sql, collection_sales_sql

    def calculate_volume_top_10(self, time_type):
        """
        计算volume top10
        :param time_type：ONE_DAY,ONE_WEEK,ONE_MONTH,THREE_MONTHS
        """
        res = Overview().top_ten_app(params={"type": "VOLUME", "timeRange": time_type})
        volume_top_10_interface = res['data']['sales']
        collection_name_interface = []
        collection_sales_interface = []
        for collection in volume_top_10_interface:
            collection_name_interface.append(collection['collectionName'])
            collection_sales_interface.append(collection['statisticValue'])

        sales_top_10_sql = db_mysql.select_db(Sql.sales_top_10.format(self.time_dict[time_type]))
        collection_name_sql = []
        collection_sales_sql = []
        for collection in sales_top_10_sql:
            collection_name_sql.append(collection['collect_name'])
            collection_sales_sql.append(collection['sales'])
        return collection_name_interface, collection_sales_interface, collection_name_sql, collection_sales_sql

    def calculate_heat_map(self, time_type, total_num=20):
        """
        计算首页热力图
        :param time_type: ONE_DAY,ONE_WEEK,ONE_MONTH,THREE_MONTHS
        :param total_num: 热力图总数
        :return:
        """
        res = Overview().heat_map_app(params={"dataNum": total_num, "timeRange": time_type})
        rise_list_interface = []
        fall_list_interface = []
        rise_list_interface.append(res['data']['riseList'])
        fall_list_interface.append(res['data']['fallList'])
        rise_num_sql = int(db_mysql.select_db(Sql.heat_map_rise_count.format(self.time_dict[time_type]))[0]['rise_count'])
        fall_num_sql = int(db_mysql.select_db(Sql.heat_map_fall_count.format(self.time_dict[time_type]))[0]['fall_count'])
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

        rise_list_sql = db_mysql.select_db(Sql.heat_map_rise.format(self.time_dict[time_type], int(rise_num)))
        fall_list_sql = db_mysql.select_db(Sql.heat_map_fall.format(self.time_dict[time_type], int(fall_num)))
        last_price = db_mysql.select_db(Sql.last_price)[0]['last_price']
        return rise_list_interface, fall_list_interface, rise_list_sql, fall_list_sql, last_price





