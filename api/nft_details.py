# -*- coding: UTF-8 -*-
"""
@File    ：nft_details.py
@Author  ：taofangpeng
@Date    ：2022/10/8 10:09 
"""
import os

from api.base_api import BaseApi
from common.data_load import ReadFileData


class NftDetails(BaseApi):

    def __init__(self):
        super().__init__()
        self.api_root_url = ReadFileData().load_ini(self.data_file_path)[self.host]["api_root_url"]


nft_details = NftDetails()
