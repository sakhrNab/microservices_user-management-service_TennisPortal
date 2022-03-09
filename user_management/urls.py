
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# from .api import router

### this is correct
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('token_app.urls'),
    path('api/user/', include('manage_user.urls')),

    # path('api/', include(router.urls)),
    # path('api/user/', include('manage_user.urls')),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
