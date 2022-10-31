# -*- coding: UTF-8 -*-
"""
@File    ：sql.py
@Author  ：taofangpeng
@Date    ：2022/10/10 10:01 
"""
from common.db import db_proxy, db_mysql


class BaseSql:
    # 集合详情查询地板价
    floor_price = """SELECT floor_price FROM `hk-manhattan`.chain_collection WHERE collection_uuid = {}"""

    # 查询现有的所有集合的uuid
    collection_uuid = """SELECT distinct collection_uuid collection_uuid FROM `hk-manhattan`.chain_collection_aggregation_data"""

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
        SELECT sales FROM `hk-manhattan`.chain_collection_aggregation_data WHERE collection_uuid = {} and date_type = {}
    """

    # 查询sales top 10
    sales_top_10 = """
        SELECT collect_name, sales FROM `hk-manhattan`.chain_collection_aggregation_data WHERE date_type={} ORDER BY sales
        desc LIMIT 10
    """

    # 查询热力图上涨数据
    heat_map_rise = """
        SELECT collect_name, volume_change, volume FROM `hk-manhattan`.chain_collection_aggregation_data 
        WHERE date_type={} AND volume_change>0 ORDER BY cast(volume as float4) desc limit {}
    """

    # 查询热力图上涨的总条数
    heat_map_rise_count = """
        SELECT count(*) rise_count FROM `hk-manhattan`.chain_collection_aggregation_data 
        WHERE date_type={} AND volume_change>0
    """

    # 查询热力图下跌数据
    heat_map_fall = """
        SELECT collect_name, volume_change, volume FROM `hk-manhattan`.chain_collection_aggregation_data 
        WHERE date_type={} AND volume_change<0 ORDER BY cast(volume as float4) desc limit {}
    """

    # 查询热力图下跌总条数
    heat_map_fall_count = """
        SELECT count(*) fall_count FROM `hk-manhattan`.chain_collection_aggregation_data 
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
            `hk-chaindata`.chain_collection_nft_activity
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
    select count(*) count from `hk-chaindata`.chain_collection_nft_activity where collection_uuid = {} and event = 'SALE' and transaction_price<{}*1000000000000000000
    """

    # 查询高于地板价购买
    above_floor_price = """
    select count(*) count from `hk-chaindata`.chain_collection_nft_activity where collection_uuid = {} and event = 'SALE' and transaction_price>={}*1000000000000000000
    """

    # 查询从未交易的集合
    never_traded_distribution = """
    select count(DISTINCT token_id) count from `hk-chaindata`.chain_collection_nft_activity where collection_uuid = {} and event = '{}'
    """

    # 查询版本号
    version = """
    select CONFIG_VALUE FROM `hk-manhattan`.chain_config_sys where CONFIG_ID = '{}'
    """

    # 查询筛选条件categories
    categories = """
    select CONFIG_VALUE from chain_config_sys ccs where CONFIG_ID = 'categories'
    """

    # 查询筛选条件chains
    chains = """
    select CONFIG_VALUE from chain_config_sys ccs where CONFIG_ID = 'chains'
    """

    # 查询筛选条件ranks
    ranks = """
    select CONFIG_VALUE from chain_config_sys ccs where CONFIG_ID = 'ranks'
    """

    # 查询某个集合下所有的钱包地址
    wallet_address = """
    select DISTINCT wallet_address wallet_address FROM `hk-chaindata`.chain_nft_holder_wallet WHERE collection_uuid={}
    """

    # 筛选蓝筹钱包地址
    blue_chip_wallet_address = """
    select DISTINCT wallet_address wallet_address FROM `hk-manhattan`.chain_blue_chip_holder_wallet WHERE wallet_address IN {}
    """

    # 查询单个集合的挂单数量
    count_listing_price = """
    select COUNT(DISTINCT token_uuid) count FROM `hk-chaindata`.chain_collection_nft_listing_price WHERE collection_uuid={}
    """

    # 查询单个集合发行的nft的总数量
    total_nft = """
    SELECT total_nft from `hk-manhattan`.chain_collection WHERE collection_uuid={}
    """

    # 计算总市值
    total_market = """
    select
        sum(market_cap) market_cap
    from
        `hk-manhattan`.chain_collection_quotation ccq
    where
        create_time = str_to_date( date_format( DATE_sub(CURRENT_TIMESTAMP(), interval {} hour), '%Y-%m-%d %H'),
        '%Y-%m-%d %H%i%m')
    """

    # 计算总的交易量
    total_volume = """
    select
        sum(volume) volume
    from
        `hk-manhattan`.chain_collection_quotation ccq
    where
        create_time = str_to_date( date_format( DATE_sub(CURRENT_TIMESTAMP(), interval {} hour), '%Y-%m-%d %H'),
        '%Y-%m-%d %H%i%m')
    """


class BuriedPointSql:
    # 查询新用户，需要传入起始时间，结束时间，附加筛选条件
    new_users = """
    select
        {} substring(create_time , 1, 10)dateTime, count(distinct device_id ) count
    from
        `hk-manhattan`.system_operate_record
    where
        replace(substring(create_time , 1, 10), '-', '') <= {}
        and replace(substring(create_time , 1, 10), '-', '') >= {}
        and first_visit_time is not null 
        group by {} substring(create_time , 1, 10) 
        order by {} substring(create_time , 1, 10);
    """

    # 计算留存率
    retention_rate = """
    select  create_time,count(a.device_id)count, before_count  from 
    (select  distinct  device_id, replace(substring(create_time , 1, 10), '-', '')create_time from system_operate_record )a
    left join
    (select device_id ,replace(substring(first_visit_time , 1, 10), '-', '')first_visit_time, count( device_id) over(partition by replace(substring(first_visit_time , 1, 10), '-', '') ) as before_count  
    from system_operate_record sor where first_visit_time is not null)b
    on a.device_id = b.device_id
    where create_time - first_visit_time = 1
    group by create_time
    order by create_time desc
    """

    # 计算新注册用户数
    new_register_user = """
    select
        {} ,substring(create_time , 1, 10)dateTime,count(distinct id)count
    from
        (select id, create_time from `hk-manhattan`.chain_user_info) a
    left join    
        (select user_id , channel, platform from `hk-manhattan`.system_operate_record)b
    on a.id = b.user_id
    where 
        replace(substring(create_time , 1, 10), '-', '') <= {}
        and replace(substring(create_time , 1, 10), '-', '') >= {}
    group by {} substring(create_time , 1, 10)
    order by {} substring(create_time , 1, 10);
    """

    # 计算绑定钱包数
    bind_wallet = """
    select count(1)count, substring(create_time  , 1, 10) create_time from `hk-manhattan`.chain_user_info where wallet_address is not null group by substring(create_time  , 1, 10) 
    """

    # 计算活跃用户
    active_user = """
    select  count( distinct device_id)count, substring(create_time , 1, 10)create_time from system_operate_record group by substring(create_time , 1, 10);
    """

    # 计算活跃钱包用户
    active_wallet_user = """
    select count( distinct user_id)count,create_time from 
    (select id  from chain_user_info where wallet_address is not null )a
    left join 
    (select device_id, substring(create_time , 1, 10)create_time,user_id from system_operate_record)b
    on a.id = b.user_id
    group by create_time
    """

    # uv
    uv = """
    select
        substring(create_time , 1, 10)dateTime,
        count(distinct device_id)count
    from
        `hk-manhattan`.system_operate_record
    where
        replace(substring(create_time , 1, 10), '-', '') <= {}
        and replace(substring(create_time , 1, 10), '-', '') >= {}
    group by
        substring(create_time , 1, 10)
    """

    # pv
    pv = """
       select
            substring(create_time , 1, 10)dateTime,
            count(device_id)count
        from
            `hk-manhattan`.system_operate_record
        where
            replace(substring(create_time , 1, 10), '-', '') <= {}
            and replace(substring(create_time , 1, 10), '-', '') >= {}
        group by
            substring(create_time , 1, 10)
    """

    # 计算尝试登录用户
    attempt_login_user = """
    select
        {} substring(create_time , 1, 10)dateTime, count(device_id ) count
    from
        `hk-manhattan`.system_operate_record
    where
        replace(substring(create_time , 1, 10), '-', '') <= {}
        and replace(substring(create_time , 1, 10), '-', '') >= {} and first_try_login is not null
        group by {} substring(create_time , 1, 10) 
        order by {} substring(create_time , 1, 10);
    """

    # 计算新增钱包中有NFT的用户数
    wallet_with_nft = """
    
    """
