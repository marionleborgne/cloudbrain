#!/usr/bin/env python
import pika


_DEVICE_ID = "mock_device"
_DEVICE_NAME = "openbci"
_HOST = "localhost"
_BUFFER_SIZE = 100


connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange=_DEVICE_NAME,
                         type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue


channel.queue_bind(exchange=_DEVICE_NAME,
                   queue=queue_name,
                   routing_key=_DEVICE_ID)


def callback(ch, method, properties, body):
    print " -> %r:%r" % (method.routing_key, body,)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
