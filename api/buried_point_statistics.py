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

    def new_user(self, **kwargs):
        """数据埋点-新用户统计"""
        return self.get("/mng/systemOperateRecord/newUserStatistics", **kwargs)

    def first_try_login_user(self, **kwargs):
        """数据埋点-首次尝试登录用户统计"""
        return self.get("/mng/systemOperateRecord/firstLoginStatistics", **kwargs)

    def pv(self, **kwargs):
        """数据埋点-PV统计"""
        return self.get("/mng/systemOperateRecord/pvStatistics", **kwargs)

    def new_register_user(self, **kwargs):
        """数据埋点-新注册用户数统计"""
        return self.get("/mng/systemOperateRecord/registerUserStatistics", **kwargs)

    def retention_user(self, **kwargs):
        """数据埋点-此次留存用户统计"""
        return self.get("/mng/systemOperateRecord/retentionUserStatistics", **kwargs)

    def user_active(self, **kwargs):
        """数据埋点-用户活跃度统计"""
        return self.get("/mng/systemOperateRecord/userActiveStatistics", **kwargs)

    def user_active_wallet(self, **kwargs):
        """数据埋点-绑定钱包活跃用户数统计"""
        return self.get("/mng/systemOperateRecord/userActiveWalletStatistics", **kwargs)

    def bind_wallet_with_nft(self, **kwargs):
        """数据埋点--新注册用户绑定钱包中有NFT的钱包用户数量按天统计"""
        return self.get("/mng/systemOperateRecord/userBindWalletHasNftStatistics", **kwargs)

    def bind_wallet(self, **kwargs):
        """数据埋点-绑定钱包用户数统计"""
        return self.get("/mng/systemOperateRecord/userWalletStatistics", **kwargs)

    def uv(self, **kwargs):
        """数据埋点-UV统计"""
        return self.get("/mng/systemOperateRecord/uvStatistics", **kwargs)
