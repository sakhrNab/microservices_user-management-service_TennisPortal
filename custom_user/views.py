import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from apps.profiles import serializers
from apps.profiles.models import Profile
from apps.profiles.producer import RabbitMq
from apps.profiles.serializers import ProfileSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from custom_user.send_email import send_reset_password_email
from django_filters.rest_framework import DjangoFilterBackend
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, status, filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_auth.views import LogoutView
from rest_auth.serializers import PasswordResetConfirmSerializer
from rest_framework.exceptions import NotAcceptable, PermissionDenied, ValidationError
from rest_framework import viewsets
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    GenericAPIView,
    DestroyAPIView
)

from .serializers import ( RegisterSerializer, UserSerializer,
                         ChangePasswordSerializer, UpdateUserSerializer,
                        PasswordResetConfirmSerializer, ResetPasswordEmailRequestSerializer, 
                        ProfileAvailabilitySerializer, WishListSerializer, UserFilter, GoogleSocialAuthSerializer, UserFilterByID)
from .decorators import time_calculator

User=get_user_model()


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
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)

@csrf_exempt
def user_login(request):
    email = request.POST['email']
    print("I AM  HERERERERERE#########################################")
    user_data = User.objects.filter(email=email).first()
    print(user_data)
    # models.Tennisplayer.objects.get(email=email, password=password)
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

            print("ra ", request.data)
            # user_data = User.objects.filter(email=request.data['email']).first()
            refresh_token = request.data["refresh_token"]
            print("ra2", user_data)
            token = RefreshToken(refresh_token)
            print("ra3", user_data)
            token.blacklist()
            print("ra4", user_data)
            print(user_data)
            user_data.is_signed=False
            print("ra5", user_data)
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


class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UpdateUserSerializer


#API to search users
class FilterUsersAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    ) 
    filterset_class = UserFilter
    queryset = User.objects.filter(available=True)

    @time_calculator
    def time(self):
        return 0

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        self.time()
        return Response(serializer.data)


#API to fetch all users
class AllUsersAPIView(ListAPIView):
    permission_classes = [IsAdminUser]
    # permission_classes = (AllowAny,)

    serializer_class = UserSerializer
    queryset = User.objects.filter(available=True)

    @time_calculator
    def time(self):
        return 0

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        self.time()
        all_emails = User.objects.filter(is_active=True).values_list('email', flat=True)
        date_created_list = User.objects.filter(is_active=True).values_list('created', flat=True)

    # return Response(serializer.data)
        return JsonResponse({'users': list(all_emails),
                             'date_created': list(date_created_list)})

class UserDetailView(APIView):
    permission_classes = permission_classes = (AllowAny,)

    def get(self, request, pk):
        profile = User.objects.get(pk=pk)
        serializer = UserSerializer(
            profile, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


#API to reset password
class PasswordResetView(GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"detail": _("Password reset e-mail has been sent.")},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordResetConfirmView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": _("Password has been reset with the new password.")}
        )


