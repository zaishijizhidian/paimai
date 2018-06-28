# -*- coding: utf-8 -*-
import os

import logging

import pika

ENV = os.getenv("ENV","LOC")

DATABASES = {"ENV": {
        "MYSQL_HOST": "127.0.0.1",
        "MYSQL_PORT": 3306,
        "MYSQL_USERNAME": "root",
        "MYSQL_PASSWORD": "123456",
        "MYSQL_DATABASE": "spider",
        "MYSQL_URI": "mysql+pymysql://root:123456@127.0.0.1:3306/spider?charset=utf8",

        "REDIS_HOST": "127.0.0.1",
        "REDIS_PORT": 6379,
        "REDIS_DATABASE": 0,

        "REDIS_URI": "redis://localhost:6379/0",
        "REDIS_PASSWORD": None,

        "RABBITMQ_HOST": "10.10.168.94",
        "RABBITMQ_PORT": 5672,
        "RABBITMQ_USERNAME": "mq",
        "RABBITMQ_PASSWORD": "123456",

        "RABBITMQ_URI": "amqp://root:123456@10.10.168.29:5672",

        "MONGO_DATABASE": 'spider',
        "MONGO_URI": "mongodb://127.0.0.1:27017/spider",
                    }}

if ENV != "LOC":
    logging.getLogger("pika").setLevel(logging.INFO)
    # rabbitmq 实例化 获取channel

    ra_host = DATABASES.get(ENV).get("RABBITMQ_HOST")
    ra_port = DATABASES.get(ENV).get("RABBITMQ_PORT")
    ra_user = DATABASES.get(ENV).get("RABBITMQ_USERNAME")
    ra_pass = DATABASES.get(ENV).get("RABBITMQ_PASSWORD")

    rabbit_connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=ra_host, port=ra_port, credentials=pika.PlainCredentials(username=ra_user, password=ra_pass)))
    rabbit_channel = rabbit_connection.channel()

    # 维度信息
    DIMENSIONS = [
       "house_sum_info"
    ]

    # rabbitmq exchange 与队列初始化
    # 确认是否有对应的交换器以及队列
    for dim in DIMENSIONS:
        rabbit_channel.exchange_declare(
            exchange=dim,
            type="topic"
        )
        rabbit_channel.queue_declare(queue=dim)
        rabbit_channel.queue_bind(
                exchange=dim,
                routing_key="#",  # "#" 代表接受topic中的所有信息
                queue=dim
        )