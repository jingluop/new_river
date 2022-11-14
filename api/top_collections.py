# -*- coding: UTF-8 -*-
"""
@File    ：top_collections.py
@Author  ：taofangpeng
@Date    ：2022/10/11 10:50 
"""

from api.base_api import BaseApi
from common.data_load import ReadFileData


class TopCollections(BaseApi):

    def __init__(self):
        super().__init__()
        self.api_root_url = ReadFileData().load_ini(self.data_file_path)[self.host]["api_root_url"]

    def select_collection_info(self, **kwargs):
        """获取集合列表"""
        return self.post("/selectCollectionInfo", **kwargs)

    def get_type_str(self, **kwargs):
        """获取配置的集合查询类型"""
        return self.get("/getTypeStr", **kwargs)
