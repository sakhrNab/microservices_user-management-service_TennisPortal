from django.urls import path

from .views import (OpponentListAPIView, GetProfileAPIView, UpdateProfileAPIView
                    )

urlpatterns = [
     path("me/", GetProfileAPIView.as_view(), name="get_profile"),
     path("update/<str:username>/", UpdateProfileAPIView.as_view(),
          name="update_profile"),
     path("opponents/all/", OpponentListAPIView.as_view(),
          name="all-opponents"),
    # path("")
]