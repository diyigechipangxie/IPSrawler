#!/bin/bash/evn python
# encoding=utf-8
"""
@file:proxy_spiders.py
@time:5/18/20|3:06 PM
"""
import random
from core.proxy_spider.base_spider import BaseSpider


class XiciSpider(BaseSpider):
	urls = ["https://www.xicidaili.com/nt/{}".format(i) for i in range(1, 6)]
	group_xpath = '//*[@id="ip_list"]/tr'  # 查看网页源代码里面是否真的有tbody，
	detail_xpath = {
		'ip': './td[2]/text()',
		'port': './td[3]/text()',
		'area': './td[4]/a/text()',
	}



class KDSpider(BaseSpider):
	urls = ["https://www.kuaidaili.com/free/inha/{}/".format(i) for i in range(1, 6)]
	group_xpath = '//*[@id="list"]/table/tbody/tr'  # 查看网页源代码里面是否真的有tbody，
	detail_xpath = {
		'ip': './td[1]/text()',
		'port': './td[2]/text()',
		'area': './td[5]/text()',
	}


class Ip3366Spider(BaseSpider):
	urls = ["http://www.ip3366.net/free/?stype={}&page={}".format(i, j) for i in range(1, 2) for j in range(1, 6)]
	group_xpath = '//*[@id="list"]/table/tbody/tr'  # 查看网页源代码里面是否真的有tbody，
	detail_xpath = {
		'ip': './td[1]/text()',
		'port': './td[2]/text()',
		'area': './td[5]/text()'
	}


# spi = KDSpider()
# for _ in spi.get_proxies():
# 	print(_)

# class Ip66Spider(BaseSpider):
# 	"""with encrypt js cookie cant open """
# 	urls = [''.format(i) for i in range(1, 10)]
# 	group_xpath = ''
# 	detail_xpath = {
# 		'ip': '',
# 		'port': '',
# 		'area': ''
# 	}
#
# 	def get_page_from_url(self, url):
# 		pass