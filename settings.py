#!/bin/bash/evn python
# encoding=utf-8
"""
@file:settings.py
@time:5/18/20|3:07 PM
"""
import logging

#const
MAX_SCORE = 50
TIMEOUT = 3
CHECK_PROXY_ASYNC = 10
SPIDER_AUTO_INTERVAL = 12
CHECK_PROXY_INTERVAL = 2

MONGOURI = "mongodb://127.0.0.1:27017/"

# default  logging settings
LOG_LEVEL = logging.INFO
LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d %(levelname)s: %(message)s]'
LOG_DATEFMT = '%Y-%m-%d %M:%M:%S'
LOG_FILENAME = 'log.log'

# spider path
SPIDER_PATH = [
	'core.proxy_spider.proxy_spiders.XiciSpider',
	'core.proxy_spider.proxy_spiders.KDSpider',
	'core.proxy_spider.proxy_spiders.Ip3366Spider',
]