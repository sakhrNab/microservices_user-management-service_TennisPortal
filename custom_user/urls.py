from django.urls import path
from knox import views as knox_views
from . import views
from .views import WishListView
from django.conf.urls import include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework.routers import DefaultRouter
from .views import BlacklistTokenUpdateView

router = DefaultRouter()
router.register("favorites", WishListView, basename="student")

urlpatterns = [
    path('', include(router.urls)),
    path('api/register/', views.RegisterAPI.as_view(), name='register'),
    path('api/login/', views.LoginAPI.as_view(), name='login'),
    # path('api/user-login/', views.user_login),
    path('api/user/', views.UserAPI.as_view(), name='user'),
    path('api/change-password/<int:pk>/', views.ChangePasswordView.as_view(), name='changepassword'),
    path('api/update-profile/<int:pk>/', views.UpdateProfileView.as_view(), name='updateprofile'),
    path('api/filter-users/', views.FilterUsersAPIView.as_view(), name='filter_user'),
    path('api/user-details/<int:pk>/', views.UserDetailView.as_view(), name='user_details'), 
    path("api/reset/password/", views.PasswordResetView.as_view(), name="rest_password_reset"),
    path('password/reset/confirm/<str:uidb64>/<str:token>/',views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('api/update-user-availability/<str:pk>/', views.UpdateAvailability.as_view(), name="update_profile"),
    path('api/recommended-players/', views.RecommendedPlayersAPIView.as_view(), name="recommended_players"),
    path('api/latest-players/', views.LatestPlayersAPIView.as_view(), name="latest_players"),
    path('api/popular-players/', views.PopularUsersAPIView.as_view(), name="popular_players"),
    path('api/registered-users/', views.AllUsersAPIView.as_view(), name="registered_users"),
    path('api/delete-user/', views.DestroyUserAPIView.as_view(), name="delete_user"),
    path('api/search-by-id/', views.FilterUsersByIDAPIView.as_view(), name="search_by_id"),
    path('google/', views.GoogleSocialAuthView.as_view()),

    path('api/logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

