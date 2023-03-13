# -*- coding: utf-8 -*-
# @Time    : 2023/3/9-15:35
# @Author  : 灯下客
# @Email   : 
# @File    : producer.py
# @Software: PyCharm

from kafka import KafkaProducer as _KafkaProducer


class KafkaProducer(object):

    def __init__(self, **config):
        self._producer:_KafkaProducer = _KafkaProducer(**config)

    def __getattr__(self, item):
        return getattr(self._producer, item)
