# -*- coding: UTF-8 -*-
"""
@File    ：top_sales.py
@Author  ：taofangpeng
@Date    ：2022/10/11 15:40 
"""
import os

from api.base_api import BaseApi
from common.data_load import ReadFileData


class TopSales(BaseApi):

    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        data_file_path = os.path.join(base_path, "config", "config.ini")
        api_root_url = ReadFileData().load_ini(data_file_path)["host"]["api_root_url"]
        super(TopSales, self).__init__(api_root_url)

    def select_collection_info(self, **kwargs):
        """获取集合列表"""
        return self.post("/listTopSales/app", **kwargs)


top_sales = TopSales()
