# amqps://dowzsxzj:UT7_s888elZ3FCRdD1CjiHY9S9aQPI81@cow.rmq2.cloudamqp.com/dowzsxzj
import json

import pika

params = \
    pika.URLParameters('amqps://dowzsxzj:UT7_s888elZ3FCRdD1CjiHY9S9aQPI81@cow.rmq2.cloudamqp.com/dowzsxzj')

connection = pika.BlockingConnection(params)

channel = connection.channel()
channel.queue_declare(queue='review_service')

def publish(method, body):
    properties = pika.BasicProperties(method)
    # routing key, for the consumer to know whom it's coming from
    channel.basic_publish(exchange='', routing_key='review_service',
                          body=json.dumps(body), properties=properties)
