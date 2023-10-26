from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from apps.relations.celery.update_user import update_user_async


class User(AbstractUser):
    country_code = models.CharField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    uuid = models.UUIDField(editable=False, default=uuid4, db_index=True, unique=True)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        update_user_async.delay(str(self.uuid))
