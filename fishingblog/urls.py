from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from blog import urls
from fishingblog.settings import DEBUG, MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include(urls))
] + static(MEDIA_URL, document_root=MEDIA_ROOT)