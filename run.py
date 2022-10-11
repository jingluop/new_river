# -*- coding: UTF-8 -*-
"""
@File    ：run.py
@Author  ：taofangpeng
@Date    ：2022/9/13 11:29 
"""
import os
import pytest
from common.logger import logger


def run():
    try:
        logger.info(
            """开始执行用例..."""
        )

        pytest.main(['-W', 'ignore:Module already imported:pytest.PytestWarning',
                     '--alluredir', './report/tmp'])
        """
                   --reruns: 失败重跑次数
                   --count: 重复执行次数
                   -v: 显示错误位置以及错误的详细信息
                   -s: 等价于 pytest --capture=no 可以捕获print函数的输出
                   -q: 简化输出信息
                   -m: 运行指定标签的测试用例
                   -x: 一旦错误，则停止运行
                   --maxfail: 设置最大失败次数，当超出这个阈值时，则不会在执行测试用例
                    "--reruns=3", "--reruns-delay=2"
                   """

        # os.system(r"allure generate ./report/tmp -o ./report/html --clean")
        # os.system(f"allure serve ./report/tmp -p 9999")

    except Exception:
        logger.info(Exception)
        raise


if __name__ == '__main__':
    run()
