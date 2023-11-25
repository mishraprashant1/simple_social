from rest_framework import serializers
from django.urls import reverse
from apps.relations.models import FriendRequest


class ReceivedFriendRequestSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    accept_fr = serializers.SerializerMethodField()
    reject_fr = serializers.SerializerMethodField()
    user_uuid = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ['full_name', 'accept_fr', 'reject_fr', 'created_at', 'uuid', 'user_uuid']

    def get_full_name(self, obj):
        return f'{obj.from_user.first_name} {obj.from_user.last_name}'

    def get_accept_fr(self, obj):
        return reverse('accept_friend_request', kwargs={'fr_uuid': obj.uuid})

    def get_reject_fr(self, obj):
        return reverse('reject_friend_request', kwargs={'fr_uuid': obj.uuid})

    def get_user_uuid(self, obj):
        return str(obj.from_user.uuid)


class SentFriendRequestSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    cancel_fr = serializers.SerializerMethodField()
    user_uuid = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ['full_name', 'cancel_fr', 'created_at', 'uuid', 'user_uuid']

    def get_full_name(self, obj):
        return f'{obj.from_user.first_name} {obj.from_user.last_name}'

    def get_cancel_fr(self, obj):
        return reverse('cancel_friend_request', kwargs={'fr_uuid': obj.uuid})

    def get_user_uuid(self, obj):
        return str(obj.to_user.uuid)
