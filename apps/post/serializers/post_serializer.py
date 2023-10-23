from rest_framework import serializers
from apps.post.models import Post, PostImage, PostLike, PostComment, PostTags
from apps.relations.core.posts.sync_post import SyncPost


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'deleted_at', 'post')

    def create(self, validated_data):
        post_image = PostImage()
        post_image.post = validated_data['post']
        post_image.image = validated_data['image']
        post_image.save()


class PostTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTags
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'deleted_at', 'post')

    def create(self, validated_data):
        post_tags = PostTags()
        post_tags.post = validated_data['post']
        post_tags.tag = validated_data['tag']
        post_tags.type = validated_data['type']
        post_tags.save()


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
        SyncPost(post).sync_post()
        return post

    def update(self, instance, validated_data):
        images = validated_data.pop('images', None)
        tags = validated_data.pop('tags', None)
        instance.text_content = validated_data.get('text_content', instance.text_content)
        instance.share_with = validated_data.get('share_with', instance.share_with)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        if images is not None:
            PostImage.update_post_image(instance, images)
        if tags is not None:
            PostTags.update_post_tags(instance, tags)
        SyncPost(instance).sync_post()
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
