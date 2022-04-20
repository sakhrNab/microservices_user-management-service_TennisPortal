from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.manage_user.controller.serializers.user_login.serializers import (
    GoogleSocialAuthSerializer, LogoutSerializer, UserLoginSerializer)
from apps.profiles.producer import RabbitMq

User=get_user_model()

# API to login with a private email-address
class LoginAPI(APIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        user_data = self.serializer_class(data=request.data)
        user_data.is_valid(raise_exception=True)

        user_data = User.objects.get(email=request.data['email'])
        user_data.is_signed=True
        user_data.save()

        if user_data:
            status_code = status.HTTP_200_OK
            response = {
                'bool': True, #success
                'status code': status.HTTP_200_OK,
                'isAdmin': user_data.is_staff,
                'message': 'User logged in  successfully',
                'username': user_data.username
            }
            publish_data = {
                "username": str(user_data),
                "logged_status": "True"
            }
            p = RabbitMq()
            RabbitMq.publish(p, 'user_signed', publish_data)
            return JsonResponse(response, status=status_code)
        else:
            # user can is not logged in
            return JsonResponse({'bool': False})

# API to login with gmail account
class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return JsonResponse(data, status=status.HTTP_200_OK)

# API to blacklist a token
class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            user_data = User.objects.filter(is_signed=True).first()

            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            print(user_data)
            user_data.is_signed=False
            publish_data = {
                "username": str(user_data),
                "logged_status": str(user_data.is_signed)
            }
            p = RabbitMq()
            RabbitMq.publish(p, 'user_signed', publish_data)
            print("shared logout message")
            user_data.save()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"response": str(e)},status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

