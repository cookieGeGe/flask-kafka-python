# -*- coding: utf-8 -*-
# @Time    : 2023/3/9-17:09
# @Author  : 灯下客
# @Email   : 
# @File    : demo.py
# @Software: PyCharm


from flask import Flask
from threading import Event

from flaskKafka import FlaskKafka

app = Flask(__name__)

app.config["KAFKA_CONFIG"] = {
    "bootstrap_servers": ["172.31.2.20:32423"]
}

INTERRUPT_EVENT = Event()

bus = FlaskKafka()
bus.init_app(app)


@bus.topic_handler('kafka_demo')
def test_topic_handler(msg):
    print("consumed {} from test-topic".format(msg))


if __name__ == '__main__':
    bus.start()
    app.run(debug=True, port=5004)
