#!/bin/bash/evn python
# encoding=utf-8
"""
@file:proxy_api.py
@time:5/18/20|3:06 PM
"""
import json
import random

from flask import Flask, request

from core.db.mongo_pool import MongoPool


class ProxyAPI(object):

	def __init__(self):
		self.app = Flask(__name__)
		self.mongo_pool = MongoPool()

		@self.app.route('/random')
		def random_proxy():
			protocol = request.args.get('protocol')
			domain = request.args.get('domain')
			proxies = self.mongo_pool.find_all()
			p_index = random.randint(1, 100)
			pr = proxies[p_index]
			pr = pr.__dict__
			return pr

		@self.app.route('/proxies')
		def proxies_list():
			proxies = self.mongo_pool.find_all()
			dict_list = [proxy.__dict__ for proxy in proxies]
			return json.dumps(dict_list)

	def run(self):
		self.app.run('0.0.0.0', port=9999, debug=True)

	@classmethod
	def start(cls):
		pa = cls()
		pa.run()


if __name__ == '__main__':
	ProxyAPI.start()