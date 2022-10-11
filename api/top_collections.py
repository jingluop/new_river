# -*- coding: UTF-8 -*-
"""
@File    ：top_collections.py
@Author  ：taofangpeng
@Date    ：2022/10/11 10:50 
"""
import os

from api.base_api import BaseApi
from common.data_load import ReadFileData


class TopCollections(BaseApi):

    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        data_file_path = os.path.join(base_path, "config", "config.ini")
        api_root_url = ReadFileData().load_ini(data_file_path)["host"]["api_root_url"]
        super(TopCollections, self).__init__(api_root_url)

    def select_collection_info(self, **kwargs):
        """获取集合列表"""
        return self.post("/selectCollectionInfo", **kwargs)


top_collections = TopCollections()
