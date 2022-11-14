# -*- coding: UTF-8 -*-
"""
@File    ：config.py
@Author  ：taofangpeng
@Date    ：2022/10/8 10:12 
"""
from common.data_load import ReadFileData
from api.base_api import BaseApi


class Config(BaseApi):

    def __init__(self):
        super().__init__()
        self.api_root_url = ReadFileData().load_ini(self.data_file_path)[self.host]["api_root_url"]

    def get_date_button_show(self, **kwargs):
        """获取dateButton是否显示"""
        return self.get("/getDateButtonShow", **kwargs)

    def check_version_update(self, **kwargs):
        """检验版本号信息"""
        return self.get("/checkVersionUpdate", **kwargs)
