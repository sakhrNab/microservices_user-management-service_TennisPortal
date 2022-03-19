from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.profiles.producer import RabbitMq
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


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        ## This data variable will contain refresh and accesss tokens
        data = super().validate(attrs)
        ## You can add more User model's attributes like username, email etc. in the data dictionary like this
        ##  the information, I want to share
        data['username'] = self.user.username
        data['is_signed'] = self.user.is_signed
        data_dict = {
            "username": data["username"],
            "is_signed": data["is_signed"]
        }
        # publish
        p = RabbitMq()
        ##
        print("~~~~~~~~~~~~~~~~~~ ", "publishing signed in user")
        RabbitMq.publish(p, 'user_signed', data_dict)
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer