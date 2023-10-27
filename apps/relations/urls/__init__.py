from django.urls import path
from apps.relations.api.friend_request import SendFriendRequestView, CancelFriendRequestView, AcceptFriendRequestView

urlpatterns = [
    path('api/send_friend_requests/<uuid:to_user_uuid>', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('api/cancel_friend_requests/<uuid:to_user_uuid>', CancelFriendRequestView.as_view(),
         name='cancel_friend_request'),
    path('api/accept_friend_requests/<uuid:to_user_uuid>', AcceptFriendRequestView.as_view(),
         name='accept_friend_request'),
]
