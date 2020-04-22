# <*_* python3 coding:utf-8 D:\pycharm *_*>
import HtmlTestRunner
from test_case import Requests
import unittest

# 构建测试套件
suit = unittest.TestSuite()    # 新建suit对象
suit.addTest(Requests.UserInfo('test_case_01'))    # 添加测试集
suit.addTest(Requests.UserInfo('test_case_02'))


if __name__ == '__main__':
    # 执行测试用例
    runner = unittest.TextTestRunner()
    runner.run(suit)

