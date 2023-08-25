from django.urls import path
from apps.create_post.api import CreatePostView

urlpatterns = [
    path('api/create/', CreatePostView.as_view(), name='create_post'),
]
