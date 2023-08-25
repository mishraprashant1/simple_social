from rest_framework import serializers
from apps.post.models import Post, PostImage, PostLike, PostComment, PostTags


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
        return post


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
