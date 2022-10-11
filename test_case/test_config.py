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

from common.logger import logger

sys.path.extend(["D:/code/newriver_api"])

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_file_path = os.path.join(BASE_PATH, "config", "config.ini")
api_root_url = ReadFileData().load_ini(data_file_path)["host"]["api_root_url"]


class TestConfig:

    @pytest.mark.parametrize('test_data', get_yaml_data('test_config.yaml', 'get_date_button_show', db_type='mysql'))
    def test_get_date_button_show(self, test_data):
        res = config.get_date_button_show(params={"configKey": test_data['configKey']})
        now = datetime.datetime.now()
        assert res['code'] == test_data['code']
        if test_data['configKey'] == '':
            min_day = []
            for time in test_data['sql_data']:
                min_time = time['create_time']
                date_diff = (now - min_time).days
                min_day.append(date_diff)
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
            min_time = test_data['sql_data'][0]['create_time']
            date_diff = (now - min_time).days
            if date_diff >= 90:
                assert '3M' in res['data'][-1]
            elif date_diff >= 30:
                assert '30D' in res['data'][-1]
            elif date_diff >= 7:
                assert '7D' in res['data'][-1]
            else:
                assert '24H' in res['data'][-1]


if __name__ == '__main__':
    pytest.main(['-sv'])
