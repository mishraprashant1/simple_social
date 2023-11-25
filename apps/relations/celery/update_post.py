from apps.relations.core.posts.sync_post import SyncPost
from celery import shared_task
from apps.post.models import Post


@shared_task
def update_post_async(post_uuid):
    post = Post.objects.get(uuid=post_uuid)
    add_post = SyncPost(post)
    add_post.sync_entire_post()
