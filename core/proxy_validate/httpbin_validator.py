#!/bin/bash/evn python
# encoding=utf-8
"""
@file:httpbin_validator.py
@time:5/18/20|3:05 PM
"""
import json
import time
import requests

from domain import Proxy
from settings import TIMEOUT
from utils.http import get_user_agent
from utils.log import logger


def check_proxy(proxy):
	"""return validated proxy object"""
	proxies = {
		'http': 'http://{}:{}'.format(proxy.ip, proxy.port),
		'https': 'https://{}:{}'.format(proxy.ip, proxy.port)
	}
	http, http_nick_type, http_speed = check_http_proxy(proxies)
	https, https_nick_type, https_speed = check_http_proxy(proxies, False)
	if http and https:
		proxy.protocol = 2
		proxy.nick_type = http_nick_type
		proxy.speed = http_speed
	elif http:
		proxy.protocol = 0
		proxy.nick_type = http_nick_type
		proxy.speed = http_speed
	elif https:
		proxy.protocol = 1
		proxy.speed = https_nick_type
		proxy.nick_type = https_nick_type
	else:
		proxy.speed = -1
		proxy.nick_type = -1

	return proxy


def check_http_proxy(proxies, is_http=True):
	nick_type = -1
	speed = -1
	if is_http:
		test_url = 'http://httpbin.org/get'
	else:
		test_url = 'https://httpbin.org/get'
	start = time.time()
	try:
		response = requests.get(test_url, headers=get_user_agent(), timeout=TIMEOUT, proxies=proxies)
		if response.ok:
			speed = round(time.time()-start, 2)
			dict_resp = json.loads(response.text)
			origin = dict_resp['origin']
			proxy_connection = dict_resp['headers'].get('Proxy-Connection', None)
			if ',' in origin:
				nick_type = 2
			elif proxy_connection:
				nick_type = 1
			else:
				nick_type = 0
			return True, nick_type, speed
		else:
			return False, nick_type, speed
	except Exception as e:
		# logger.exception(e)
		return False, nick_type, speed


if __name__ == '__main__':
	proxy = Proxy(ip='124.93.201.59', port='42672')
	print(check_proxy(proxy))
