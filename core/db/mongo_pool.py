#!/bin/bash/evn python
# encoding=utf-8
"""
@file:mongo_pool.py
@time:5/18/20|3:04 PM
"""
import pymongo

from domain import Proxy
from settings import MONGOURI
from utils.log import logger


class MongoPool(object):
	def __init__(self):
		self.client = pymongo.MongoClient(MONGOURI)
		self.proxies = self.client['proxies_pool']['proxies']

	def insert_one(self, proxy):
		count = self.proxies.count_documents({'_id': proxy.ip})
		if not count:
			dic = proxy.__dict__
			dic['_id'] = proxy.ip
			self.proxies.insert_one(dic)
			logger.info('insert success')
		else:
			logger.warning('already exist')

	def insert_many(self, proxies: list):
		self.proxies.insert_many(proxies)

	def update_one(self, proxy):
		self.proxies.update_one({"_id": proxy.ip}, {"$set": {"score":proxy.score}})

	def find_all(self):
		query_set = self.proxies.find()
		proxy_list = []
		for item in query_set:
			item.pop('_id')
			proxy = Proxy(**item)
			proxy_list.append(proxy)
		return proxy_list

	def delete_one(self, proxy):
		self.proxies.delete_one({"_id": proxy.ip})
		logger.info('delete %s' % proxy.ip)

	def __del__(self):
		self.client.close()


if __name__ == '__main__':
	mongo = MongoPool()
	proxy = Proxy(ip='124.93.201.59', port='42672')
	mongo.insert_one(proxy)
	mongo.update_one(proxy)
	proxy = Proxy(ip='124.93.201.09', port='42672')
	mongo.insert_one(proxy)

