from django.urls import path
from apps.retrieve_post.api.post_by_user import PostByUserView

urlpatterns = [
    path('api/post_by_user/<uuid:user_uuid>', PostByUserView.as_view(), name='post_by_user'),
]
