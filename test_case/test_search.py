# -*- coding: UTF-8 -*-
"""
@File    ：test_search.py
@Author  ：taofangpeng
@Date    ：2022/9/14 16:11 
"""
import pytest

from api.search import search


class TestSearch:

    def test_like_collection_name(self):
        res = search.global_search(params={
            "content": "a",
            "pageNum": "1",
            "pageSize": "10",
            "type": "COLLECTION"
        })
        print(res)


if __name__ == '__main__':
    pytest.main(["-sv"])
