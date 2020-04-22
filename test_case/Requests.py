# coding=utf-8
"""
created on 2020-01-15
@author: 7_hearts
project: 模拟接口发送请求
"""
import hashlib
from test_case.excel import excel_open, excel_wr
import requests
import json
import unittest
from conf.config import *


class UserInfo(unittest.TestCase):

    def setUp(self):
        print('='*10+'执行测试脚本!'+'='*10)
        # 用户登录
        pdata = {
            'username': '99980000026',
            'password': hashlib.md5(bytes('666666', encoding='utf-8')).hexdigest()
        }
        r = requests.post(STUDENT_APP_URL + "auth/login/", json=pdata)
        res1 = json.loads(r.text)
        token = res1["data"]["token"]
        self.headers = {
            'Authorization': 'Token ' + token,
            'Content-Type': 'application/json'
        }
        # 读取测试数据--case.excel
        self.sh = excel_open()
        """
        dick = sh.cell_value(14, 3)
        user_n = eval(dick).get('username')    # 将字符串解析成字典格式
        print(user_n)
        """

    def tearDown(self) -> None:
        print('='*10+'脚本执行完成!'+'='*10)

    def test_case_01(self):
        """
        输入：url、请求方法、请求data
        输出：响应body、错误信息
        :return:
        """
        for i in range(1, 11):
            # 输入
            user_homework_id = self.sh.cell_value(1, 7)    # 获取作业id
            # print(user_homework_id)
            question_history_list = self.sh.cell_value(1, 8)
            question_history_list = question_history_list.replace("'", "\"")    # 转换字符串中的单引号
            # print(question_history_list)
            # 将列表形式的字符串转换成json文本，以便使用get方法
            question_history_id = json.loads(question_history_list)[0].get("question_history_id", None)
            # print(question_history_id)
            if i in [2, 3, 5, 6, 7]:     # url中需要传入user_homework_id
                url = self.sh.cell_value(i, 1)
                url = url.format(user_homework_id)   # 拼接url
                print(url)
            elif i == 4:             # url中需要传入user_homework_id和question_history_id
                url = self.sh.cell_value(i, 1)
                url = url.format(a=user_homework_id, b=question_history_id)     # 拼接url
                print(url)
            elif i == 8:
                url = self.sh.cell_value(i, 1)
                url = url.format(question_history_id)  # 拼接url
                print(url)
            else:
                url = self.sh.cell_value(i, 1)
                print(url)
            method = self.sh.cell_value(i, 2)    # 获取请求方法
            data = {
                "do_homework_duration": 10,
                "question": [{
                    "do_not_submit": False,
                    "do_question_duration": 10,
                    "answer": [""],
                    "user_subject_answer_images": [],
                    "question_history_id": question_history_id,
                    "index": 0
                }],
                "squad_code": "test_DEV",
                "teacher_name": "yangjinda",
                "student_name": "11"
            }    # 获取请求体
            # 判断请求方式
            if method == 'get':
                res = requests.get(url, headers=self.headers)
                resp = json.loads(res.text)
                res_data = resp.get("data", 'null')
                user_homework_list = res_data.get("user_homework_list", 'null')
                # 判断接口请求是否成功
                if resp["code"] == 200:
                    excel_wr(i, 4, str(resp["code"]))
                    excel_wr(i, 6, str(res.text))    # 打印返回值
                    excel_wr(i, 5, str(resp["msg"]))
                    if user_homework_list != "null":
                        excel_wr(i, 7, str(user_homework_list[0].get("id", None)))    # 打印列表第一道作业的user_homework_id
                        # question_history_list = user_homework_list[0].get("question_history_list", None)
                        excel_wr(i, 8, str(user_homework_list[0].get("question_history_list", None)))   # 打印作业中的所有题目列表
                else:
                    excel_wr(i, 4, str(resp["code"]))    # 打印错误信息
                    excel_wr(i, 5, str(resp["msg"]))

            elif method == 'post':
                res = requests.post(url, json=data, headers=self.headers)
                resp = json.loads(res.text)
                # 判断接口请求是否成功
                if resp['code'] == 200:
                    excel_wr(i, 4, str(resp["code"]))    # 打印返回值
                    excel_wr(i, 6, str(res.text))
                    excel_wr(i, 5, str(resp["msg"]))

                else:
                    excel_wr(i, 4, str(resp["code"]))    # 打印错误信息
                    excel_wr(i, 5, str(resp["msg"]))

    def test_case_02(self):
        """
        校验题目数据是否缺失
        :return:
        """
        res = self.sh.cell_value(4, 6)
        res = json.loads(res)
        data = res.get("data", None)    # 获取question_history做题历史
        question = data.get("question", None)
        print(question)
        question_type = question.get("question_type", None)
        print(question_type)
        if question_type == 0:
            print('单选题', end="\n")
            self.assertNotEqual(data["question"]["right_answers"], [], msg="right_answers为空")

        elif question_type == 1:
            print('填空题', end="")
            self.assertNotEqual(data['question']['blank_answers'], [], msg="blank_answers为空")

        elif question_type == 2:
            print('主观题', end='')
            self.assertNotEqual(data['question']['subject_answers'], [], msg="subject_answers为空")

        elif question_type == 3:
            print('多选题', end='')
            self.assertNotEqual(data['question']['right_answers'], [], msg='right_answers为空')

        elif question_type == 4:
            print('排序题', end='')
            self.assertNotEqual(data['question']['sorted_answers'], [], msg='sorted_answers排序数组为空')
            self.assertNotEqual(data['question']['unsorted_options'], [], msg='排序选项为空')


if __name__ == '__main__':
    unittest.main()



