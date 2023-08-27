from django.db import models

from apps.core.models.base import TimeStampedModel, SoftDeleteModel


class Post(SoftDeleteModel):
    class ShareWithChoices(models.TextChoices):
        PUBLIC = 'PUBLIC', 'Public'
        FRIENDS = 'FRIENDS', 'Friends'
        ONLY_ME = 'ONLY_ME', 'Only Me'

    user = models.ForeignKey('simple_social.User', on_delete=models.CASCADE, related_name='posts')
    text_content = models.TextField()
    share_with = models.CharField(max_length=50, choices=ShareWithChoices.choices, default=ShareWithChoices.FRIENDS)
    is_active = models.BooleanField(default=True)


class PostImage(SoftDeleteModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.URLField()


class PostTags(SoftDeleteModel):
    class TypeChoices(models.TextChoices):
        HASHTAG = 'HASHTAG', 'Hashtag'
        MENTION = 'MENTION', 'Mention'
        LOCATION = 'LOCATION', 'Location'

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='tags')
    tag = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=TypeChoices.choices)


class PostLike(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey('simple_social.User', on_delete=models.CASCADE, related_name='likes')


class PostComment(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('simple_social.User', on_delete=models.CASCADE, related_name='comments')
    replied_to = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    text_content = models.TextField()
    is_active = models.BooleanField(default=True)