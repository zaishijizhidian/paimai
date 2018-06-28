# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: Sheng <shengweisong@upg.cn>
# target: 一些公用的函数
"""全局配置文件"""
import logging
import os
import traceback

import pika
from retrying import retry

from model import config



ENV = os.getenv("ENV","LOC")

logger = logging.getLogger("rabbitmq")

@retry(stop_max_attempt_number=10, wait_fixed=100)  # 重试10次 间隔0.1秒
def send_rbmq_message(exchange_name, routing_key, message):
    """
    发送message到主题为topic_name，routing_key是routing_key rabbitmq
    :param exchange_name: 主题
    :param routing_key:
    :param message: 要发送的信息
    :return:
    """
    if config.ENV == "LOC":
        return

    def reconnect():
        """
            MQ 重新连接
        :return:
        """
        config.rabbit_connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=config.ra_host, port=config.ra_port,
                credentials=pika.PlainCredentials(username=config.ra_user, password=config.ra_pass)
            )
        )
        if config.rabbit_connection.is_open:
            logger.info("MQ重新连接成功")

    try:
        # 如果pika连接超时，重新连接
        if config.rabbit_connection.is_closed:
            reconnect()

        try:
            rabbit_channel = config.rabbit_connection.channel()
        except Exception as e:
            logger.error("pika创建channel失败 原因:{0}".format(e))
            logger.error("pika 重新连接")
            reconnect()
            rabbit_channel = config.rabbit_connection.channel()

        # logger.error("rabbit_channel is_open: {0}".format(rabbit_channel.is_open))

        rabbit_channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=message
        )
        rabbit_channel.close()
    except Exception as e:
        logger.error("MQ入库发生失败 原因为：{0}, uuid:{1}".format(traceback.format_exc(), message))
        raise e
