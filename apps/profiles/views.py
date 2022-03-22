from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import NotYourProfile, ProfileNotFound
from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer, UpdateProfileSerializer


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