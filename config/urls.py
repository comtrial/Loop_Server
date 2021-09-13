
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny


schema_view = get_schema_view(
    openapi.Info(
        title="Loop API",
        default_version='v1',
        description="Test description of loop apis",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="rlfgks97@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('feed_api/', include('feed_api.urls')),
    path('user_api/', include('user_api.urls')),
    path('notice_api/', include('notice_api.urls')),
    path('group_api/', include('group_api.urls')),
    path('notification_api/', include('notification_api.urls')),
    path('reports_api/', include('reports_api.urls')),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # path('user_test/', include('user_test.urls')) 
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
