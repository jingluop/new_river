# -*- coding: UTF-8 -*-
"""
@File    ：base_api.py
@Author  ：taofangpeng
@Date    ：2022/9/13 11:27 
"""
import os

import requests
import json as complexjson

from common.data_load import ReadFileData
from common.logger import logger
import urllib3
import hashlib


class BaseApi:

    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.data_file_path = os.path.join(base_path, "config", "config.ini")
        self.host = 'host-' + ReadFileData().load_ini(self.data_file_path)['env']['env']
        self.session = requests.session()

    def get(self, url, **kwargs):
        data = self.request(url, "GET", **kwargs)
        logger.info(f"接口返回数据 ==>> {data}")
        return data

    def post(self, url, data=None, json=None, **kwargs):
        data = self.request(url, "POST", data, json, **kwargs)
        logger.info(f"接口返回数据 ==>> {data}")
        return data

    def put(self, url, data=None, **kwargs):
        data = self.request(url, "PUT", data, **kwargs)
        logger.info(f"接口返回数据 ==>> {data}")
        return data

    def delete(self, url, **kwargs):
        data = self.request(url, "DELETE", **kwargs)
        logger.info(f"接口返回数据 ==>> {data}")
        return data

    def patch(self, url, data=None, **kwargs):
        data = self.request(url, "PATCH", data, **kwargs)
        logger.info(f"接口返回数据 ==>> {data}")
        return data

    def request(self, url, method, data=None, json=None, **kwargs):
        #  取消InsecureRequestWarning警告
        urllib3.disable_warnings()
        url = self.api_root_url + url
        headers = dict(**kwargs).get("headers")
        params = dict(**kwargs).get("params")
        files = dict(**kwargs).get("params")
        cookies = dict(**kwargs).get("params")
        self.request_log(url, method, data, json, params, headers, files, cookies)
        if method == "GET":
            return requests.get(url, **kwargs, verify=False).json()
        if method == "POST":
            return requests.post(url, data, json, **kwargs, verify=False).json()
        if method == "PUT":
            if json:
                # PUT 和 PATCH 中没有提供直接使用json参数的方法，因此需要用data来传入
                data = complexjson.dumps(json)
            return self.session.put(url, data, **kwargs, verify=False).json()
        if method == "DELETE":
            return self.session.delete(url, **kwargs, verify=False).json()
        if method == "PATCH":
            if json:
                data = complexjson.dumps(json)
            return self.session.patch(url, data, **kwargs, verify=False).json()

    @staticmethod
    def request_log(url, method, data=None, json=None, params=None, headers=None, files=None, cookies=None,
                    **kwargs):
        if url:
            logger.info("接口请求地址 ==>> {}".format(url))
        if method:
            logger.info("接口请求方式 ==>> {}".format(method))
        # Python3中，json在做dumps操作时，会将中文转换成unicode编码，因此设置 ensure_ascii=False
        if headers:
            logger.info("接口请求头 ==>> {}".format(complexjson.dumps(headers, indent=4, ensure_ascii=False)))
        if params:
            logger.info("接口请求 params 参数 ==>> {}".format(complexjson.dumps(params, indent=4, ensure_ascii=False)))
        if data:
            logger.info("接口请求体 data 参数 ==>> {}".format(complexjson.dumps(data, indent=4, ensure_ascii=False)))
        if json:
            logger.info("接口请求体 json 参数 ==>> {}".format(complexjson.dumps(json, indent=4, ensure_ascii=False)))
        if files:
            logger.info("接口上传附件 files 参数 ==>> {}".format(files))
        if cookies:
            logger.info("接口 cookies 参数 ==>> {}".format(complexjson.dumps(cookies, indent=4, ensure_ascii=False)))

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

