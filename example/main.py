# -*- coding: utf-8 -*-
# @Time    : 2023/3/10-15:41
# @Author  : 灯下客
# @Email   : 
# @File    : main.py
# @Software: PyCharm

from flask import Flask

from flask_kafka import FlaskKafka

app = Flask(__name__)

app.config["KAFKA_CONFIG"] = {
    "bootstrap_servers": ["172.31.2.20:32423"]
}

kfk = FlaskKafka()
kfk.init_app(app)


@app.route("/", methods=["get"])
def index():
    return "hello world! ----1"


@kfk.topic_handler('kafka_demo')
def test_topic_handler(consumer, msg):
    print("consumed {} from test-topic".format(msg))


# or
# kfk.add_topic_handler("kafka_demo", lambda con, msg: print(msg))


if __name__ == '__main__':
    kfk.start()
    app.run(debug=True)
