from apps.relations.core.posts.sync_post import SyncPost
from celery import shared_task


@shared_task
def update_post_async(post):
    add_post = SyncPost(post)
    add_post.sync_entire_post()
