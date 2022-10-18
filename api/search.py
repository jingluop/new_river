# -*- coding: UTF-8 -*-
"""
@File    ：search.py
@Author  ：taofangpeng
@Date    ：2022/9/14 16:07 
"""
import os

from api.base_api import BaseApi
from common.data_load import ReadFileData


class Search(BaseApi):

    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        data_file_path = os.path.join(base_path, "config", "config.ini")
        api_root_url = ReadFileData().load_ini(data_file_path)["host"]["api_root_url"]
        super(Search, self).__init__(api_root_url)

    def like_collection_name(self, **kwargs):
        """全局搜索-全局搜索"""
        return self.get("/likeCollectionName", **kwargs)


search = Search()
