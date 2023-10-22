from django.db import models
from uuid import uuid4
from apps.core.models.base import TimeStampedModel, SoftDeleteModel


class Post(SoftDeleteModel):
    class ShareWithChoices(models.TextChoices):
        PUBLIC = 'PUBLIC', 'Public'
        FRIENDS = 'FRIENDS', 'Friends'
        ONLY_ME = 'ONLY_ME', 'Only Me'

    uuid = models.UUIDField(editable=False, default=uuid4, db_index=True, unique=True)
    user = models.ForeignKey('simple_social.User', on_delete=models.CASCADE, related_name='posts')
    text_content = models.TextField()
    share_with = models.CharField(max_length=50, choices=ShareWithChoices.choices, default=ShareWithChoices.FRIENDS)
    is_active = models.BooleanField(default=True)


class PostImage(SoftDeleteModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.URLField()

    @staticmethod
    def update_post_image(post: Post, images: []):
        ids_to_keep = []
        for image in images:
            obj, created = PostImage.objects.get_or_create(post=post, image=image)
            ids_to_keep.append(obj.id)
        PostImage.objects.filter(post=post).exclude(id__in=ids_to_keep).delete()

    @staticmethod
    def handle_delete(post: Post):
        PostImage.objects.filter(post=post).delete()


class PostTags(SoftDeleteModel):
    class TypeChoices(models.TextChoices):
        HASHTAG = 'HASHTAG', 'Hashtag'
        MENTION = 'MENTION', 'Mention'
        LOCATION = 'LOCATION', 'Location'

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='tags')
    tag = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=TypeChoices.choices)

    @staticmethod
    def update_post_tags(post: Post, tags: []):
        ids_to_keep = []
        for tag in tags:
            obj, created = PostTags.objects.get_or_create(post=post, tag=tag['tag'], type=tag['type'])
            ids_to_keep.append(obj.id)
        PostTags.objects.filter(post=post).exclude(id__in=ids_to_keep).delete()

    @staticmethod
    def handle_delete(post: Post):
        PostTags.objects.filter(post=post).delete()


class PostLike(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey('simple_social.User', on_delete=models.CASCADE, related_name='likes')


class PostComment(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('simple_social.User', on_delete=models.CASCADE, related_name='comments')
    replied_to = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    text_content = models.TextField()
    is_active = models.BooleanField(default=True)
