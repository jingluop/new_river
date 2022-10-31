# -*- coding: UTF-8 -*-
"""
@File    ：buried_point_statistics.py
@Author  ：taofangpeng
@Date    ：2022/10/27 10:52 
"""
import datetime

from api.buried_point_statistics import BuriedPointStatistics
from common.db import db_mysql
from data_calculate.sql import BuriedPointSql


class BuriedPointStatisticsCal:
    """埋点数据统计"""

    @staticmethod
    def get_all_day_list(params_type):
        all_day_list = []
        if params_type == 1:
            start_time = (datetime.datetime.now() - datetime.timedelta(days=7))
            end_time = (datetime.datetime.now() - datetime.timedelta(days=1))
        elif params_type == 2:
            start_time = (datetime.datetime.now() - datetime.timedelta(days=30))
            end_time = (datetime.datetime.now() - datetime.timedelta(days=1))
        elif params_type == 3:
            start_time = datetime.datetime.now().replace(day=1)
            end_time = (datetime.datetime.now() - datetime.timedelta(days=1))
        elif params_type == 4:
            start_time = (datetime.date.today().replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
            end_time = (datetime.date.today().replace(day=1) - datetime.timedelta(days=1))
        else:
            # type为5
            start_time = datetime.datetime.strptime(params['startDate'], '%Y%m%d')
            end_time = datetime.datetime.strptime(params['endDate'], '%Y%m%d')
        while start_time <= end_time:
            all_day_list.append(start_time.strftime("%Y%m%d"))
            start_time += datetime.timedelta(days=1)
        return all_day_list

    def new_user_statistics(self, interface_params, filter_condition=''):
        """
        新用户统计
        @param interface_params:接口入参
        @param filter_condition:sql筛选条件，platform,channel
        @return:
        """
        if filter_condition in ['platform', 'channel']:
            filter_condition_sql = f' {filter_condition},'
        else:
            filter_condition_sql = filter_condition
        order_condition = filter_condition_sql
        optional_field = filter_condition_sql
        # 拿两个日期之间的所有日期
        all_day_list = self.get_all_day_list(interface_params['type'])
        res = BuriedPointStatistics().new_user(params=interface_params)
        new_users_sql = db_mysql.select_db(
            BuriedPointSql.new_users.format(optional_field, all_day_list[-1], all_day_list[0], filter_condition_sql,
                                            order_condition))
        sql_result = []
        interface_result = []
        if filter_condition != '':
            platform = [
                [i for i in new_users_sql if i[filter_condition] == 1],
                [i for i in new_users_sql if i[filter_condition] == 2],
                [i for i in new_users_sql if i[filter_condition] == 3]
            ]
            for i in range(len(platform)):
                if len(platform[i]) == 0:
                    continue
                time_platform = [j['dateTime'] for j in platform[i]]
                tmp_inter = []
                for index in range(len(all_day_list)):
                    # 先处理接口返回
                    values = []
                    for data in res['data']['itemList']:
                        if data['id'] == i + 1:
                            values = data['values']
                    tmp_inter.append(
                        {filter_condition: i + 1, 'dateTime': values[index]['dateTime'],
                         'count': values[index]['count']})
                    # 处理sql返回
                    time = datetime.datetime.strptime(all_day_list[index], '%Y%m%d').strftime('%Y-%m-%d')
                    if time in time_platform:
                        continue
                    else:
                        platform[i].insert(index, {filter_condition: i + 1, 'dateTime': time, 'count': 0})
                sql_result.append(platform[i])
                # 接口返回
                interface_result.append(tmp_inter)
        else:
            platform = [i for i in new_users_sql]
            time_all = [j['dateTime'] for j in platform]
            # 先处理接口返回
            values = res['data']['itemList'][0]['values']
            # 接口返回
            interface_result.append([{'dateTime': item['dateTime'], 'count': item['count']} for item in values])
            for index in range(len(all_day_list)):
                # 处理sql返回
                time = datetime.datetime.strptime(all_day_list[index], '%Y%m%d').strftime('%Y-%m-%d')
                if time in time_all:
                    continue
                else:
                    platform[index].insert(index, {'dateTime': time, 'count': 0})
            sql_result.append(platform)
        return sql_result, interface_result

    def first_try_login_user_statistics(self, interface_params, filter_condition=''):
        """首次尝试登录用户统计"""
        if filter_condition in ['platform']:
            filter_condition_sql = f' {filter_condition},'
        else:
            filter_condition_sql = filter_condition
        order_condition = filter_condition_sql
        optional_field = filter_condition_sql
        # 拿两个日期之间的所有日期
        all_day_list = self.get_all_day_list(interface_params['type'])
        res = BuriedPointStatistics().first_try_login_user(params=interface_params)
        first_try_login_sql = db_mysql.select_db(
            BuriedPointSql.attempt_login_user.format(optional_field, all_day_list[-1], all_day_list[0],
                                                     filter_condition_sql,
                                                     order_condition))
        sql_result = []
        interface_result = []
        if filter_condition != '':
            platform = [
                [i for i in first_try_login_sql if i[filter_condition] == 1],
                [i for i in first_try_login_sql if i[filter_condition] == 2],
                [i for i in first_try_login_sql if i[filter_condition] == 3]
            ]
            for i in range(len(platform)):
                if len(platform[i]) == 0:
                    continue
                time_platform = [j['dateTime'] for j in platform[i]]
                tmp_inter = []
                for index in range(len(all_day_list)):
                    # 先处理接口返回
                    values = []
                    for data in res['data']['itemList']:
                        if data['id'] == i + 1:
                            values = data['values']
                    tmp_inter.append(
                        {filter_condition: i + 1, 'dateTime': values[index]['dateTime'],
                         'count': values[index]['count']})
                    # 处理sql返回
                    time = datetime.datetime.strptime(all_day_list[index], '%Y%m%d').strftime('%Y-%m-%d')
                    if time in time_platform:
                        continue
                    else:
                        platform[i].insert(index, {filter_condition: i + 1, 'dateTime': time, 'count': 0})
                sql_result.append(platform[i])
                # 接口返回
                interface_result.append(tmp_inter)
        else:
            platform = [i for i in first_try_login_sql]
            time_all = [j['dateTime'] for j in platform]
            # 先处理接口返回
            values = res['data']['itemList'][0]['values']
            # 接口返回
            interface_result.append([{'dateTime': item['dateTime'], 'count': item['count']} for item in values])
            for index in range(len(all_day_list)):
                # 处理sql返回
                time = datetime.datetime.strptime(all_day_list[index], '%Y%m%d').strftime('%Y-%m-%d')
                if time in time_all:
                    continue
                else:
                    platform[index].insert(index, {'dateTime': time, 'count': 0})
            sql_result.append(platform)
        return sql_result, interface_result

    def pv_statistics(self, interface_params):
        """PV统计"""
        # 拿两个日期之间的所有日期
        all_day_list = self.get_all_day_list(interface_params['type'])
        res = BuriedPointStatistics().pv(params=interface_params)
        pv_sql = db_mysql.select_db(
            BuriedPointSql.pv.format(all_day_list[-1], all_day_list[0]))
        sql_result = []
        interface_result = []
        platform = [i for i in pv_sql]
        time_all = [j['dateTime'] for j in platform]
        # 先处理接口返回
        values = res['data']['itemList'][0]['values']
        # 接口返回
        interface_result.append([{'dateTime': item['dateTime'], 'count': item['count']} for item in values])
        for index in range(len(all_day_list)):
            # 处理sql返回
            time = datetime.datetime.strptime(all_day_list[index], '%Y%m%d').strftime('%Y-%m-%d')
            if time in time_all:
                continue
            else:
                platform[index].insert(index, {'dateTime': time, 'count': 0})
        sql_result.append(platform)
        return sql_result, interface_result

    def new_register_user_statistics(self, params, filter_condition):
        """新注册用户数统计"""
        res = BuriedPointStatistics().new_user(params={"type": 1, "dimensionType": "platform"})
        new_users_sql = db_mysql.select_db(BuriedPointSql.new_users.format(1, 8, ''))
        total_new_users_interface = res['data']['totalCount']
        total_new_users_sql = new_users_sql[0]['count']
        return total_new_users_interface, total_new_users_sql

    def retention_user_statistics(self, params, filter_condition):
        """此次留存用户统计"""
        res = BuriedPointStatistics().new_user(params={"type": 1, "dimensionType": "platform"})
        new_users_sql = db_mysql.select_db(BuriedPointSql.new_users.format(1, 8, ''))
        total_new_users_interface = res['data']['totalCount']
        total_new_users_sql = new_users_sql[0]['count']
        return total_new_users_interface, total_new_users_sql

    def user_active_statistics(self, params, filter_condition):
        """用户活跃度统计"""
        res = BuriedPointStatistics().new_user(params={"type": 1, "dimensionType": "platform"})
        new_users_sql = db_mysql.select_db(BuriedPointSql.new_users.format(1, 8, ''))
        total_new_users_interface = res['data']['totalCount']
        total_new_users_sql = new_users_sql[0]['count']
        return total_new_users_interface, total_new_users_sql

    def user_active_wallet_statistics(self, params, filter_condition):
        """绑定钱包活跃用户数统计"""
        res = BuriedPointStatistics().new_user(params={"type": 1, "dimensionType": "platform"})
        new_users_sql = db_mysql.select_db(BuriedPointSql.new_users.format(1, 8, ''))
        total_new_users_interface = res['data']['totalCount']
        total_new_users_sql = new_users_sql[0]['count']
        return total_new_users_interface, total_new_users_sql

    def bind_wallet_with_nft_statistics(self, params, filter_condition):
        """新注册用户绑定钱包中有NFT的钱包用户数量按天统计"""
        res = BuriedPointStatistics().new_user(params={"type": 1, "dimensionType": "platform"})
        new_users_sql = db_mysql.select_db(BuriedPointSql.new_users.format(1, 8, ''))
        total_new_users_interface = res['data']['totalCount']
        total_new_users_sql = new_users_sql[0]['count']
        return total_new_users_interface, total_new_users_sql

    def bind_wallet_statistics(self, params, filter_condition):
        """绑定钱包用户数统计"""
        res = BuriedPointStatistics().new_user(params={"type": 1, "dimensionType": "platform"})
        new_users_sql = db_mysql.select_db(BuriedPointSql.new_users.format(1, 8, ''))
        total_new_users_interface = res['data']['totalCount']
        total_new_users_sql = new_users_sql[0]['count']
        return total_new_users_interface, total_new_users_sql

    def uv_statistics(self, interface_params):
        """UV统计"""
        # 拿两个日期之间的所有日期
        all_day_list = self.get_all_day_list(interface_params['type'])
        res = BuriedPointStatistics().uv(params=interface_params)
        uv_sql = db_mysql.select_db(
            BuriedPointSql.uv.format(all_day_list[-1], all_day_list[0]))
        sql_result = []
        interface_result = []
        platform = [i for i in uv_sql]
        time_all = [j['dateTime'] for j in platform]
        # 先处理接口返回
        values = res['data']['itemList'][0]['values']
        # 接口返回
        interface_result.append([{'dateTime': item['dateTime'], 'count': item['count']} for item in values])
        for index in range(len(all_day_list)):
            # 处理sql返回
            time = datetime.datetime.strptime(all_day_list[index], '%Y%m%d').strftime('%Y-%m-%d')
            if time in time_all:
                continue
            else:
                platform[index].insert(index, {'dateTime': time, 'count': 0})
        sql_result.append(platform)
        return sql_result, interface_result


# params = {"type": 1, "dimensionType": 'platform'}
params = {"type": 1}
res = BuriedPointStatisticsCal().uv_statistics(params)
print(res)





