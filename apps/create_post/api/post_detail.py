from rest_framework.generics import RetrieveUpdateDestroyAPIView
from apps.post.serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated
from apps.post.models import Post


class PostDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
