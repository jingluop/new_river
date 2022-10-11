# -*- coding: UTF-8 -*-
"""
@File    ：overview_page.py
@Author  ：taofangpeng
@Date    ：2022/9/30 10:57 
"""
from common.db import db_mysql, db_proxy
from api.overview import Overview


class TestOverView:

    def test_calculate_market_cap_total24h(self):
        """计算24小时的总市值"""
        res = Overview().market_cap_and_volume_app(params={"timeRange": "ONE_DAY"})
        # 接口返回的总市值
        interface_maket_cap_total = res['data']['marketCapTotal']
        print(interface_maket_cap_total)
        # 从数据库拉数据计算的总市值


