from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.manage_user.controller.serializers.user_register.serializers import \
    RegisterSerializer


# API to register to Tennis Companion
class RegisterAPI(CreateAPIView):

    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'success': 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User registered  successfully!',
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)

