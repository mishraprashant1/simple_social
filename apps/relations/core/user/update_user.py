from apps.relations.models import User as neoUser


def update_user(user):
    user_obj = neoUser.nodes.get_or_none(uuid=str(user.uuid))
    if not user_obj:
        user_obj = neoUser()
        user_obj.uuid = user.uuid
    user_obj.first_name = user.first_name
    user_obj.last_name = user.last_name
    user_obj.email = user.email
    user_obj.is_active = user.is_active
    user_obj.is_staff = user.is_staff
    user_obj.is_superuser = user.is_superuser
    user_obj.date_joined = user.date_joined
    user_obj.save()
