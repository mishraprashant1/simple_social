from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.relations.models import FriendRequest
from simple_social.models import User
from django.utils import timezone
from apps.relations.celery.friend_request import add_friend, remove_friend
from django.db.models import Q
from apps.post.celery.timeline import sync_post_between_users
from apps.relations.serializers.friend_request import ReceivedFriendRequestSerializer, SentFriendRequestSerializer


def handle_create_friend_request(from_user, to_user):
    if from_user == to_user:
        return False
    user1 = min(from_user.id, to_user.id)
    user2 = max(from_user.id, to_user.id)
    if FriendRequest.objects.filter(
            Q(action_taken__isnull=True) | (Q(action_taken=FriendRequest.ActionTaken.ACCEPTED) & Q(unfriend=False)),
            user1=user1,
            user2=user2
    ).exists():
        return False
    fr = FriendRequest()
    fr.from_user = from_user
    fr.to_user = to_user
    fr.user1 = user1
    fr.user2 = user2
    fr.save()
    return True


def handle_friend_request(from_user, to_user, action):
    if from_user == to_user:
        return False
    if FriendRequest.objects.filter(from_user=from_user, to_user=to_user, action_taken__isnull=True).exists():
        fr = FriendRequest.objects.get(from_user=from_user, to_user=to_user, action_taken__isnull=True)
        fr.action_taken = action
        fr.action_taken_on = timezone.now()
        fr.save()
        return True
    return False


def handle_friend_request_v2(fr, action):
    if fr.action_taken is not None:
        return False
    fr.action_taken = action
    fr.action_taken_on = timezone.now()
    fr.save()
    return True


class SendFriendRequestView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        to_user = User.objects.get(uuid=kwargs['to_user_uuid'])
        resp = handle_create_friend_request(request.user, to_user)
        if resp:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CancelFriendRequestView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        fr_uuid = kwargs['fr_uuid']
        fr = FriendRequest.objects.get(uuid=fr_uuid)
        if fr.from_user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        resp = handle_friend_request_v2(fr, FriendRequest.ActionTaken.CANCELLED)
        if resp:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class AcceptFriendRequestView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        fr_uuid = kwargs['fr_uuid']
        fr = FriendRequest.objects.get(uuid=fr_uuid)
        if fr.to_user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        resp = handle_friend_request_v2(fr, FriendRequest.ActionTaken.ACCEPTED)
        if resp:
            add_friend.delay(fr.from_user.uuid, fr.to_user.uuid)
            sync_post_between_users.delay(fr.from_user.uuid, fr.to_user.uuid)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RejectFriendRequestView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        fr_uuid = kwargs['fr_uuid']
        fr = FriendRequest.objects.get(uuid=fr_uuid)
        if fr.to_user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        resp = handle_friend_request_v2(fr, FriendRequest.ActionTaken.REJECTED)
        if resp:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UnfriendView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        to_user = User.objects.get(uuid=kwargs['to_user_uuid'])
        if to_user == request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user1 = min(request.user.id, to_user.id)
        user2 = max(request.user.id, to_user.id)
        if FriendRequest.objects.filter(user1=user1, user2=user2, action_taken=FriendRequest.ActionTaken.ACCEPTED,
                                        unfriend=False).exists():
            fr = FriendRequest.objects.get(user1=user1, user2=user2, action_taken=FriendRequest.ActionTaken.ACCEPTED,
                                           unfriend=False)
            fr.unfriend = True
            fr.unfriend_on = timezone.now()
            fr.save()
            remove_friend.delay(fr.from_user.uuid, fr.to_user.uuid)
            sync_post_between_users.delay(fr.from_user.uuid, fr.to_user.uuid, action='REMOVE')
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class FriendRequestReceived(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReceivedFriendRequestSerializer

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, action_taken__isnull=True)


class FriendRequestSent(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SentFriendRequestSerializer

    def get_queryset(self):
        return FriendRequest.objects.filter(from_user=self.request.user, action_taken__isnull=True)