class UpdateAvailability(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileAvailabilitySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        data_to_change = {'available': request.data.get("available")}
        
        serializer = self.serializer_class(request.user, data=data_to_change, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)

        return Response(serializer.data)


class WishListView(viewsets.ModelViewSet):
    serializer_class = WishListSerializer
    queryset = User.objects.filter(available=True)
    permission_classes = (permissions.IsAuthenticated,)

    @time_calculator
    def time(self):
        return 0


    def retrieve(self, request, *args, **kwargs):
        self_user = self.request.user
        favorites = self_user.favorite_players.all()
        page = self.paginate_queryset(favorites)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(favorites, many=True)
        self.time()
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        user_item = self.request.user
        print(data)

        for fav in data["favorite_players"]:
            fav_obj = User.objects.get(module_name=fav["pk"])
            user_item.favorite_players.add(fav_obj)

        return Response(
            {"detail": _("The user has been added to the favorites")},
            status=status.HTTP_200_OK
        )


#API to fetch recommended players
class RecommendedPlayersAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProfileSerializer

    @time_calculator
    def time(self):
        return 0

    def get_queryset(self):
        if not User.is_authenticated:
            recommended_users = Profile.objects.filter(Q(age__iexact=self.request.user.profile.age)
            | Q(region__iexact=self.request.user.profile.region) | Q(gender__iexact=self.request.user.profile.gender) | Q(skill_level__iexact=self.request.user.profile.skill_level)).exclude(Q(user__pk__iexact=self.request.user.pk) | Q(user__available=False))
            return recommended_users

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            self.time()
            return Response(serializer.data)


#API to fetch latest players
class LatestPlayersAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProfileSerializer

    @time_calculator
    def time(self):
        return 0

    def get_queryset(self):
        latest_users = Profile.objects.all().exclude(Q(user__pk__iexact=self.request.user.pk) | Q(user__available=False)).order_by('-user__created')[:30]
        return latest_users

    @method_decorator(cache_page(60 * 60 * 1))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        self.time()
        return Response(serializer.data)

from apps.profiles.renderers import ProfileJSONRenderer
#API to fetch popular players
class PopularUsersAPIView(ListAPIView):
    # permission_classes = (IsAdminUser,)
    # permission_classes = (AllowAny,)
    permission_classes = [AllowAny]
    serializer_class = serializers.ProfileSerializer
    # renderer_classes = ProfileJSONRenderer
    @time_calculator
    def time(self):
        return 0

    def get_queryset(self):
        popular_users = Profile.objects.annotate(num_likes=Count('num_reviews')).exclude(Q(user__pk__iexact=self.request.user.pk) | Q(user__available=False)).order_by('-num_reviews')[:30]
        return popular_users

    @method_decorator(cache_page(60 * 60 * 1))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True,context={"request": request})

        length = len(serializer.data)
        newlist = [x for ind, x in enumerate(serializer.data) if length > ind >= 0]
        response = {}
        response2 = {}

        for i in range(length):
            response[i] = {"first_name": newlist[i]['first_name'],
                           "last_name": newlist[i]['last_name'],
                           'profile_photo': newlist[i]['profile_photo'],
                           'rating': newlist[i]['rating'],
                           }

        #     # response=(',u'.join(str(a)for a in list(response.values())))
        #
        #     response2 =", ".join( repr(e) for e in list(response.values()))

        #--------------------------------------------------------
        # all_first_names = User.objects.filter(is_active=True).values_list('first_name', flat=True).order_by('-first_name')
        # all_last_names = User.objects.filter(is_active=True).values_list('last_name', flat=True).order_by('-first_name')
        # profile_photo = Profile.objects.filter(user__is_active=True).values_list('profile_photo', flat=True).order_by('-user__first_name')
        # rating = Profile.objects.filter(user__is_active=True).values_list('rating', flat=True).order_by('-user__first_name')
        #
        # res = {
        #     'first_name': list(all_first_names),
        #     'last_name': list(all_last_names),
        #     'profile_photo': list(profile_photo),
        #     'rating': list(rating),
        # }
        # self.time()
        #
        # return JsonResponse(res, status=status.HTTP_200_OK)
        #--------------------------------------------------------
        print("####d############ ", list(response))
        return Response(response, status=status.HTTP_200_OK)        # return Response(response2, status=status.HTTP_200_OK)





#API to login with gmail account
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
        return Response(data, status=status.HTTP_200_OK)


class DestroyUserAPIView(DestroyAPIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({"detail": "User deleted"})


#API to search user by ID
class FilterUsersByIDAPIView(ListAPIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = UserSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    filterset_class = UserFilterByID
    def get_queryset(self):
        queryset = User.objects.all().exclude(pk=self.request.user.pk)
        return queryset

    @time_calculator
    def time(self):
        return 0

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        self.time()
        return Response(serializer.data)

