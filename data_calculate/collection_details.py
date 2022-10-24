# -*- coding: UTF-8 -*-
"""
@File    ：collection_details.py
@Author  ：taofangpeng
@Date    ：2022/9/30 10:58 
"""
import random
import pytest
from common.db import db_mysql, db_proxy
from api.collection_details import collection_detail
from data_calculate.sql import Sql


class CollectionDetailCal:
    time_dict = {0: 'ONE_DAY', 1: 'ONE_WEEK', 2: 'ONE_MONTH', 3: 'THREE_MONTHS'}

    def calculate_collection_details(self, collection_uuid):
        """计算集合详情页面的数据"""
        # 1.计算地板价
        # 接口返回值
        result = []
        res = collection_detail.select_collection_details_app(json={"collectionUuid": collection_uuid})
        floor_price_interface = float(res['data']['floorPrice'])
        # 数据库查询的值
        floor_price_sql = float(db_mysql.select_db(Sql.floor_price.format(collection_uuid))[0]['floor_price'])
        # 四舍五入保留4位小数位数
        floor_price_interface = round(floor_price_interface, 4)
        floor_price_sql = round(floor_price_sql, 4)
        result.append([res['data']['collectName'], res['data']['collectName']])
        result.append([collection_uuid, collection_uuid])
        result.append([floor_price_interface, floor_price_sql])

        # 2.计算24h总交易量
        volume_interface = float(res['data']['oneDayVolume'])
        volume_now = float(
            db_mysql.select_db(Sql.one_collection_volume.format(0, collection_uuid))[0]['volume'])
        volume_24 = float(
            db_mysql.select_db(Sql.one_collection_volume.format(23, collection_uuid))[0]['volume'])
        volume_sql = volume_now - volume_24
        # 四舍五入保留4位小数位数
        volume_interface = round(volume_interface, 4)
        volume_sql = round(volume_sql, 4)
        result.append([volume_interface, volume_sql])

        # 3. 计算总市值
        market_cap_interface = float(res['data']['marketCap'])
        market_cap_sql = float(
            db_mysql.select_db(Sql.one_collection_market_cap.format(0, collection_uuid))[0]['market_cap'])
        # 四舍五入保留4位小数位数
        market_cap_interface = round(market_cap_interface, 4)
        market_cap_sql = round(market_cap_sql, 4)
        result.append([market_cap_interface, market_cap_sql])

        # 4. 计算holders
        holders_interface = float(res['data']['numOwners'])
        holders_sql = float(
            db_mysql.select_db(Sql.one_collection_holders.format(0, collection_uuid))[0]['holders'])
        result.append([holders_interface, holders_sql])

        # 5. 计算地板价24h的变化率
        floor_price_change_rate_interface = float(res['data']['floorPriceChange'])
        floor_price_now = db_mysql.select_db(Sql.history_floor_price.format(collection_uuid, 0))[0]['floor_price']
        floor_price_24 = db_mysql.select_db(Sql.history_floor_price.format(collection_uuid, 23))[0]['floor_price']
        if floor_price_now == floor_price_24 == 0:
            floor_price_change_rate_sql = 0
        elif floor_price_now != 0 and floor_price_24 == 0:
            floor_price_change_rate_sql = 1
        else:
            floor_price_change_rate_sql = float((floor_price_now - floor_price_24) / floor_price_24)
        # 四舍五入保留4位小数位数
        floor_price_change_rate_interface = round(floor_price_change_rate_interface, 4)
        floor_price_change_rate_sql = round(floor_price_change_rate_sql, 4)
        result.append([floor_price_change_rate_interface, floor_price_change_rate_sql])

        # 6. 计算24h volume变化率
        volume_change_rate_interface = float(res['data']['volumeChange'])
        if volume_now == volume_24 == 0:
            volume_change_rate_sql = 0
        elif volume_now != 0 and volume_24 == 0:
            volume_change_rate_sql = 1
        else:
            volume_change_rate_sql = (volume_now - volume_24) / volume_24
        # 四舍五入保留4位小数位数
        volume_change_rate_interface = round(volume_change_rate_interface, 4)
        volume_change_rate_sql = round(volume_change_rate_sql, 4)
        result.append([volume_change_rate_interface, volume_change_rate_sql])

        # 7. 计算24h总市值的变化率
        market_cap_change_rate_interface = float(res['data']['marketCapChange'])
        market_cap_now = market_cap_sql
        market_cap_24 = float(
            db_mysql.select_db(Sql.one_collection_market_cap.format(23, collection_uuid))[0]['market_cap'])
        if market_cap_now == market_cap_24 == 0:
            market_cap_change_rate_sql = 0
        elif market_cap_now != 0 and market_cap_24 == 0:
            market_cap_change_rate_sql = 1
        else:
            market_cap_change_rate_sql = (market_cap_now - market_cap_24) / market_cap_24
        # 四舍五入保留4位小数位数
        market_cap_change_rate_interface = round(market_cap_change_rate_interface, 4)
        market_cap_change_rate_sql = round(market_cap_change_rate_sql, 4)
        result.append([market_cap_change_rate_interface, market_cap_change_rate_sql])

        # 8. 计算24h持有人的变化率
        holders_sql_change_rate_interface = float(res['data']['ownersChange'])
        holders_now = holders_sql
        holders_24 = float(
            db_mysql.select_db(Sql.one_collection_holders.format(23, collection_uuid))[0]['holders'])
        if holders_now == holders_24 == 0:
            holders_change_rate_sql = 0
        elif holders_now != 0 and holders_24 == 0:
            holders_change_rate_sql = 1
        else:
            holders_change_rate_sql = (holders_now - holders_24) / holders_24
        # 四舍五入保留4位小数位数
        holders_sql_change_rate_interface = round(holders_sql_change_rate_interface, 4)
        holders_change_rate_sql = round(holders_change_rate_sql, 4)
        result.append([holders_sql_change_rate_interface, holders_change_rate_sql])

        return result

    def calculate_recent_transactions(self, collection_uuid, limit_num=30):
        """
        计算集合详情下面的最近交易
        :param collection_uuid:
        :param limit_num:app-30，web-10
        :return:
        """
        res = collection_detail.recent_transactions_app(params={"collectionUuid": collection_uuid})
        recent_transactions_interface = res['data']
        recent_transactions_sql = db_proxy.select_db(Sql.recent_transactions.format(collection_uuid, limit_num))
        recent_transactions_name_interface = [i['tokenName'] for i in recent_transactions_interface]
        recent_transactions_last_price_interface = [float(i['lastPrice']) for i in recent_transactions_interface]

        recent_transactions_name_sql = [i['collection_name'] for i in recent_transactions_sql]
        recent_transactions_last_price_sql = [float(i['transaction_price']) / 1E+18 for i in recent_transactions_sql]
        return recent_transactions_name_interface, recent_transactions_last_price_interface, recent_transactions_name_sql, recent_transactions_last_price_sql

    def calculate_floor_price_chart(self, collection_uuid, time_type):
        """
        计算集合详情下面的地板价图表
        :param collection_uuid:
        :param time_type：0-ONE_DAY,1-ONE_WEEK,2-ONE_MONTH,3-THREE_MONTHS
        :return:
        """
        hour_dict = {0: 24, 1: 24 * 7 - 1, 2: 30 * 24, 3: 90 * 24}
        res = collection_detail.collection_floor_price_chart_app(
            params={"collectionUuid": collection_uuid, "timeType": self.time_dict[time_type]})
        floor_price_interface = [float(i['floorPrice']) for i in res['data']]
        avg_price_interface = [float(i['avgPrice']) for i in res['data']]
        floor_price_sql = []
        avg_price_sql = []
        floor_price = [float(i['floor_price']) for i in
                       db_mysql.select_db(
                           Sql.history_floor_price_list.format(collection_uuid, hour_dict[time_type] - 1, 0))]
        floor_price.reverse()
        avg_price = [float(i['avg_price']) for i in
                     db_mysql.select_db(Sql.avg_price_list.format(collection_uuid, hour_dict[time_type] - 1, 0))]
        avg_price.reverse()
        if time_type == 0:
            floor_price_sql.append(floor_price)
            avg_price_sql.append(avg_price)
        elif time_type == 1:
            floor_price_sql.append(floor_price[::2])
            avg_price_sql.append(avg_price[::2])
        elif time_type == 2:
            floor_price_sql.append(floor_price[::24])
            avg_price_sql.append(avg_price[::24])
        else:
            floor_price_sql.append(floor_price[::120])
            avg_price_sql.append(avg_price[::120])
        return floor_price_interface, avg_price_interface, floor_price_sql, avg_price_sql

    def calculate_market_cap_and_volume_one_collection(self, collection_uuid, time_type):
        """
        计算集合详情下面的市值和交易量的图表
        :param collection_uuid:
        :param time_type：0-ONE_DAY,1-ONE_WEEK,2-ONE_MONTH,3-THREE_MONTHS
        :return:
        """
        last_price = float(db_mysql.select_db(Sql.last_price)[0]['last_price'])
        hour_dict = {0: 24, 1: 24 * 7 - 1, 2: 30 * 24, 3: 90 * 24}
        res = collection_detail.collection_marketcap_and_volume_app(
            params={"collectionUuid": collection_uuid, "timeType": self.time_dict[time_type]})
        result = []
        # 1. 计算总市值
        market_cap_sql_now = float(
            db_mysql.select_db(Sql.one_collection_market_cap.format(0, collection_uuid))[0]['market_cap'])
        market_cap_sql_before = float(
            db_mysql.select_db(Sql.one_collection_market_cap.format(hour_dict[time_type], collection_uuid))[0][
                'market_cap'])
        # 2. 总市值的变化率
        if market_cap_sql_now == market_cap_sql_before == 0:
            market_cap_rate = 0
        elif market_cap_sql_now != 0 and market_cap_sql_before == 0:
            market_cap_rate = 1
        else:
            market_cap_rate = (market_cap_sql_now - market_cap_sql_before) / market_cap_sql_before
        # 3.计算总交易量
        volume_now = float(
            db_mysql.select_db(Sql.one_collection_volume.format(0, collection_uuid))[0]['volume'])
        volume_before = float(
            db_mysql.select_db(Sql.one_collection_volume.format(hour_dict[time_type], collection_uuid))[0]['volume'])
        # 4. 总交易量的变化率
        if volume_now == volume_before == 0:
            volume_rate = 0
        elif volume_now != 0 and volume_before == 0:
            volume_rate = 1
        else:
            volume_rate = (volume_now - volume_before) / volume_before
        result.append([(market_cap_sql_now - market_cap_sql_before) * last_price, res['data']['marketCapTotal']])
        result.append([market_cap_rate, res['data']['marketCapChange']])
        result.append([(volume_now - volume_before) * last_price, res['data']['volumeTotal']])
        result.append([volume_rate, res['data']['volumeChange']])
        return result

    def calculate_analytics(self, collection_uuid):
        """
        计算集合详情下面的市值和交易量的图表
        :param collection_uuid:
        :return:
        """
        res = collection_detail.get_thermodynamic_diagram_app(params={"collectionUuid": collection_uuid})
        # 1. 低于地板价购买
        floor_price = float(db_mysql.select_db(Sql.history_floor_price.format(collection_uuid, 0))[0]['floor_price'])
        below_floor_price = int(
            db_proxy.select_db(Sql.below_floor_price.format(collection_uuid, floor_price))[0]['count'])
        above_floor_price = int(
            db_proxy.select_db(Sql.above_floor_price.format(collection_uuid, floor_price))[0]['count'])
        # 2. 从未交易
        mint_total = int(
            db_proxy.select_db(Sql.never_traded_distribution.format(collection_uuid, 'MINT'))[0]['count'])
        sale_total = int(
            db_proxy.select_db(Sql.never_traded_distribution.format(collection_uuid, 'SALE'))[0]['count'])
        nerve_trade = mint_total - sale_total
        # 3. 蓝筹股持有人
        total_holders_address = tuple(
            [i['wallet_address'] for i in db_proxy.select_db(Sql.wallet_address.format(collection_uuid))])
        total_holders = len(total_holders_address)
        blue_chip_address = [i['wallet_address'] for i in
                             db_mysql.select_db(Sql.blue_chip_wallet_address.format(total_holders_address))]
        total_blue_chip_address = len(blue_chip_address)
        # 4. NFT in pending orders
        total_listing_price = int(db_proxy.select_db(Sql.count_listing_price.format(collection_uuid))[0]['count'])
        total_nft = int(db_mysql.select_db(Sql.total_nft.format(collection_uuid))[0]['total_nft'])
        result = []
        result.append([collection_uuid, collection_uuid])
        if 'blueChipVo' in res['data']:
            if total_holders == 0:
                total_blue_chip_address_rate = 0
                not_blue_chip_address_rate = 0
            else:
                total_blue_chip_address_rate = total_blue_chip_address / total_holders
                not_blue_chip_address_rate = (total_holders - total_blue_chip_address) / total_holders
            # 截取保留4位小数
            total_blue_chip_address_rate = int(total_blue_chip_address_rate * 10000) / 10000
            not_blue_chip_address_rate = round(not_blue_chip_address_rate, 4)
            result.append(['blueChipVo', 'blueChipVo'])
            result.append([total_blue_chip_address, res['data']['blueChipVo']['holdersQuantity']])
            result.append([total_holders - total_blue_chip_address, res['data']['blueChipVo']['noHoldersQuantity']])
            result.append([total_blue_chip_address_rate, res['data']['blueChipVo']['holdersPercentage']])
            result.append([not_blue_chip_address_rate, res['data']['blueChipVo']['noHoldersPercentage']])
        if 'belowFloorPriceVo' in res['data']:
            if below_floor_price + above_floor_price == 0:
                below_floor_price_rate = above_floor_price_rate = 0
            else:
                below_floor_price_rate = below_floor_price / (below_floor_price + above_floor_price)
                above_floor_price_rate = above_floor_price / (below_floor_price + above_floor_price)
            # 截取保留4位小数
            below_floor_price_rate = int(below_floor_price_rate * 10000) / 10000
            above_floor_price_rate = round(above_floor_price_rate, 4)
            result.append(['belowFloorPriceVo', 'belowFloorPriceVo'])
            result.append([below_floor_price, res['data']['belowFloorPriceVo']['holdersQuantity']])
            result.append([above_floor_price, res['data']['belowFloorPriceVo']['noHoldersQuantity']])
            result.append([below_floor_price_rate, res['data']['belowFloorPriceVo']['holdersPercentage']])
            result.append([above_floor_price_rate, res['data']['belowFloorPriceVo']['noHoldersPercentage']])
        if 'listingVo' in res['data']:
            if total_nft == 0:
                total_listing_price_rate = no_listing_price_rate = 0
            else:
                total_listing_price_rate = total_listing_price / total_nft
                no_listing_price_rate = (total_nft - total_listing_price) / total_nft
            # 截取保留4位小数
            total_listing_price_rate = int(total_listing_price_rate * 10000) / 10000
            no_listing_price_rate = round(no_listing_price_rate, 4)
            result.append(['listingVo', 'listingVo'])
            result.append([total_listing_price, res['data']['listingVo']['holdersQuantity']])
            result.append([total_nft - total_listing_price, res['data']['listingVo']['noHoldersQuantity']])
            result.append([total_listing_price_rate, res['data']['listingVo']['holdersPercentage']])
            result.append([no_listing_price_rate, res['data']['listingVo']['noHoldersPercentage']])
        if 'tradeVO' in res['data']:
            if nerve_trade + sale_total == 0:
                nerve_trade_rate = sale_total_rate = 0
            else:
                nerve_trade_rate = nerve_trade / (nerve_trade + sale_total)
                sale_total_rate = sale_total / (nerve_trade + sale_total)
            # 截取保留4位小数
            nerve_trade_rate = int(nerve_trade_rate * 10000) / 10000
            sale_total_rate = round(sale_total_rate, 4)
            result.append(['tradeVO', 'tradeVO'])
            result.append([nerve_trade, res['data']['tradeVO']['noHoldersQuantity']])
            result.append([sale_total, res['data']['tradeVO']['holdersQuantity']])
            result.append([nerve_trade_rate, res['data']['tradeVO']['noHoldersPercentage']])
            result.append([sale_total_rate, res['data']['tradeVO']['holdersPercentage']])

        return result
