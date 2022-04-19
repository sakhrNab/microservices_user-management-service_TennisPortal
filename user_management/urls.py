from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
# from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from rest_framework import permissions

import user_management.settings.base

schema_view = get_schema_view(
    openapi.Info(
        title="DRF Tutorial  API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('superuser/', admin.site.urls),

    path('users/', include('apps.manage_user.urls')),
    # path('users/api/swagger/', schema_view),
    path('users/api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path("users/api/profile/", include("apps.profiles.urls")),
    # path('users/', include('custom_user.urls')),
    path('rest-auth/', include('rest_auth.urls')),
] + static(user_management.settings.base.MEDIA_URL,
          document_root = user_management.settings.base.MEDIA_ROOT)

admin.site.site_header = "User Management Admin"
admin.site.site_title = "User Management Admin Portal"
admin.site.index_title = "Welcome to the User Management Portal"
