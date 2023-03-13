# -*- coding: utf-8 -*-
# @Time    : 2023/3/9-15:26
# @Author  : 灯下客
# @Email   : 
# @File    : consumer.py
# @Software: PyCharm
import traceback
from typing import Callable

from kafka import KafkaConsumer as _KafkaConsumer


class KafkaConsumer(object):

    def __init__(self, app, **config):
        self.app = app
        self.handlers = {}
        self._consumer = _KafkaConsumer(**config)

    def __getattr__(self, item: str):
        return getattr(self._consumer, item)

    def _add_handler(self, topic: str, handler: Callable):
        if self.handlers.get(topic) is None:
            self.handlers[topic] = []
        self.handlers[topic].append(handler)

    def handle(self, topic: str):
        def decorator(f):
            self._add_handler(topic, f)
            return f

        return decorator

    def _run_handlers(self, msg):
        handlers = self.handlers.get(msg.topic, [])
        for handler in handlers:
            try:
                if not callable(handler):
                    continue
                handler(self, msg)
            except Exception as e:
                self.app.logger.error(traceback.format_exc())

    def subscribe(self):
        try:
            self._consumer.subscribe(topics=list(self.handlers.keys()))
            for msg in self._consumer:
                self._run_handlers(msg)
        finally:
            self._consumer.close()
