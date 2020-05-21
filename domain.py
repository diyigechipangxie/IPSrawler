#!/bin/bash/evn python
# encoding=utf-8
"""
@file:domain.py
@time:5/18/20|3:07 PM
"""
from settings import MAX_SCORE


class Proxy(object):

	def __init__(self, ip, port, protocol=-1, speed=-1, area=None, nick_type=0, score=MAX_SCORE, disable_domains=[]):
		self.ip = ip
		self.port = port
		self.protocol = protocol
		self.speed = speed
		self.area = area
		self.nick_type = nick_type
		self.score = score
		self.disable_domains = disable_domains

	def __str__(self):
		return str(self.__dict__)