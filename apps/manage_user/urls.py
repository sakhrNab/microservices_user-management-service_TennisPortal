from django.urls import path, re_path
from .views import CustomUserCreate, BlacklistTokenUpdateView
from rest_framework import routers
from . import views

app_name = 'apps.manage_user'


urlpatterns = [
    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist'),
    path('user-login/', views.user_login),
    path('all-registered-users/', views.get_users),
    # url gonna match here with global url
    re_path(r'^user_detailss/', views.UserProfileListCreateAPIView.as_view()),
    re_path(r'^user_details/$', views.UserProfileListCreateAPIView.as_view()),
    re_path(r'^user_details/(?P<pk>\d+)/$', views.UserProfileRetrieveUpdateDestroyAPIView.as_view()),

    # path('delete-user/<int:pk>/', views.user_list),
    # path('delete-user/<str:pk>/', views.delete_user_by_id, name='delete_user'),
]