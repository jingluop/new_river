# -*- coding: UTF-8 -*-
"""
@File    ：test_overview.py
@Author  ：taofangpeng
@Date    ：2022/10/8 10:30 
"""
import os
import pytest
from api.overview import overview
from common.data_load import ReadFileData

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_file_path = os.path.join(BASE_PATH, "config", "config.ini")
api_root_url = ReadFileData().load_ini(data_file_path)["host"]["api_root_url"]


class TestOverview:

    def test_count_collection_num(self):
        res = overview.count_collection_num()
        assert res['code'] == 200
        assert res['data'] == 97


if __name__ == '__main__':
    pytest.main(['-sv'])
