from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from apps.post.serializers import PostSerializer


class CreatePostView(CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
