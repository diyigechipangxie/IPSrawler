#!/bin/bash/evn python
# encoding=utf-8
"""
@file:json_dict.py
@time:5/18/20|5:17 PM
"""
import json

json_date = '''{
    "args": {},
    "headers": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8,la;q=0.7,zh-TW;q=0.6",
        "Host": "httpbin.org",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
        "X-Amzn-Trace-Id": "Root=1-5ec2525b-5fb0942061897400d1ac1f00"
    },
    "origin": "117.152.77.250",
    "url": "http://httpbin.org/get"
}'''
dict_date = json.loads(json_date)
q = dict_date['headers'].get('Host')



