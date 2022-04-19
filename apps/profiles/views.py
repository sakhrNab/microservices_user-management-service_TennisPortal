from django.contrib import messages
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import NotYourProfile, ProfileNotFound
from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer, UpdateProfileSerializer

User = get_user_model()

class OpponentListAPIView(generics.ListAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.filter(is_opponent=True)
    serializer_class = ProfileSerializer

# 20:00
""" 
    Behind the scenes for the class above
    from rest_framework import api_view, permissions
    @api_view(["GET"])
    @permission_classes((permissions.IsAuthenticated))
    def get_all_agents(request):
        agents = Profile.objects.filter(is_agent=True)
        serializer=ProfileSerializer(agents, many=True)
        name_spaced_response={"agents": serializer.data}
        return Response(name_spaced_response,status=status.HTTP_200_OK)
"""
class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = ProfileSerializer(data=request.data)
        email = request.POST.get('email', False)
        print("############3", User.objects.filter(email=email).exists())

        if serializer.is_valid():
            email = serializer.validated_data.get('email')


            if User.objects.filter(email=email).exists():
                print("#!!!!!!!!!!!!!!!!!!!!", serializer.errors)
                messages.add_message(request, messages.ERROR,
                                     'Email is taken, choose another one')

                return Response({'message': 'Email is duplicate'}, status=status.HTTP_226_IM_USED)

            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
            # if serializer.validate_email(email):
            #     return Response(serializer.errors, status=status.HTTP_226_IM_USED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # ["ProfileJsonRenderer")
    renderer_classes = [ProfileJSONRenderer]

    def get(self, request):
        user = self.request.user
        user_profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(user_profile, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJSONRenderer]

    serializer_class = UpdateProfileSerializer

    # the req. will take a username
    def patch(self, request, username):
        try:
            Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise ProfileNotFound

        print(username, "@@@@@@@@@@@@@@@@@@@@@@@@@")
        user_name = request.user.username
        if user_name != username:
            raise NotYourProfile

        data = request.data
        print(data, "########################")
        serializer = UpdateProfileSerializer(
            instance=request.user.profile, data=data, partial=True
        )
        print("Errrrooooooor")

        serializer.is_valid()
        print("Errrrooooooor2")
        serializer.save()
        print("Errrrooooooor3")
        return Response(serializer.data, status=status.HTTP_200_OK)

