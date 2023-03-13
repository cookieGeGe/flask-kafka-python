# -*- coding: utf-8 -*-
# @Time    : 2023/3/9-14:38
# @Author  : 灯下客
# @Email   : 
# @File    : flask_kafka.py
# @Software: PyCharm
import atexit
import os
import platform
import threading
from typing import Dict, Callable

from .consumer import KafkaConsumer
from .producer import KafkaProducer


class FlaskKafka(object):

    def __init__(self, app=None):
        self.app = None
        self._consumers: Dict[str, KafkaConsumer] = {}
        self._producers: Dict[str, KafkaProducer] = {}
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
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

    def get_consumer(self, consumer_name: str = "default") -> KafkaConsumer:
        return self._consumers.get(consumer_name, None)

    def get_producer(self, producer_name: str = "default") -> KafkaProducer:
        return self._producers.get(producer_name, None)

    def add_consumer(self, consumer_name: str, consumer: KafkaConsumer):
        if consumer_name is None or consumer_name == "":
            raise Exception("Consumer name cannot be empty")
        if consumer_name in self._consumers.keys():
            raise Exception("Duplicate consumer name")
        if not isinstance(consumer, KafkaConsumer):
            raise Exception(f"must be {KafkaConsumer.__class__}")
        self._consumers[consumer_name] = consumer

    def create_consumer(self, consumer_name: str, **config):
        self.add_consumer(consumer_name, KafkaConsumer(self.app, **config))

    def create_producer(self, producer_name: str, **config):
        self.add_producer(producer_name, KafkaProducer(**config))

    def add_producer(self, producer_name: str, producer: KafkaProducer):
        if producer_name is None or producer_name == "":
            raise Exception("Producer name cannot be empty")
        if producer_name in self._producers.keys():
            raise Exception("Duplicate Producer name")
        if not isinstance(producer, KafkaProducer):
            raise Exception(f"must be {KafkaProducer.__class__}")
        self._producers[producer_name] = producer

    def topic_handler(self, topic: str, consumer: str = "default"):
        consumer_obj = self.get_consumer(consumer)
        if consumer_obj is None:
            raise Exception(f"name {consumer} Consumer not registered")
        return consumer_obj.handle(topic)

    def add_topic_handler(self, topic: str, callback: Callable, consumer: str = "default"):
        self.topic_handler(topic, consumer)(callback)

    def _run(self):
        for name, consumer in self._consumers.items():
            t = threading.Thread(target=consumer.subscribe, name=name)
            t.setDaemon(True)
            t.start()

    def _start(self):
        self._run()

    def start(self, lock: bool = True):
        if not lock:
            self._start()
            return
        self._start_with_lock()

    def _start_with_lock(self):
        """
        Start the kafka consumer with a lock
        :return:
        """
        lock_file_path = os.path.join(os.getcwd(), "flask_kafka.lock")
        if platform.system() != 'Windows':
            fcntl = __import__("fcntl")
            f = open(lock_file_path, 'wb')
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                self._start()
            except:
                pass

            def unlock():
                fcntl.flock(f, fcntl.LOCK_UN)
                f.close()

            atexit.register(unlock)
        else:
            msvcrt = __import__('msvcrt')
            f = open(lock_file_path, 'wb')
            try:
                msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                self._start()
            except:
                pass

            def _unlock_file():
                try:
                    f.seek(0)
                    msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
                except:
                    pass

            atexit.register(_unlock_file)
