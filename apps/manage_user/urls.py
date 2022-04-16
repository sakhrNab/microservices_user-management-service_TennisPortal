from django.urls import path, include
from knox.views import LogoutView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .views import BlacklistTokenUpdateView, CustomTokenObtainPairView
from rest_framework import routers

from .controller.user_register import RegisterAPI
from .controller.profile_management import (UserAPI, WishListView, UpdateAvailability,
                                            UserDetailView, AllUsersAPIView, DestroyUserAPIView, PasswordResetDoneView,
                                            PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetView,
                                            PasswordChangeView, UpdateProfileView, DeleteAccount, AddWishList)
from .controller.user_search_and_categories import (FilterAvailableUsersAPIView, RecommendedPlayersAPIView,
     LatestPlayersAPIView, PopularUsersAPIView, FilterUsersByIDAPIView, FilterUsersStrengthAPIView)
from .controller.user_login import LoginAPI, GoogleSocialAuthView, LogoutAPIView

app_name = 'apps.manage_user'

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register('profiles', views.ProfileViewset,
#                 basename='profiles')
# router.register("favorites", WishListView, basename="student")

urlpatterns = [

     path('', include(router.urls)),
     path('api/register/', RegisterAPI.as_view(), name='register'),
     path('api/login/', LoginAPI.as_view(), name='login'),
     path('api/logout/', LogoutView.as_view(), name='logout'),

     path('api/my-profile/', UserAPI.as_view(), name='user'),
     # path('api/change-password/<int:pk>/', ChangePasswordView.as_view(), name='changepassword'),
     path('api/update-profile/<int:pk>/', UpdateProfileView.as_view(), name='updateprofile'),
     path('api/filter-available-users/', FilterAvailableUsersAPIView.as_view(), name='filter_user'),
     path('api/user-details/<int:pk>/', UserDetailView.as_view(), name='user_details'),
     # path("api/reset/password/", views.PasswordResetView.as_view(), name="rest_password_reset"),
     # path('password/reset/confirm/<str:uidb64>/<str:token>/',views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
     path('api/update-user-availability/<str:pk>/', UpdateAvailability.as_view(), name="update_profile"),

     path('api/recommended-players/', RecommendedPlayersAPIView.as_view(), name="recommended_players"),
     path('api/latest-players/', LatestPlayersAPIView.as_view(), name="latest_players"),
     path('api/popular-players/', PopularUsersAPIView.as_view(), name="popular_players"),
     path('api/registered-users/', AllUsersAPIView.as_view(), name="registered_users"),

     path('api/delete-user/<str:username>/', DestroyUserAPIView.as_view(), name="delete_user"),
     path('api/delete-user/', DeleteAccount.as_view(), name="delete_account"),
     path('api/filter-by-id/', FilterUsersByIDAPIView.as_view(), name="search_by_id"),
     path('google/', GoogleSocialAuthView.as_view()),
     # path('api/wish-list/', WishListView.as_view({'get': 'list', 'post': 'create' }), name='favorite-players'),
     # path('api/wish-list/<str:pk>/', WishListView.as_view({'post': 'create' }), name='favorite-players'),
     path('api/wishlist/', WishListView.as_view(), name="wishlist"),
     path('api/add-wishlist/', AddWishList.as_view(), name="add_wishlist"),
     # path('api/wish-list/<str:pk>/', WishListView.as_view({'post': 'create'}), name='add-favorite-players'),
     path('api/filter-by-strength/', FilterUsersStrengthAPIView.as_view(), name="search_by_id"),


     path("api/reset_password/", PasswordResetView.as_view(), name="reset_password"),
     path(
          "api/password_reset/done/",
          PasswordResetDoneView.as_view(),
          name="password_reset_done",
     ),
     path(
          "api/reset/<uidb64>/<token>/",
          PasswordResetConfirmView.as_view(),
          name="password_reset_confirm",
     ),
     path(
          "api/reset/done/",
          PasswordResetCompleteView.as_view(),
          name="password_reset_complete",
     ),
     path('api/logout/blacklist/', BlacklistTokenUpdateView.as_view(),
          name='blacklist'),
     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


     # # path('user-login/', views.user_login),
     # path('all-registered-users/', views.get_users),
     # # path('delete-user/<int:pk>/', views.user_list),
     # # path('delete-user/<str:pk>/', views.delete_user_by_id, name='delete_user'),
     # path("api/", views.UserAPIView().as_view(), name="users"),
     # path("users/<int:pk>/", views.UserDetailAPIView.as_view(),
     #      name='user-details'),
]
