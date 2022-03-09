# from django.contrib import admin
# from django.urls import path, include
#
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include('user_management.urls')),
#     path('api/user/', include('users.urls', namespace='users')),
#     path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# ]

## app_name = 'users'

## path('register/' , CustomUserCrete.as_view(), name="create_user"),
## create/, CustomUserCreate.as_view(), name=create_user
## 'logout/blacklist/', BlacklistTokenUpdateView.as_view(), name='blacklist')