# -*- coding: utf-8 -*-
# @Time    : 2023/3/9-15:26
# @Author  : 灯下客
# @Email   : 
# @File    : consumer.py
# @Software: PyCharm
from kafka import KafkaConsumer as _KafkaConsumer


class KafkaConsumer(object):

    def __init__(self, **config):
        self.handlers = {}
        self._consumer = _KafkaConsumer(**config)

    def __getattr__(self, item):
        if hasattr(self, item):
            return getattr(self, item)
        return getattr(self._consumer, item)

    def _add_handler(self, topic: str, handler):
        if self.handlers.get(topic) is None:
            self.handlers[topic] = []
        self.handlers[topic].append(handler)

    def handle(self, topic):
        def decorator(f):
            self._add_handler(topic, f)
            return f

        return decorator

    def _run_handlers(self, msg):
        handlers = self.handlers[msg.topic]
        for handler in handlers:
            try:
                if not callable(handler):
                    continue
                handler(msg)
                self._consumer.commit()
            except Exception as e:
                self._consumer.close()

    def subscribe(self):
        self._consumer.subscribe(topics=tuple(self.handlers.keys()))
        for msg in self._consumer:
            self._run_handlers(msg)

