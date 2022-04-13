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

    def __init__(self, host='amqps://dowzsxzj:UT7_s888elZ3FCRdD1CjiHY9S9aQPI81@cow.rmq2.cloudamqp.com/dowzsxzj',
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
        new_rating = int(data['rating'])
        if properties.content_type == 'review_added':
            try:
                print("Rartatgga ", data['rating'])

                print("holaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa2", new_rating)
                profile = Profile.objects.get(user__username=data['username'])
                profile.num_reviews += 1
                profile.rating += new_rating
                profile.save()
                print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
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
    serverconfigure = RabbitMqServerConfigure(host='amqps://dowzsxzj:UT7_s888elZ3FCRdD1CjiHY9S9aQPI81@cow.rmq2.cloudamqp.com/dowzsxzj',
                                              queue='profiles')

    server = rabbitmqServer(server=serverconfigure)
    server.startserver()



# # amqps://dowzsxzj:UT7_s888elZ3FCRdD1CjiHY9S9aQPI81@cow.rmq2.cloudamqp.com/dowzsxzj
# import functools
# import json, django, os, pika, threading
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "review_service.settings.development")
# django.setup()
#
# from apps.reviews.models import UserProfile
#
# params = pika.URLParameters('amqps://dowzsxzj:UT7_s888elZ3FCRdD1CjiHY9S9aQPI81@cow.rmq2.cloudamqp.com/dowzsxzj')
#
# connection = pika.BlockingConnection(params)
#
# channel = connection.channel()
#
#
# # queue --> review_service
# channel.queue_declare(queue='review_service')
#
# def callback(ch, method, properties, body):
#     print('Received in review_service')
#     print("####################@##########################################")
#     # print(body) --> this will print b'"\\"UUID"
#     data = json.loads(body)
#     print(data)
#
#     print("!!!!!!!!!!", data['id'])
#     # id = uuid.UUID(data['id']).hex
#     if properties.content_type == 'profile_created':
#         print("Information about the id and username: Id:", data['id'], " username: ", data['username'])
#         # user_profile = data['id']
#
#         user_profile = UserProfile.objects.create(id=data['id'],
#                                                   username=data['username'])
#         user_profile.save()
#
#         print("Users Profile created")
#
#
# channel.basic_consume(queue='review_service', on_message_callback=callback, auto_ack=True)
# channel.start_consuming()
#
# print('Started Consuming')
#
# channel.close()
#
