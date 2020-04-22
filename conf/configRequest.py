# <*_* python3 coding:utf-8 D:\pycharm *_*>

import requests
import json


# get请求
def get(url, querystring):
    headers = request_header()
    response = requests.request("GET", url, headers=headers, params=querystring)
    # print response.url
    return response


# post请求
def post(url, payload, querystring):
    headers = request_header()
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    # print response.url
    return response


# 设置请求的header
def request_header():
    headers = {
        'Content-Type': "application/json",
        'Cache-Control': "no-cache"
    }
    return headers
