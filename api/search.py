# -*- coding: UTF-8 -*-
"""
@File    ：search.py
@Author  ：taofangpeng
@Date    ：2022/9/14 16:07 
"""

from api.base_api import BaseApi
from common.data_load import ReadFileData


class Search(BaseApi):

    def __init__(self):
        super().__init__()
        self.api_root_url = ReadFileData().load_ini(self.data_file_path)[self.host]["api_root_url"]

    def like_collection_name(self, **kwargs):
        """全局搜索-全局搜索"""
        return self.get("/likeCollectionName", **kwargs)
