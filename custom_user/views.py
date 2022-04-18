from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_auth.views import LogoutView
from django.http.response import JsonResponse
from .producer import RabbitMq
from .serializers import (RegisterSerializer, UserSerializer,
                          ChangePasswordSerializer, UpdateUserSerializer)
# UserLoginSerializer,LogoutSerializer,

User = get_user_model()

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters("password1", "password2")
)

class RegisterAPI(CreateAPIView):

    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User registered  successfully!',
            }
        # serializer.
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)


class LoginAPI(APIView):

    permission_classes = (AllowAny,)
    # serializer_class = UserLoginSerializer

    def post(self, request):
        # serializer = self.serializer_class(data=request.data)
        # serializer.is_valid(raise_exception=True)
        print("I AM  HERERERERERE#########################################")
        user_data = User.objects.get(email=request.data['email'])
            # User.objects.filter(email=request.data['email']).first()

        user_data.is_signed=True
        user_data.save()
        print(user_data.is_signed)
        # models.Tennisplayer.objects.get(email=email, password=password)
        print(user_data, "##R##########################")
        if user_data:
            status_code = status.HTTP_200_OK
            response = {
                'bool': True, #success
                'status code': status.HTTP_200_OK,
                'isAdmin': user_data.is_staff,
                'message': 'User logged in  successfully',
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


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ChangePasswordSerializer

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(ChangePasswordView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("Congratulations, password has been Changed.")})


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            # print("faaffafa ", User.data)
            user_data = User.objects.filter(is_signed=True).first()

            print("ra ", user_data)
            # user_data = User.objects.filter(email=request.data['email']).first()
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            user_data.is_signed=False
            publish_data = {
                "username": str(user_data),
                "logged_status": str(user_data.is_signed)
            }
            p = RabbitMq()
            RabbitMq.publish(p, 'user_signed', publish_data)
            print("!!!!!!!!!!!!!!!!!!!! ", "shared logout message")
            user_data.save()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
# class LogoutAPIView(generics.GenericAPIView):
#     serializer_class = LogoutSerializer
#
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def post(self, request):
#
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         print("sfaaaaaaffa ", serializer.data)
#         # p = RabbitMq()
#         # RabbitMq.publish(p, 'user_signed', "False")
#         return Response(status=status.HTTP_204_NO_CONTENT)



class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UpdateUserSerializer
