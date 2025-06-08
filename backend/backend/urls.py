from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Movin API",
      default_version='v1',
      description="Movin API 문서",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@minari.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('movies.urls')),  # 실제 API 라우팅
    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # Redoc (선택)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Raw JSON (선택)
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),


    path('api/dj-rest-auth/', include('dj_rest_auth.urls')),
    path('profile/', include('accounts.urls')), #???
    path('api/accounts/', include('accounts.urls')),
    
    path('api/movies/', include('movies.urls')),
    path('recommend/', include('recommend.urls')),
    path('api/dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
