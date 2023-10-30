from django.core.management.base import BaseCommand
from simple_social.models import User
import pandas as pd
import uuid
from django.utils.text import slugify
import random
from apps.relations.models import FriendRequest
from apps.relations.api.friend_request import handle_create_friend_request
from apps.relations.celery.friend_request import add_friend


def create_mock_user():
    users = pd.read_csv('./simple_social/management/commands/dumps/users.csv')
    for row in users.iterrows():
        user = User.objects.create_user(
            username=slugify(row[1]['username']).replace('-', '_'),
            email=row[1]['email'],
            first_name=row[1]['first_name'],
            last_name=row[1]['last_name'],
            phone_number=row[1]['phone'],
            country_code=row[1]['country_code'],
            date_joined=row[1]['date_joined'],
            uuid=uuid.uuid4(),
        )
        user.save()
        try:
            user.set_password(row[1]['password'])
        except Exception as e:
            user.set_password('simple_social')
        user.save()


def create_mock_friendships():
    users = User.objects.all()
    user_mappings = dict()
    for user in users:
        user_mappings[user.id] = user
    users = list(User.objects.all().values_list('id', flat=True))
    left = 1
    right = 200
    for i, user in enumerate(users):
        if i < 100:
            left = 1
            right = 199
        elif 100 <= i < len(users) - 100:
            left = left + 1
            right = right + 1
        else:
            left = len(users) - 199
            right = len(users) - 1
        random_users = random.sample(range(left, right), random.randint(1, 150))
        for random_user in random_users:
            handle_create_friend_request(user_mappings[user], user_mappings[random_user])


def accept_reject_cancel_friend_requests():
    actions = [FriendRequest.ActionTaken.ACCEPTED] * 7 + [FriendRequest.ActionTaken.REJECTED] * 2 + [
        FriendRequest.ActionTaken.CANCELLED] * 1
    all_requests = FriendRequest.objects.filter(action_taken__isnull=True)
    for request in all_requests:
        action_taken = random.choice(actions)
        request.action_taken = action_taken
        request.action_taken_on = request.created_at
        request.save()
        if action_taken == FriendRequest.ActionTaken.ACCEPTED:
            add_friend.delay(request.from_user.uuid, request.to_user.uuid)


class Command(BaseCommand):
    help = "Create complete mock data for the app"

    def handle(self, *args, **options):
        create_mock_user()
        self.stdout.write(self.style.SUCCESS('Successfully created new mock users'))
        create_mock_friendships()
        self.stdout.write(self.style.SUCCESS('Successfully created new mock friendships'))
        accept_reject_cancel_friend_requests()
        self.stdout.write(self.style.SUCCESS('Successfully accepted/rejected/cancelled friend requests'))
