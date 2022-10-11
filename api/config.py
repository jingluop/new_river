# -*- coding: UTF-8 -*-
"""
@File    ：config.py
@Author  ：taofangpeng
@Date    ：2022/10/8 10:12 
"""
import os
from common.data_load import ReadFileData
from api.base_api import BaseApi


class Config(BaseApi):

    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        data_file_path = os.path.join(base_path, "config", "config.ini")
        api_root_url = ReadFileData().load_ini(data_file_path)["host"]["api_root_url"]
        super(Config, self).__init__(api_root_url)

    def get_date_button_show(self, **kwargs):
        """获取dateButton是否显示"""
        return self.get("/getDateButtonShow", **kwargs)

    def check_version_update(self, **kwargs):
        """检验版本号信息"""
        return self.get("/checkVersionUpdate", **kwargs)


config = Config()
