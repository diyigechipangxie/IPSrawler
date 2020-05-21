#!/bin/bash/evn python
# encoding=utf-8
"""
@file:run_spider.py
@time:5/18/20|3:06 PM
"""
import importlib
import time

from gevent import monkey
from gevent.pool import Pool
import schedule

monkey.patch_all()

from core.db.mongo_pool import MongoPool
from core.proxy_validate.httpbin_validator import check_proxy
from settings import SPIDER_PATH, SPIDER_AUTO_INTERVAL
from utils.log import logger


class RunSpider(object):
	def __init__(self):
		self.mongo_pool = MongoPool()
		self.coroutine_pool = Pool()

	def get_spider_from_settings(self):
		for full_name_path in SPIDER_PATH:
			module_name, class_name = full_name_path.rsplit('.', maxsplit=1)
			module = importlib.import_module(module_name)
			cls = getattr(module, class_name)
			spider = cls()
			yield spider

	def run(self):
		spiders = self.get_spider_from_settings()
		for spider in spiders:
			# self._execute_one_task(spider)
			self.coroutine_pool.apply_async(self._execute_one_task, args=(spider,))
		self.coroutine_pool.join()

	def _execute_one_task(self, spider):
		try:
			proxies = spider.get_proxies()
			for proxy in proxies:
				proxy = check_proxy(proxy)
				if proxy.speed != -1:
					self.mongo_pool.insert_one(proxy)
		except Exception as e:
			logger.error(e)

	@classmethod
	def start(cls):
		rs = RunSpider()
		rs.run()
		schedule.every(SPIDER_AUTO_INTERVAL).hours.do(rs.run)
		while True:
			schedule.run_pending()
			time.sleep(1)


if __name__ == '__main__':
	RunSpider.start()
