from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# from .api import router

### this is correct
urlpatterns = [
    path('superuser/', admin.site.urls),

                  # jwt/create, jwt/refresh, etc..
    # path('api/', include('apps.token_app.urls'),
    path('api/user/', include('apps.manage_user.urls')),

    # path('api/', include(router.urls)),
    # path('api/user/', include('apps.manage_user.urls')),
    ##
    # important to share tokens
    # path ('auth/jwt/token/', CustomTokenObtainPairView.as_view()),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("djoser.urls.jwt")),
    path("api/v1/profile/", include("apps.profiles.urls")),
    path("api/v1/auth/", include("apps.manage_user.urls")),
    path("api/v1/ratings/", include("apps.ratings.urls")),
]

admin.site.site_header = "User Management Admin"
admin.site.site_title = "User Management Admin Portal"
admin.site.index_title = "Welcome to the User Management Portal"
