from django.urls import path
from apps.relations.api.friend_request import (SendFriendRequestView, CancelFriendRequestView, AcceptFriendRequestView,
                                               RejectFriendRequestView, UnfriendView, FriendRequestReceived,
                                               FriendRequestSent)
from apps.relations.api.friend_recommendation import FriendRecommendationView

urlpatterns = [
    path('api/send_friend_requests/<uuid:to_user_uuid>', SendFriendRequestView.as_view(),
         name='send_friend_request'),
    path('api/cancel_friend_requests/<uuid:fr_uuid>', CancelFriendRequestView.as_view(),
         name='cancel_friend_request'),
    path('api/accept_friend_requests/<uuid:fr_uuid>', AcceptFriendRequestView.as_view(),
         name='accept_friend_request'),
    path('api/reject_friend_requests/<uuid:fr_uuid>', RejectFriendRequestView.as_view(),
         name='reject_friend_request'),
    path('api/unfriend/<uuid:to_user_uuid>', UnfriendView.as_view(),
         name='unfriend_user'),
    path('api/friend_recommendations', FriendRecommendationView.as_view(),
         name='friend_recommendations'),
    path('api/friend_requests_received', FriendRequestReceived.as_view(),
         name='friend_requests_received'),
    path('api/friend_requests_sent', FriendRequestSent.as_view(),
         name='friend_requests_sent'),
]
