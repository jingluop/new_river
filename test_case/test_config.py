# -*- coding: UTF-8 -*-
"""
@File    ：test_config.py
@Author  ：taofangpeng
@Date    ：2022/10/8 10:39 
"""

import os
import datetime

import pytest
from api.config import config
from common.data_load import ReadFileData, get_yaml_data
import sys

from common.db import db_mysql
from common.logger import logger
from data_calculate.sql import Sql

sys.path.extend(["D:/code/newriver_api"])

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_file_path = os.path.join(BASE_PATH, "config", "config.ini")
api_root_url = ReadFileData().load_ini(data_file_path)["host"]["api_root_url"]


class TestConfig:

    @pytest.mark.parametrize('test_data', get_yaml_data('test_config.yaml', 'get_date_button_show', db_type='mysql'))
    def test_get_date_button_show(self, test_data):
        logger.info("当前测试数据：{}".format(test_data))
        res = config.get_date_button_show(params={"configKey": test_data['configKey']})
        now = datetime.datetime.now()
        assert res['code'] == test_data['code']
        if test_data['configKey'] == '':
            min_day = []
            for time in test_data['sql_data']:
                min_time = time[0]['create_time']
                date_diff = (now - min_time).days
                min_day.append(date_diff)
            logger.info("数据查询出来的最大时间差为：{}".format(min_day))
            if min_day[0] >= 90:
                assert '3M' in res['data']['ethereum'][-1]
                assert '3M' in res['data']['transactionCount'][-1]
            elif min_day[0] >= 30:
                assert '30D' in res['data']['ethereum'][-1]
                assert '30D' in res['data']['transactionCount'][-1]
            elif min_day[0] >= 7:
                assert '7D' in res['data']['ethereum'][-1]
                assert '7D' in res['data']['transactionCount'][-1]
            else:
                assert '24H' in res['data']['ethereum'][-1]
                assert '24H' in res['data']['transactionCount'][-1]
            if min_day[1] >= 90:
                assert '3M' in res['data']['hotCollection'][-1]
                assert '3M' in res['data']['eopCollection'][-1]
                assert '3M' in res['data']['eopSales'][-1]
                assert '3M' in res['data']['top10'][-1]
                assert '3M' in res['data']['priceList'][-1]
                assert '3M' in res['data']['marketCapVolume'][-1]
            elif min_day[1] >= 30:
                assert '30D' in res['data']['hotCollection'][-1]
                assert '30D' in res['data']['eopCollection'][-1]
                assert '30D' in res['data']['eopSales'][-1]
                assert '30D' in res['data']['top10'][-1]
                assert '30D' in res['data']['priceList'][-1]
                assert '30D' in res['data']['marketCapVolume'][-1]
            elif min_day[1] >= 7:
                assert '7D' in res['data']['hotCollection'][-1]
                assert '7D' in res['data']['eopCollection'][-1]
                assert '7D' in res['data']['eopSales'][-1]
                assert '7D' in res['data']['top10'][-1]
                assert '7D' in res['data']['priceList'][-1]
                assert '7D' in res['data']['marketCapVolume'][-1]
            else:
                assert '24H' in res['data']['hotCollection'][-1]
                assert '24H' in res['data']['eopCollection'][-1]
                assert '24H' in res['data']['eopSales'][-1]
                assert '24H' in res['data']['top10'][-1]
                assert '24H' in res['data']['priceList'][-1]
                assert '24H' in res['data']['marketCapVolume'][-1]
        else:
            min_time = test_data['sql_data'][0][0]['create_time']
            date_diff = (now - min_time).days
            if date_diff >= 90:
                assert '3M' in res['data'][-1]
            elif date_diff >= 30:
                assert '30D' in res['data'][-1]
            elif date_diff >= 7:
                assert '7D' in res['data'][-1]
            else:
                assert '24H' in res['data'][-1]

    @pytest.mark.parametrize('test_data', get_yaml_data('test_config.yaml', 'check_version_update', db_type='mysql'))
    def test_check_version_update(self, test_data):
        logger.info("当前测试数据：{}".format(test_data))
        # 先查询当前版本号
        ios_need_update_version = db_mysql.select_db(Sql.version.format('iosLastNewVersion'))[0]['CONFIG_VALUE']
        ios_force_update_version = db_mysql.select_db(Sql.version.format('iosForcedUpdateVersion'))[0]['CONFIG_VALUE']
        and_need_update_version = db_mysql.select_db(Sql.version.format('andLastNewVersion'))[0]['CONFIG_VALUE']
        and_force_update_version = db_mysql.select_db(Sql.version.format('andForcedUpdateVersion'))[0]['CONFIG_VALUE']
        logger.info("ios_need_update_version：{}".format(ios_need_update_version),
                    "ios_force_update_version：{}".format(ios_force_update_version),
                    "and_need_update_version：{}".format(and_need_update_version),
                    "and_force_update_version：{}".format(and_force_update_version))
        # 算版本号
        if test_data['version'] == "equal_now_force_version":
            if test_data['terminalType'] == "IOS":
                version = ios_force_update_version
            else:
                version = and_force_update_version
        elif test_data['version'] == "above_now_force_version":
            version = '100.0.0'
        elif test_data['version'] == "equal_now_update_version":
            if test_data['terminalType'] == "IOS":
                version = ios_need_update_version
            else:
                version = and_need_update_version
        elif test_data['version'] == "above_now_update_version":
            version = '100.0.0'
        elif test_data['version'] == "below_now_force_version":
            version = '1.0.0'
        elif test_data['version'] == "below_now_update_version":
            version = '1.0.0'
        else:
            logger.info("version输入有有误")
            raise
        logger.info("当前接口入参需要输入的版本号为：{}".format(version))
        res = config.check_version_update(
            params={"version": version, "terminalType": test_data['terminalType']})
        need_update_interface = res['data']['needUpdate']
        force_update_interface = res['data']['forceUpdate']
        assert test_data['code'] == res['code']
        if 'forceUpdate' in test_data:
            assert test_data['forceUpdate'] == force_update_interface
        elif 'needUpdate' in test_data:
            assert test_data['needUpdate'] == need_update_interface
