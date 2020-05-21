#!/bin/bash/evn python
# encoding=utf-8
"""
@file:proxy_check.py
@time:5/18/20|3:06 PM
1.实现单线程代理检测
2.使用协程实现异步检测 提高效率
3.实现定时检测
"""
import time

import schedule
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
from queue import Queue

from core.db.mongo_pool import MongoPool
from core.proxy_validate.httpbin_validator import check_proxy
from settings import MAX_SCORE, CHECK_PROXY_ASYNC, CHECK_PROXY_INTERVAL


class ProxyCheck(object):
	def __init__(self):
		self.mongo_pool = MongoPool()
		self.queue = Queue()
		self.coroutine_pool = Pool()

	def run(self):
		proxies = self.mongo_pool.find_all()
		for proxy in proxies:
			self.queue.put(proxy)
		# 异步回调函数
		for i in range(CHECK_PROXY_ASYNC):
			self.coroutine_pool.apply_async(self._check_one_proxy, callback=self._callback_check)
		# 让当前线程等待队列任务完成
		self.queue.join()

	def _callback_check(self, tmp):
		self.coroutine_pool.apply_async(self._check_one_proxy, callback=self._callback_check)

	def _check_one_proxy(self):
		proxy = self.queue.get()
		proxy = check_proxy(proxy)
		if proxy.speed == -1:
			proxy.score -= 1
			print(proxy.score)
			if proxy.score == 0:
				self.mongo_pool.delete_one(proxy)
			else:
				self.mongo_pool.update_one(proxy)
		else:
			proxy.score = MAX_SCORE
			self.mongo_pool.update_one(proxy)
		self.queue.task_done()

	@classmethod
	def start(cls):
		pc = ProxyCheck()
		pc.run()
		schedule.every(CHECK_PROXY_INTERVAL).do(pc.run)
		while True:
			schedule.run_pending()
			time.sleep(1)


if __name__ == '__main__':
	ProxyCheck.start()
