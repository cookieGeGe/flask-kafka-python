# -*- coding: utf-8 -*-
# @Time    : 2023/3/9-14:38
# @Author  : 灯下客
# @Email   : 
# @File    : FlaskKafka.py
# @Software: PyCharm
import threading
from typing import Dict

from flask import Flask
from .consumer import KafkaConsumer
from .producer import KafkaProducer


class FlaskKafka(object):

    def __init__(self, app=None):
        self.app = None
        self._consumers: Dict[str, KafkaConsumer] = {}
        self._producers: Dict[str, KafkaProducer] = {}
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        self.app = app
        if "kafka" in self.app.extensions:
            raise RuntimeError(
                "A 'Kafka' instance has already been registered on this Flask app."
                " Import and use that instance instead."
            )
        self.app.extensions["kafka"] = self
        kafka_config = self.app.config.setdefault("KAFKA_CONFIG", {})
        self.create_consumer("default", **kafka_config)
        self.create_producer("default", **kafka_config)
        kafka_binds = self.app.config.setdefault("KAFKA_BINDS", {})
        for name, config in kafka_binds.items():
            self.create_consumer(name, **config)
            self.create_producer(name, **config)

    def get_consumer(self, consumer_name: str = "default"):
        return self._consumers.get(consumer_name, None)

    def get_producer(self, producer_name: str = "default"):
        return self._producers.get(producer_name, None)

    def add_consumer(self, consumer_name: str, consumer: KafkaConsumer):
        if consumer_name is None or consumer_name == "":
            raise Exception("Consumer name cannot be empty")
        if consumer_name in self._consumers.keys():
            raise Exception("Duplicate consumer name")
        if not isinstance(consumer, KafkaConsumer):
            raise Exception(f"must be {KafkaConsumer.__class__}")
        self._consumers[consumer_name] = consumer

    def create_consumer(self, consumer_name, **config):
        self.add_consumer(consumer_name, KafkaConsumer(**config))

    def create_producer(self, producer_name, **config):
        self.add_producer(producer_name, KafkaProducer(**config))

    def add_producer(self, producer_name: str, producer: KafkaProducer):
        if producer_name is None or producer_name == "":
            raise Exception("Producer name cannot be empty")
        if producer_name in self._producers.keys():
            raise Exception("Duplicate Producer name")
        if not isinstance(producer, KafkaProducer):
            raise Exception(f"must be {KafkaProducer.__class__}")
        self._producers[producer_name] = producer

    def topic_handler(self, topic, consumer: str = "default"):
        consumer_obj = self.get_consumer(consumer)
        if consumer_obj is None:
            raise Exception(f"name {consumer} Consumer not registered")
        return consumer_obj.handle(topic)

    def add_topic_handler(self, topic, callback, consumer: str = "default"):
        self.topic_handler(topic, consumer)(callback)

    def _run(self):
        for name, consumer in self._consumers.items():
            t = threading.Thread(target=consumer.subscribe, name=name)
            t.setDaemon(True)
            t.start()

    def start(self):
        self._run()
