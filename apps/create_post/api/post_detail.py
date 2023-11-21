from rest_framework.generics import RetrieveUpdateDestroyAPIView
from apps.post.serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated
from apps.post.models import Post, PostImage, PostTags
from rest_framework.response import Response
from rest_framework import status


class PostDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    lookup_field = 'uuid'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        PostImage.handle_delete(instance)
        PostTags.handle_delete(instance)
        return Response({'status': 'Post Deleted Successfully!'}, status=status.HTTP_204_NO_CONTENT)
