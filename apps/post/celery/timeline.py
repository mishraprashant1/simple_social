from celery import shared_task
from apps.post.models import Post
from apps.post.core.timeline import TimelineManager, MyTimelineManager
from simple_social.models import User


@shared_task()
def add_to_timeline(post_uuid):
    post = Post.objects.get(uuid=post_uuid)
    TimelineManager(post).add_to_timeline()


@shared_task()
def remove_from_timeline(post_uuid):
    post = Post.objects.get(uuid=post_uuid)
    TimelineManager(post).remove_from_timeline()


@shared_task()
def add_to_user_timeline(post_uuid, user_uuid):
    post = Post.objects.get(uuid=post_uuid)
    user = User.objects.get(uuid=user_uuid)
    TimelineManager(post).add_to_user_timeline(user)


@shared_task()
def remove_from_user_timeline(post_uuid, user_uuid):
    post = Post.objects.get(uuid=post_uuid)
    user = User.objects.get(uuid=user_uuid)
    TimelineManager(post).remove_from_user_timeline(user)


@shared_task()
def add_to_my_timeline(post_uuid):
    post = Post.objects.get(uuid=post_uuid)
    MyTimelineManager(post).add_to_timeline()


@shared_task()
def remove_from_my_timeline(post_uuid):
    post = Post.objects.get(uuid=post_uuid)
    MyTimelineManager(post).remove_from_timeline()


@shared_task()
def sync_post_between_users(user1_uuid, user2_uuid, action='ADD'):
    user1 = User.objects.get(uuid=user1_uuid)
    user2 = User.objects.get(uuid=user2_uuid)
    posts = Post.objects.filter(user=user1)
    for post in posts:
        if action == 'ADD':
            TimelineManager(post).add_to_user_timeline(user2)
        else:
            TimelineManager(post).remove_from_user_timeline(user2)
    posts = Post.objects.filter(user=user2)
    for post in posts:
        if action == 'ADD':
            TimelineManager(post).add_to_user_timeline(user1)
        else:
            TimelineManager(post).remove_from_user_timeline(user1)
