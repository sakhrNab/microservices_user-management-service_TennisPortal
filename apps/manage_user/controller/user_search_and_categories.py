from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count

from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import permissions, status, filters

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_cookie

from apps.profiles.models import Profile
from apps.profiles.serializers import ProfileSerializer
from .serializers.utils.decorators import time_calculator

from apps.manage_user.controller.serializers.profile_management.serializers import UserSerializer
from apps.manage_user.controller.serializers.user_search_and_categories.serializers import (UserFilterByID,
                                                                                            UserFilter)

User = get_user_model()


# API to List Available Users
class FilterAvailableUsersAPIView(ListAPIView):
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

# API to List users by strength
class FilterUsersStrengthAPIView(ListAPIView):
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

# API to List user by ID
class FilterUsersByIDAPIView(ListAPIView):
    # permission_classes = (permissions.IsAdminUser,)
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

# API to List recommended players
class RecommendedPlayersAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    @time_calculator
    def time(self):
        return 0

    def get_queryset(self):
        if  User.is_authenticated:
            recommended_users = Profile.objects.filter(Q(age=self.request.user.profile.age)
                                                       | Q(region=self.request.user.profile.region) | Q(gender=self.request.user.profile.gender)
                                                       | Q(skill_level=self.request.user.profile.skill_level)).exclude(Q(user__pk=self.request.user.pk)
                                                                                                                       | Q(user__available=False))
            return recommended_users

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        if  request.user.is_authenticated:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True,context={"request": request})
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            # length = len(serializer.data)
            # newlist = [x for ind, x in enumerate(serializer.data) if length > ind >= 0]
            # response = {}
            #
            # for i in range(length):
            #     response[i] = {"first_name": newlist[i]['first_name'],
            #                    "last_name": newlist[i]['last_name'],
            #                    'profile_photo': newlist[i]['profile_photo'],
            #                    'rating': newlist[i]['rating'],
            #                    'about_me': newlist[i]['about_me'],
            #                    }
            self.time()
            res = {
                "users": serializer.data
            }
            return Response(res, status=status.HTTP_200_OK)

# API to List latest players
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
        response = {
            "users": serializer.data
        }
        self.time()
        return Response(response, status = status.HTTP_200_OK)

# API to List popular players
class PopularUsersAPIView(ListAPIView):
    # permission_classes = (IsAdminUser,)
    # permission_classes = (AllowAny,)
    permission_classes = [AllowAny]
    serializer_class = ProfileSerializer
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
        #
        # length = len(serializer.data)
        # newlist = [x for ind, x in enumerate(serializer.data) if length > ind >= 0]
        # response = {}
        #
        # for i in range(length):
        #     response[i] = {"first_name": newlist[i]['first_name'],
        #                    "last_name": newlist[i]['last_name'],
        #                    'profile_photo': newlist[i]['profile_photo'],
        #                    'rating': newlist[i]['rating'],
        #                    'about_me': newlist[i]['about_me'],
        #                    }

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
        resp ={
            "users": serializer.data
        }
        # print("####d############ ", list(response))
        return Response(resp, status=status.HTTP_200_OK)        # return Response(response2, status=status.HTTP_200_OK)




