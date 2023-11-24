from django.conf import settings
from apps.post.models import Post
from apps.relations.models import User


class TimelineManager:
    def __init__(self, post: Post):
        self.post = post
        self.user = post.user
        self.redis_conn = settings.REDIS_CONNECTION

    def add_to_timeline(self):
        user_node = User.nodes.get(uuid=self.user.uuid)
        friends = user_node.friends.all()
        for friend in friends:
            self.redis_conn.zadd(f"timeline:{str(friend.uuid)}",
                                 {str(self.post.uuid): self.post.created_at.timestamp()})

    def remove_from_timeline(self):
        user_node = User.nodes.get(uuid=self.user.uuid)
        friends = user_node.friends.all()
        for friend in friends:
            self.redis_conn.zrem(f"timeline:{str(friend.uuid)}", str(self.post.uuid))

    def add_to_user_timeline(self, user: User):
        self.redis_conn.zadd(f"timeline:{str(user.uuid)}", {str(self.post.uuid): self.post.created_at.timestamp()})

    def remove_from_user_timeline(self, user: User):
        self.redis_conn.zrem(f"timeline:{str(user.uuid)}", str(self.post.uuid))


class MyTimelineManager:
    def __init__(self, post: Post = None):
        self.post = post
        self.redis_conn = settings.REDIS_CONNECTION

    def add_to_timeline(self):
        self.redis_conn.zadd(f"my_timeline:{str(self.post.user.uuid)}",
                             {str(self.post.uuid): self.post.created_at.timestamp()})

    def remove_from_timeline(self):
        self.redis_conn.zrem(f"my_timeline:{str(self.post.user.uuid)}", str(self.post.uuid))

    def build_user_timeline(self, user: User):
        posts = Post.objects.filter(user=user)
        for post in posts:
            self.redis_conn.zadd(f"my_timeline:{str(user.uuid)}",
                                 {str(post.uuid): post.created_at.timestamp()})
