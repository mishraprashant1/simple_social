from django.db import models
from apps.core.models.base import TimeStampedModel
import uuid


class ActionTaken(models.TextChoices):
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    CANCELLED = 'CANCELLED'


class FriendRequest(TimeStampedModel):
    ActionTaken = ActionTaken

    from_user = models.ForeignKey(
        'simple_social.User',
        related_name='friend_requests_sent',
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        'simple_social.User',
        related_name='friend_requests_received',
        on_delete=models.CASCADE
    )

    user1 = models.PositiveBigIntegerField(db_index=True)
    user2 = models.PositiveBigIntegerField(db_index=True)

    action_taken = models.CharField(choices=ActionTaken.choices, max_length=20, null=True, blank=True)
    action_taken_on = models.DateTimeField(null=True, blank=True)

    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)

    def __str__(self):
        return f'Request Sent from {self.from_user} to {self.to_user}'
