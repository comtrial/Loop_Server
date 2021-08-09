
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('feed_api/', include('feed_api.urls')),
    path('user_api/', include('user_api.urls')),
    path('notice_api/', include('notice_api.urls'))
    # path('user_test/', include('user_test.urls')) 
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
