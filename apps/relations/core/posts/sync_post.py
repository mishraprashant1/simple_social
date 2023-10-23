from apps.post.models import Post
from apps.relations.models import Posts, User, PostImage, PostTags


class SyncPost:
    def __init__(self, post: Post):
        self.post = post
        self.post_image = post.images.all()
        self.post_tags = post.tags.all()
        self.user = User.nodes.get(uuid=str(self.post.user.uuid))

    def sync_post(self):
        post = Posts.nodes.get_or_none(uuid=str(self.post.uuid))
        if post:
            post.text_content = self.post.text_content
            post.share_with = self.post.share_with
            post.is_active = self.post.is_active
            post.updated_at = self.post.updated_at
            post.save()
        else:
            post = Posts()
            post.uuid = str(self.post.uuid)
            post.text_content = self.post.text_content
            post.share_with = self.post.share_with
            post.is_active = self.post.is_active
            post.created_at = self.post.created_at
            post.updated_at = self.post.updated_at
            post.save()
            self.user.posts.connect(post)
        return post

    def update_post_image(self, post):
        post_images_neo = {img.uuid for img in post.images.all()}
        post_images_pg = {str(img.uuid) for img in self.post_image}
        to_insert = post_images_pg - post_images_neo
        to_delete = post_images_neo - post_images_pg
        for image in self.post_image.filter(uuid__in=to_insert):
            post_image = PostImage()
            post_image.uuid = image.uuid
            post_image.image = image.image
            post_image.save()
            post.images.connect(post_image)
        for image in PostImage.nodes.filter(uuid__in=list(to_delete)):
            post.images.disconnect(image)
            image.delete()

    def update_post_tags(self, post):
        post_tags_neo = {tag.uuid for tag in post.tags.all()}
        post_tags_pg = {str(tag.uuid) for tag in self.post_tags}
        to_insert = post_tags_pg - post_tags_neo
        to_delete = post_tags_neo - post_tags_pg
        for tag in self.post_tags.filter(uuid__in=to_insert):
            post_tag = PostTags()
            post_tag.uuid = tag.uuid
            post_tag.tag = tag.tag
            post_tag.type = tag.type
            post_tag.save()
            post.tags.connect(post_tag)
        for tag in PostTags.nodes.filter(uuid__in=list(to_delete)):
            post.tags.disconnect(tag)
            tag.delete()

    @staticmethod
    def delete_post(post):
        pass

    def sync_entire_post(self):
        post = self.sync_post()
        self.update_post_image(post)
        self.update_post_tags(post)
