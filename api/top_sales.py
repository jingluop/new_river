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
        super().__init__()
        self.api_root_url = ReadFileData().load_ini(self.data_file_path)[self.host]["api_root_url"]

    def select_collection_info(self, **kwargs):
        """获取集合列表"""
        return self.get("/listTopSales/app", **kwargs)


top_sales = TopSales()
