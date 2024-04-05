import django.contrib
import django.urls
import django.views.generic

import rest_framework_swagger.views

schema_view = rest_framework_swagger.views.get_swagger_view(title='Forms API')

urlpatterns = [
    django.urls.path('', django.urls.include('api.urls')),
    django.urls.re_path(r'^auth/', django.urls.include('djoser.urls')),
    django.urls.re_path(r'^auth/', django.urls.include('djoser.urls.authtoken')),
    django.urls.re_path(r'^accounts/', django.urls.include('rest_framework.urls')),
    django.urls.path('admin/', django.contrib.admin.site.urls),
    django.urls.path('swagger-ui/', schema_view),
]
