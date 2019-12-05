from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.


class CustomUser(AbstractUser):
    currency = models.ForeignKey('money_tracker.Currency', related_name='users', on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(editable=False, default=timezone.now())
    modified = models.DateTimeField(default=timezone.now())

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(CustomUser, self).save(*args, **kwargs)
