# -*- coding: UTF-8 -*-
"""
@File    ：sql.py
@Author  ：taofangpeng
@Date    ：2022/10/10 10:01 
"""


class Sql:
    # 集合详情查询地板价
    floor_price = """SELECT floor_price FROM `hk-manhattan`.chain_collection WHERE collection_uuid = {}"""

    # 查询现有的所有集合的uuid
    collection_uuid = """SELECT distinct collection_uuid  FROM `hk-manhattan`.chain_collection_quotation"""

    # 计算单个集合的总交易量
    one_collection_volume = """
        select
            sum(volume) volume
        from
            `hk-manhattan`.chain_collection_quotation ccq
        where
            create_time = str_to_date( date_format( DATE_sub(CURRENT_TIMESTAMP(), interval {} hour), '%Y-%m-%d %H'),
            '%Y-%m-%d %H%i%m')
            and collection_uuid = {}
    """

    # 计算单个集合的总市值
    one_collection_market_cap = """
        select
            sum(market_cap) market_cap
        from
            `hk-manhattan`.chain_collection_quotation ccq
        where
            create_time = str_to_date( date_format( DATE_sub(CURRENT_TIMESTAMP(), interval {} hour), '%Y-%m-%d %H'),
            '%Y-%m-%d %H%i%m')
            and collection_uuid = {}
    """

    # 计算单个集合的holders
    one_collection_holders = """
        select
        holders
    from
        `hk-manhattan`.chain_collection_quotation ccq
    where
        create_time = str_to_date( date_format( DATE_sub(CURRENT_TIMESTAMP(), interval {} hour), '%Y-%m-%d %H'),
        '%Y-%m-%d %H%i%m')
        and collection_uuid = {}
    """

    # 查询历史的地板价
    history_floor_price = """
        select
            floor_price
        from
            `hk-manhattan`.chain_collection_quotation
        where
            collection_uuid = {}
            and create_time = str_to_date( date_format( DATE_sub(CURRENT_TIMESTAMP(), interval {} hour), '%Y-%m-%d %H'),
            '%Y-%m-%d %H%i%m') 
    """

    # 查询单个集合的sales的数据
    one_collection_sales = """
        SELECT sales FROM `hk-manhattan`.chain_collection_statistics WHERE collection_uuid = {} and date_type = {}
    """

    # 查询sales top 10
    sales_top_10 = """
        SELECT collect_name FROM chain_collection_statistics WHERE date_type={} ORDER BY sales  desc LIMIT 10
    """

