from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super().update(deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)

    def all(self, *args, **kwargs):
        kwargs['deleted_at__isnull'] = True
        return super().filter(*args, **kwargs)

    def filter(self, *args, **kwargs):
        if 'deleted_at__isnull' not in kwargs:
            kwargs['deleted_at__isnull'] = True
        return super().filter(*args, **kwargs)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        kwargs['deleted_at__isnull'] = True
        return self.get_queryset().filter(*args, **kwargs)


class SoftDeleteModel(TimeStampedModel):
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        abstract = True
