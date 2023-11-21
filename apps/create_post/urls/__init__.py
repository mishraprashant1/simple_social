from django.urls import path
from apps.create_post.api import CreatePostView, PostDetailView

urlpatterns = [
    path('api/create/', CreatePostView.as_view(), name='create_post'),
    path('api/<uuid:uuid>/', PostDetailView.as_view(), name='post_detail'),
]
