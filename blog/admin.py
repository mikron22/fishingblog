from django.contrib import admin

from blog.models import Post, UserProfile, Comment

# Register your models here.
admin.site.register([Post, UserProfile, Comment])