# flask-kafka-python
flask-kafka-python

I refer to the [`flask_kafka`](https://github.com/NimzyMaina/flask_kafka) library and make some enhancements based on it:

- 
1. Add file locks to prevent flask from repeatedly listening in debug
2. Get config from flask app
3. Increase the registration topic monitoring interface, and support designated consumers at the same time
4. Support for multiple consumers

I hope you find this useful.

## Installation

This project has been commited to Pypi, can be installed by pip:
```shell
$ pip install flask-kafka-python
```

## Simple example

```python
from flask import Flask

from flask_kafka import FlaskKafka

app = Flask(__name__)

app.config["KAFKA_CONFIG"] = {
    "bootstrap_servers": ["172.31.2.20:32423"]
}

bus = FlaskKafka()
bus.init_app(app)


@app.route("/", methods=["get"])
def index():
    return "hello world! ----1"


@bus.topic_handler('kafka_demo')
def test_topic_handler(consumer, msg):
    print("consumed {} from test-topic".format(msg))


# or
# bus.add_topic_handler("kafka_demo", lambda con, msg: print(msg))


if __name__ == '__main__':
    bus.start()
    app.run(debug=True)

```


## License

```
MIT License

Copyright (c) 2023 cookieGeGe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```