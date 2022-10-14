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

    # 查询单个集合历史的地板价
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

    # 查询某个时间段内的地板价列表
    history_floor_price_list = """
            select
                floor_price
            from
                `hk-manhattan`.chain_collection_quotation
            where
                collection_uuid = {}
                and create_time between str_to_date( date_format( DATE_sub(CURRENT_TIMESTAMP(), interval {} hour), '%Y-%m-%d %H'),
                '%Y-%m-%d %H%i%m') and str_to_date( date_format( DATE_sub(CURRENT_TIMESTAMP(), interval {} hour), '%Y-%m-%d %H'),
                '%Y-%m-%d %H%i%m') 
                order by create_time desc
        """

    # 查询单个集合历史的平均价
    avg_price = """
        select
            avg_price
        from
            `hk-manhattan`.chain_collection_quotation
        where
            collection_uuid = {}
            and create_time = str_to_date( date_format( DATE_sub(CURRENT_TIMESTAMP(), interval {} hour), '%Y-%m-%d %H'),
            '%Y-%m-%d %H%i%m')
        """

    # 查询某个时间段内的平均价的列表
    avg_price_list = """
        select
            avg_price
        from
            `hk-manhattan`.chain_collection_quotation
        where
            collection_uuid = {}
            and create_time between str_to_date( date_format( DATE_sub(CURRENT_TIMESTAMP(), interval {} hour), '%Y-%m-%d %H'),
            '%Y-%m-%d %H%i%m') and str_to_date( date_format( DATE_sub(CURRENT_TIMESTAMP(), interval {} hour), '%Y-%m-%d %H'),
            '%Y-%m-%d %H%i%m')
            order by create_time desc
        """

    # 查询单个集合的sales的数据
    one_collection_sales = """
        SELECT sales FROM `hk-manhattan`.chain_collection_statistics WHERE collection_uuid = {} and date_type = {}
    """

    # 查询sales top 10
    sales_top_10 = """
        SELECT collect_name, sales FROM `hk-manhattan`.chain_collection_statistics WHERE date_type={} ORDER BY sales
        desc LIMIT 10
    """

    # 查询热力图上涨数据
    heat_map_rise = """
        SELECT collect_name, volume_change, volume FROM `hk-manhattan`.chain_collection_statistics 
        WHERE date_type={} AND volume_change>0 ORDER BY volume desc limit {}
    """

    # 查询热力图上涨的总条数
    heat_map_rise_count = """
        SELECT count(*) rise_count FROM `hk-manhattan`.chain_collection_statistics 
        WHERE date_type={} AND volume_change>0
    """

    # 查询热力图下跌数据
    heat_map_fall = """
        SELECT collect_name, volume_change, volume FROM `hk-manhattan`.chain_collection_statistics 
        WHERE date_type={} AND volume_change<0 ORDER BY volume desc limit {}
    """

    # 查询热力图下跌总条数
    heat_map_fall_count = """
        SELECT count(*) fall_count FROM `hk-manhattan`.chain_collection_statistics 
        WHERE date_type={} AND volume_change<0
     """

    # 查询美元的汇率
    last_price = """
        select last_price  from `hk-manhattan`.token_last_price where token_type = 'ETH' and unit = 'USD' order by create_time 
        desc limit 1
    """

    # 查询最近交易
    recent_transactions = """
    select collection_name, transaction_price
        from(
        SELECT
            case protocol_type
                when 'ERC1155' then collection_name
                when 'ERC721' then CONCAT( collection_name , ' #' , token_id)
            end collection_name,
            time_stamp, collection_uuid, event, transaction_price, id, rank() over(partition by token_id
        order by
            time_stamp desc,
            id desc)rk
        from
            `hk-chaindata-new`.chain_collection_nft_activity
        where
            collection_uuid = {}
            and event = 'SALE'
        )a
    where a.rk = 1
    order by time_stamp DESC, id desc
    limit {}
    """

    # 查询低于地板价购买
    below_floor_price = """
    select count(*) count from `hk-chaindata-new`.chain_collection_nft_activity where collection_uuid = {} and event = 'SALE' and transaction_price<{}*1000000000000000000
    """

    # 查询高于地板价购买
    above_floor_price = """
    select count(*) count from `hk-chaindata-new`.chain_collection_nft_activity where collection_uuid = {} and event = 'SALE' and transaction_price>={}*1000000000000000000
    """

    # 查询从未交易的集合
    never_traded_distribution = """
    select count(DISTINCT token_id) count from `hk-chaindata-new`.chain_collection_nft_activity where collection_uuid = {} and event = {}
    """
