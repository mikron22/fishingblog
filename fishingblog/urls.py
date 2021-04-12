from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import url

from blog import urls
from fishingblog.settings import DEBUG, MEDIA_ROOT, MEDIA_URL, STATIC_URL, STATIC_ROOT

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include(urls)),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)