from rest_framework.generics import ListAPIView
from apps.post.serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated
from apps.post.models import Post
from rest_framework.pagination import PageNumberPagination
from apps.relations.core.is_friend import is_friend
from apps.post.core.timeline import MyTimelineManager, GetTimelinePosts
from django.db.models import Q

from rest_framework.permissions import BasePermission


class CanViewPost(BasePermission):
    """
    Todo: Restrict access to post if user is blocked
    """

    def has_permission(self, request, view):
        user_requested = str(request.user.uuid)
        other_user = str(view.kwargs['user_uuid'])
        # todo: check if other_user has blocked requested user
        return True


class ViewPostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20


class PostByUserView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, CanViewPost]
    pagination_class = ViewPostPagination

    def get_queryset(self):
        other_user = str(self.kwargs['user_uuid'])
        request_user = str(self.request.user.uuid)
        if is_friend(request_user, other_user):
            mtm = MyTimelineManager()
            post_uuids = mtm.get_posts(other_user)
            return Post.objects.filter(
                Q(uuid__in=post_uuids) | (Q(user__uuid=other_user) & Q(share_with=Post.ShareWithChoices.PUBLIC))
            ).order_by('-created_at')
        else:
            return Post.objects.filter(
                user__uuid=other_user, share_with=Post.ShareWithChoices.PUBLIC
            ).order_by('-created_at')


class GetTimelineView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ViewPostPagination

    def get_queryset(self):
        gtp = GetTimelinePosts()
        post_uuids = gtp.get_posts(self.request.user.uuid)
        return Post.objects.filter(uuid__in=post_uuids).order_by('-created_at')
