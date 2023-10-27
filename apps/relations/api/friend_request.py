from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.relations.models import FriendRequest
from simple_social.models import User
from django.utils import timezone
from apps.relations.celery.friend_request import add_friend


def handle_create_friend_request(from_user, to_user):
    if from_user == to_user:
        return False
    user1 = min(from_user.id, to_user.id)
    user2 = max(from_user.id, to_user.id)
    if FriendRequest.objects.filter(user1=user1, user2=user2, action_taken__isnull=True).exists():
        return False
    fr = FriendRequest()
    fr.from_user = from_user
    fr.to_user = to_user
    fr.user1 = user1
    fr.user2 = user2
    fr.save()
    return True


def handle_delete_friend_request(from_user, to_user):
    if from_user == to_user:
        return False
    if FriendRequest.objects.filter(from_user=from_user, to_user=to_user, action_taken__isnull=True).exists():
        fr = FriendRequest.objects.get(from_user=from_user, to_user=to_user, action_taken__isnull=True)
        fr.action_taken = FriendRequest.ActionTaken.CANCELLED
        fr.action_taken_on = timezone.now()
        fr.save()
        return True
    return False


def handle_accept_friend_request(from_user, to_user):
    if from_user == to_user:
        return False
    if FriendRequest.objects.filter(from_user=from_user, to_user=to_user, action_taken__isnull=True).exists():
        fr = FriendRequest.objects.get(from_user=from_user, to_user=to_user, action_taken__isnull=True)
        fr.action_taken = FriendRequest.ActionTaken.ACCEPTED
        fr.action_taken_on = timezone.now()
        fr.save()
        add_friend.delay(from_user.uuid, to_user.uuid)
        return True
    return False


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
        to_user = User.objects.get(uuid=kwargs['to_user_uuid'])
        resp = handle_delete_friend_request(request.user, to_user)
        if resp:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class AcceptFriendRequestView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        from_user = User.objects.get(uuid=kwargs['to_user_uuid'])
        resp = handle_accept_friend_request(from_user, request.user)
        if resp:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
