# -*- coding: UTF-8 -*-
"""
@File    ：overview_page.py
@Author  ：taofangpeng
@Date    ：2022/9/29 11:04 
"""
# -*- coding: UTF-8 -*-

from common.data_load import ReadFileData
from api.base_api import BaseApi


class Overview(BaseApi):

    def __init__(self):
        super().__init__()
        self.api_root_url = ReadFileData().load_ini(self.data_file_path)[self.host]["api_root_url"]

    def count_collection_num(self, **kwargs):
        """统计平台收录的集合数量"""
        return self.get("/countCollectionNum", **kwargs)

    def heat_map_app(self, **kwargs):
        """APP 热力图"""
        return self.get("/heatMap/app", **kwargs)

    def market_cap_and_volume_app(self, **kwargs):
        """统计市值和交易量"""
        return self.get("/marketCapAndVolume/app", **kwargs)

    def top_ten_app(self, **kwargs):
        """top10排行app"""
        return self.get("/topTen/app", **kwargs)

    def ethereum_app(self, **kwargs):
        """以太坊看板"""
        return self.get("/ethereum/app", **kwargs)

    def gas(self, **kwargs):
        """获取gas费"""
        return self.get("/getGas", **kwargs)
