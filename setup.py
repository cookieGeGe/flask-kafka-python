# -*- coding: utf-8 -*-
# @Time    : 2023/3/9-14:40
# @Author  : 灯下客
# @Email   : 
# @File    : setup.py
# @Software: PyCharm


from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='flaskKafka',
    version='0.0.3',
    packages=['flaskKafka'],
    install_requires=['kafka-python'],
    license='MIT',
    description='Make it easier to integrate flask with kafka',
    author='cookieGeGe',
    author_email='nimzy.maina@gmail.com',
    keywords=['kafka', 'consumer', 'kafkaesque', 'flask', 'simple', 'consumer', 'flask style', 'decorator'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cookieGeGe/flask-kafka-python",
    include_package_data=True,
)
