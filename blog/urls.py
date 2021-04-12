from django.urls import path
from django.contrib.auth.views import LogoutView

from blog.views import PostListView, PostCreateView, PostDetailView, InteractiveLoginView, ProfileDetailView, register

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('post/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('login/', InteractiveLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile-detail'),
    path('register/', register, name='register')
]
