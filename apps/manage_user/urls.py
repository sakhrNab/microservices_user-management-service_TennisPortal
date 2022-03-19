from django.urls import path, re_path
from .views import BlacklistTokenUpdateView, CustomTokenObtainPairView
from rest_framework import routers
from . import views
app_name = 'apps.manage_user'


urlpatterns = [
    # path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist'),
    # path('user-login/', views.user_login),
    # path('all-registered-users/', views.get_users),
    path('jwt/token/', CustomTokenObtainPairView.as_view())
    # path('delete-user/<int:pk>/', views.user_list),
    # path('delete-user/<str:pk>/', views.delete_user_by_id, name='delete_user'),
]