from django.core.management.base import BaseCommand
from apps.post.core.timeline import TimelineManager, MyTimelineManager
from apps.post.models import Post
from simple_social.models import User


class Command(BaseCommand):
    help = 'Build friend recommendations in redis'

    def handle(self, *args, **options):
        posts = Post.objects.all()
        for i, post in enumerate(posts):
            tm = TimelineManager(post)
            tm.add_to_timeline()
        self.stdout.write(self.style.SUCCESS('Successfully built user timeline'))

        users = User.objects.all()
        for i, user in enumerate(users):
            tm = MyTimelineManager()
            tm.build_user_timeline(user)
        self.stdout.write(self.style.SUCCESS('Successfully built my timeline'))
