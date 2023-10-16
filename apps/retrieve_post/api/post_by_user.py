from rest_framework.generics import ListAPIView
from apps.post.serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated
from apps.post.models import Post
from rest_framework.pagination import PageNumberPagination


from rest_framework.permissions import BasePermission


class CanViewPost(BasePermission):
    """
    Todo: Allows access only to friends, followers and self.
    """

    def has_permission(self, request, view):
        return True


class ViewPostPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 4


class PostByUserView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, CanViewPost]
    pagination_class = ViewPostPagination

    def get_queryset(self):
        user_uuid = self.kwargs['user_uuid']
        return Post.objects.filter(user__uuid=user_uuid).order_by('-created_at')
