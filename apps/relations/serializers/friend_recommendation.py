from rest_framework import serializers
from simple_social.models import User
from django.urls import reverse


class FriendRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'uuid', 'full_name', 'fr_url']

    full_name = serializers.SerializerMethodField()
    fr_url = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    def get_fr_url(self, obj):
        return reverse('send_friend_request', kwargs={'to_user_uuid': obj.uuid})
