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
        base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        data_file_path = os.path.join(base_path, "config", "config.ini")
        api_root_url = ReadFileData().load_ini(data_file_path)["host"]["api_root_url"]
        super(NftDetails, self).__init__(api_root_url)


nft_details = NftDetails()
