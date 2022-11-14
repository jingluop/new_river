# -*- coding: UTF-8 -*-
"""
@File    ：collection_details.py
@Author  ：taofangpeng
@Date    ：2022/9/13 15:58
"""
from common.data_load import ReadFileData
from api.base_api import BaseApi


class CollectionDetail(BaseApi):

    def __init__(self):
        super().__init__()
        self.api_root_url = ReadFileData().load_ini(self.data_file_path)[self.host]["api_root_url"]

    def nft_pending_list(self, **kwargs):
        """集合详情-正在交易中的nf列表"""
        return self.get("/nftPendingList", **kwargs)

    def select_collection_details_app(self, **kwargs):
        """集合详情-参数collectionName"""
        return self.post("/selectCollectionDetails/app", **kwargs)

    def like_collection_name(self, **kwargs):
        """根据集合名称模糊查询集合"""
        return self.get("/likeCollectionName", **kwargs)

    def buy_and_trade_app(self, **kwargs):
        """集合详情-低价购买和交易统计图-APP"""
        return self.get("/collection/buyAndTrade/App", **kwargs)

    def recent_transactions_app(self, **kwargs):
        """集合详情-最近交易nft数组-app"""
        return self.get("/recentTransactions/app", **kwargs)

    def collection_marketcap_and_volume_app(self, **kwargs):
        """集合详情-市值与交易量-APP"""
        return self.get("/collection/marketCapAndVolume/app", **kwargs)

    def collection_floor_price_chart_app(self, **kwargs):
        """集合详情-地板价趋势图-APP"""
        return self.get("/collection/floorPriceChart/app", **kwargs)

    def get_thermodynamic_diagram_app(self, **kwargs):
        """app端-集合详情-热力图"""
        return self.get("/getThermodynamicDiagram/app", **kwargs)
