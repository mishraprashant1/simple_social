from rest_framework import generics
from apps.relations.serializers.friend_recommendation import FriendRecommendationSerializer
from rest_framework.permissions import IsAuthenticated
from simple_social.models import User
from rest_framework.pagination import PageNumberPagination


class FriendRecommendationPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20


class FriendRecommendationView(generics.ListAPIView):
    serializer_class = FriendRecommendationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = FriendRecommendationPagination

    def get_queryset(self):
        recommendations = self.request.user.get_friend_recommendations()
        recommendations = [item.decode('utf-8') for item in recommendations]
        users = User.objects.filter(uuid__in=recommendations)
        return users
