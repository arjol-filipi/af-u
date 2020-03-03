from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('core.urls')),
    path('', include('shortu.urls')),
    path('', include('news.urls')),
    path('', include('cw.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-token-auth/', obtain_jwt_token),
    path('rest-auth/registration/', include('rest_auth.registration.urls'))
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
