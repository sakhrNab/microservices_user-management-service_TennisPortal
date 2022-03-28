from django.urls import path
from knox import views as knox_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views
from .views import BlacklistTokenUpdateView

urlpatterns = [
    path('api/register/', views.RegisterAPI.as_view(), name='register'),
    path('api/login/', views.LoginAPI.as_view(), name='login'),
    # path('api/logout/', views.LogoutView.as_view(), name='logout'),
    path('api/user/', views.UserAPI.as_view(), name='user'),
    path('api/change-password/<int:pk>/', views.ChangePasswordView.as_view(), name='changepassword'),
    path('api/update-profile/<int:pk>/', views.UpdateProfileView.as_view(), name='updateprofile'),
    path('api/logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]