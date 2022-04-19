from django.contrib.auth import get_user_model
from django.http import Http404, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.profiles.models import Profile
from apps.profiles.producer import RabbitMq
from apps.profiles.serializers import ProfileSerializer

from .serializers import UserSerializer

User = get_user_model()

class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# class BlacklistTokenUpdateView(APIView):
#     permission_classes = [AllowAny]
#     authentication_classes = ()
#
#     def post(self, request):
#         try:
#             # print("faaffafa ", User.data)
#             user_data = User.objects.filter(is_signed=True).first()
#
#             print("ra ", request.data)
#             # user_data = User.objects.filter(email=request.data['email']).first()
#             refresh_token = request.data["refresh_token"]
#             print("ra2", user_data)
#             token = RefreshToken(refresh_token)
#             print("ra3", user_data)
#             token.blacklist()
#             print("ra4", user_data)
#             print(user_data)
#             user_data.is_signed=False
#             print("ra5", user_data)
#             publish_data = {
#                 "username": str(user_data),
#                 "logged_status": str(user_data.is_signed)
#             }
#             p = RabbitMq()
#             RabbitMq.publish(p, 'user_signed', publish_data)
#             print("!!!!!!!!!!!!!!!!!!!! ", "shared logout message")
#             user_data.save()
#             return Response(status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response({"response": str(e)},status=status.HTTP_400_BAD_REQUEST)
#

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        ## This data variable will contain refresh and accesss tokens
        data = super().validate(attrs)
        ## You can add more User model's attributes like username, email etc. in the data dictionary like this
        ##  the information, I want to share
        data['username'] = self.user.username
        data['is_signed'] = self.user.is_signed
        # data['isAdmin'] = self.user.is_staff
        # data['bool'] = True
        # data['message'] = "User logged in successfully"

        data_dict = {
            "username": data["username"],
            "logged_status": data["is_signed"]
        }

        # publish
        p = RabbitMq()
        ##
        print("~~~~~~~~~~~~~~~~~~ ", "publishing signed in user")
        RabbitMq.publish(p, 'user_signed', data_dict)
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

from rest_framework import status, viewsets


class ProfileViewset(viewsets.ViewSet):
    def list(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = ProfileSerializer.create(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        profile = Profile.objects.get(pk=pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        profile = Profile.objects.get(pk=pk)
        serializer = ProfileSerializer(instance=profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        profile = Profile.objects.get(pk=pk)
        profile.delete()
        return Response("Profile deleted")

class UserAPIView(APIView):
    def get(self, _):
        users = User.objects.all()
        return Response(UserSerializer(users).data)

class UserDetailAPIView(APIView):
    def get_user(self, pk):
        try:
            User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        user = self.get_user(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_users(request):
    # toDO: fetch users only if you're admin
    # get the user associated with that token, des
    # user = request.email
    # notes = user.note_set.all()
    permission_classes = [AllowAny]
    all_emails = User.objects.filter(is_active=True).values_list('email', flat=True)
    date_created_list = User.objects.filter(is_active=True).values_list('created', flat=True)
    return JsonResponse({'users': list(all_emails),
                         'date_created': list(date_created_list)})