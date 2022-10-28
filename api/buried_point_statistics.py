# -*- coding: UTF-8 -*-
"""
@File    ：buried_point_statistics.py
@Author  ：taofangpeng
@Date    ：2022/10/27 10:52 
"""
from common.data_load import ReadFileData
from api.base_api import BaseApi


class BuriedPointStatistics(BaseApi):

    def __init__(self):
        super().__init__()
        self.api_root_url = ReadFileData().load_ini(self.data_file_path)[self.host]["api_background_url"]

    def new_user_statistics(self, **kwargs):
        """数据埋点-新用户统计"""
        return self.get("/mng/systemOperateRecord/newUserStatistics", **kwargs)