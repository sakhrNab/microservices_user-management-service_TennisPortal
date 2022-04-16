from user_management.settings.base import env

try:
    import pika, json, os, django
    import ast

except Exception as e:
    print("Some modules are missings {}".format(e))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "user_management.settings.development")
django.setup()

from apps.profiles.models import Profile
from apps.profiles.exceptions import NotYourProfile, ProfileNotFound

class MetaClass(type):

    _instance ={}

    def __call__(cls, *args, **kwargs):

        """ Singelton Design Pattern  """

        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]


class RabbitMqServerConfigure(metaclass=MetaClass):

    def __init__(self, host=env("RABBITMQ_HOST"),
                 queue='profiles'): # consume from user_profiles

        """ Server initialization   """

        self.host = host
        self.queue = queue


class rabbitmqServer():

    def __init__(self, server):

        """
        :param server: Object of class RabbitMqServerConfigure
        """
        self.server = server
        self._connection = pika.BlockingConnection(pika.URLParameters(self.server.host))
        self._channel = self._connection.channel()
        self._tem = self._channel.queue_declare(queue=self.server.queue)
        print("Server started waiting for Messages ")

    @staticmethod
    def callback(ch,method, properties, body):
        print(body)
        data = json.loads(body)
        print(data)# data is already the username
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX: ",data['username'], " ", properties.content_type)
        new_rating = float(data['rating'])
        if properties.content_type == 'review_added':
            try:
                print("Rartatgga ", data['rating'])
                print("holaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa2", new_rating)
                profile = Profile.objects.get(user__username=data['username'])
                profile.num_reviews += 1
                # profile.rating += new_rating
                profile.rating = data['rating']
                profile.save()
                print("Reviews increased.")
            except Profile.DoesNotExist:
                raise ProfileNotFound

    def startserver(self):
        self._channel.basic_consume(
            queue=self.server.queue,
            on_message_callback=rabbitmqServer.callback,
            auto_ack=True)
        self._channel.start_consuming()


if __name__ == "__main__":
    serverconfigure = RabbitMqServerConfigure(host=env("RABBITMQ_HOST"),
                                              queue='profiles')

    server = rabbitmqServer(server=serverconfigure)
    server.startserver()

