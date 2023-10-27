from apps.relations.models import User
from celery import shared_task


@shared_task
def add_friend(from_user, to_user):
    try:
        user1 = User.nodes.get(uuid=from_user)
        user2 = User.nodes.get(uuid=to_user)
        user1.friends.connect(user2)
    except Exception as e:
        print(e)
