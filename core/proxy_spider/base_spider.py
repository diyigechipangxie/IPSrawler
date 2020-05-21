#!/bin/bash/evn python
# encoding=utf-8
"""
@file:base_spider.py
@time:5/18/20|3:05 PM
"""
import requests
from lxml import etree

from core.db.mongo_pool import MongoPool
from domain import Proxy
from settings import TIMEOUT
from utils.http import get_user_agent


class BaseSpider(object):
	urls = []
	group_xpath = ''
	detail_xpath = {}

	def __init__(self, urls=[], group_xpath='', detail_xpath={}):
		if urls:
			self.urls = urls
		if group_xpath:
			self.group_xpath = group_xpath
		if detail_xpath:
			self.detail_xpath = detail_xpath

	def get_page_from_url(self, url):
		response = requests.get(url, headers=get_user_agent(), timeout=TIMEOUT)
		page = response.content
		return page

	def get_proxies_from_page(self, page):
		element = etree.HTML(page)
		trs = element.xpath(self.group_xpath)
		for tr in trs:
			ip = self.get_first_ele(tr.xpath(self.detail_xpath['ip']))
			port = self.get_first_ele(tr.xpath(self.detail_xpath['port']))
			area = self.get_first_ele(tr.xpath(self.detail_xpath['area']))
			proxy = Proxy(ip, port, area=area)
			yield proxy

	def get_first_ele(self, lis):
		return lis[0] if len(lis) != 0 else ''

	def get_proxies(self):
		for url in self.urls:
			page = self.get_page_from_url(url)
			proxies = self.get_proxies_from_page(page)
			yield from proxies


if __name__ == '__main__':
	config = {
		'urls': ['https://www.xicidaili.com/nt/{}'.format(i) for i in range(1, 4)],
		'group_xpath': '//*[@id="ip_list"]/tr', # 查看网页源代码里面是否真的有tbody，
		'detail_xpath': {
			'ip': './td[2]/text()',
			'port': './td[3]/text()',
			'area': './td[4]/a/text()',
		}
	}
	c_spider = BaseSpider(**config)
	for line, _ in enumerate(c_spider.get_proxies()):
		mongo = MongoPool()
		mongo.insert_one(_)
		print(line, _)
