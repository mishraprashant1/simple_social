from apps.relations.models import User


def is_friend(user1_uuid, user2_uuid):
    user1 = User.nodes.get(uuid=user1_uuid)
    return user1.friends.filter(uuid=user2_uuid).get_or_none() is not None
