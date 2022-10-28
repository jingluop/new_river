# -*- coding: UTF-8 -*-
"""
@File    ：buried_point_statistics.py
@Author  ：taofangpeng
@Date    ：2022/10/27 10:52 
"""
from api.buried_point_statistics import BuriedPointStatistics
from common.db import db_mysql
from data_calculate.sql import BuriedPointSql


class BuriedPointStatisticsCal:
    """埋点数据统计"""

    def new_user_statistics(self):
        """新用户统计"""
        res = BuriedPointStatistics().new_user(params={"type": 1, "dimensionType": "platform"})
        new_users_sql = db_mysql.select_db(BuriedPointSql.new_users.format(1, 8, ''))
        total_new_users_interface = res['data']['totalCount']
        total_new_users_sql = new_users_sql[0]['count']
        return total_new_users_interface, total_new_users_sql


BuriedPointStatisticsCal().new_user_statistics()