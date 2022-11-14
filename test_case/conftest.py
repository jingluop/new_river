# -*- coding: UTF-8 -*-
"""
@File    ：conftest.py
@Author  ：taofangpeng
@Date    ：2022/9/13 16:36 
"""
import hashlib

import requests

add = '0x396387c8921e25212e55364452c840A2eB3a45Aad'
url = "https://newrivertest.agentgo.me/dc/chain-user/user/loginByWalletAddress/app"
url_yan = f'https://newrivertest.agentgo.me/dc/chain-user/user/getSaltWalletAddress/app?walletAddress={add}'


a = hashlib.md5(add.encode(encoding='utf-8')).hexdigest()
yan = requests.get(url_yan).json()['data']
a = a+yan
b=hashlib.md5(a.encode(encoding='utf-8')).hexdigest()
params = {
    "loginSource": "0",
    "password": b,
    "loginType": "1",
    "walletName": "RainBow",
    "walletAddress": add

}
print(requests.post(url, json=params).json())