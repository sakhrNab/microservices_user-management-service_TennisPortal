from user_management.settings.base import env

try:
    import pika

except Exception as e:
    print("Some Modules are missings {}".format_map(e))

import json
class MetaClass(type):

    _instance ={}

    def __call__(cls, *args, **kwargs):

        """ Singelton Design Pattern  """

        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]


class RabbitmqConfigure(metaclass=MetaClass):

    def __init__(self, queue='review_service', host=env("RABBITMQ_HOST"),
                 routingKey='review_service', exchange=''):
        """ Configure Rabbit Mq Server  """
        self.queue = queue
        self.host = host
        self.routingKey = routingKey
        self.exchange = exchange


class RabbitMq():

    def __init__(self):

        self._connection = pika.BlockingConnection(pika.URLParameters(env("RABBITMQ_HOST")))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue="review_service")

    def publish(self, method, body):
        properties = pika.BasicProperties(method)
        self._channel.basic_publish(exchange="",
                                    routing_key="review_service",
                                    body=json.dumps(body), properties=properties)

        print("Published Message: {}".format(body), "--> ", properties.content_type)
        self._connection.close()


if __name__ == "__main__":
    server = RabbitmqConfigure(queue='review_service',
                               host=env("RABBITMQ_HOST"),
                               routingKey='review_service',
                               exchange='')

    rabbitmq = RabbitMq()


