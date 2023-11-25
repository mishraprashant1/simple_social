from rest_framework import serializers
from apps.post.models import Post, PostImage, PostLike, PostComment, PostTags
from apps.relations.core.posts.sync_post import SyncPost
from apps.post.celery.timeline import add_to_timeline, remove_from_timeline
from apps.relations.celery.update_post import update_post_async


class PostImageSerializer(serializers.ModelSerializer):
    post_uuid = serializers.SerializerMethodField()

    class Meta:
        model = PostImage
        fields = ['image', 'post_uuid']

    def create(self, validated_data):
        post_image = PostImage()
        post_image.post = validated_data['post']
        post_image.image = validated_data['image']
        post_image.save()

    def get_post_uuid(self, obj):
        return obj.post.uuid


class PostTagsSerializer(serializers.ModelSerializer):
    post_uuid = serializers.SerializerMethodField()

    class Meta:
        model = PostTags
        fields = ['tag', 'type', 'post_uuid']

    def create(self, validated_data):
        post_tags = PostTags()
        post_tags.post = validated_data['post']
        post_tags.tag = validated_data['tag']
        post_tags.type = validated_data['type']
        post_tags.save()

    def get_post_uuid(self, obj):
        return obj.post.uuid


class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True)
    tags = PostTagsSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'deleted_at', 'user')

    def create(self, validated_data):
        images = validated_data.pop('images')
        tags = validated_data.pop('tags')
        user = self.context['request'].user
        post = Post.objects.create(user=user, **validated_data)
        for image in images:
            PostImage.objects.create(post=post, **image)
        for tag in tags:
            PostTags.objects.create(post=post, **tag)
        update_post_async.delay(post.uuid)
        if post.share_with == Post.ShareWithChoices.PUBLIC and post.is_active:
            add_to_timeline.delay(post.uuid)
        return post

    def update(self, instance, validated_data):
        did_share_with_change = False
        old_share_with = instance.share_with
        new_share_with = validated_data.get('share_with', instance.share_with)
        if old_share_with != new_share_with:
            did_share_with_change = True

        post_deactivated = False
        if instance.is_active and not validated_data.get('is_active', instance.is_active):
            post_deactivated = True

        post_active = False
        if not instance.is_active and validated_data.get('is_active', instance.is_active):
            post_active = True

        images = validated_data.pop('images', None)
        tags = validated_data.pop('tags', None)
        instance.text_content = validated_data.get('text_content', instance.text_content)
        instance.share_with = validated_data.get('share_with', instance.share_with)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()

        if images is not None:
            images = [i['image'] for i in images]
            PostImage.update_post_image(instance, images)
        if tags is not None:
            PostTags.update_post_tags(instance, tags)
        update_post_async.delay(instance.uuid)

        if (did_share_with_change and old_share_with == Post.ShareWithChoices.ONLY_ME) or post_active:
            add_to_timeline.delay(str(instance.uuid))
        elif (did_share_with_change and new_share_with == Post.ShareWithChoices.ONLY_ME) or post_deactivated:
            remove_from_timeline.delay(str(instance.uuid))

        return instance


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'deleted_at')

    def create(self, validated_data):
        post_like = PostLike()
        post_like.post = validated_data['post']
        post_like.user = self.context['request'].user
        post_like.save()


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'deleted_at')

    def create(self, validated_data):
        post_comment = PostComment()
        post_comment.post = validated_data['post']
        post_comment.user = self.context['request'].user
        post_comment.replied_to = validated_data['replied_to']
        post_comment.text_content = validated_data['text_content']
        post_comment.save()
