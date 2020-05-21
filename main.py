#!/bin/bash/evn python
# encoding=utf-8
"""
@file:main.py
@time:5/18/20|3:07 PM
"""
from multiprocessing import Process

from core.proxy_api import ProxyAPI
from core.proxy_check import ProxyCheck
from core.proxy_spider.run_spider import RunSpider


def run():
	process_list = []
	process_list.append(Process(target=ProxyCheck.start))
	process_list.append(Process(target=RunSpider.start))
	process_list.append(Process(target=ProxyAPI.start))


	for process in process_list:
		process.daemon = True
		process.start()

	for process in process_list:
		process.join()


if __name__ == '__main__':
	run()