from apps.relations.core.user.update_user import update_user
from celery import shared_task


@shared_task
def update_user_async(user_uuid):
    from simple_social.models import User
    user = User.objects.get(uuid=user_uuid)
    update_user(user)
