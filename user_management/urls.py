from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# from .api import router
from rest_framework_swagger.views import get_swagger_view

import user_management.settings.base

schema_view = get_swagger_view(title='Pastebin API')
### this is correct
urlpatterns = [
    path('superuser/', admin.site.urls),

    path('api/v1/', include('apps.manage_user.urls')),
    path('api/user/swagger/', schema_view),


    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path("api/v1/profile/", include("apps.profiles.urls")),
    path("api/v1/ratings/", include("apps.ratings.urls")),
    path('', include('custom_user.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    #path('social_auth/', include(('custom_user.urls', 'social_auth'),namespace="social_auth")),
] +static(user_management.settings.base.MEDIA_URL,
          document_root=user_management.settings.base.MEDIA_ROOT)

admin.site.site_header = "User Management Admin"
admin.site.site_title = "User Management Admin Portal"
admin.site.index_title = "Welcome to the User Management Portal"
