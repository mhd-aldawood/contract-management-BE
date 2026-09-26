from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .educational_content.models import EducationalContent, PaymentScheduleItem  # noqa: F401


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} profile'


@receiver(post_save, sender=User)
def create_profile_and_token(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Token.objects.get_or_create(user=instance)



class PaymentScheduleRowBase(models.Model):
    label = models.CharField(max_length=250, blank=True, default='')
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    due_date = models.DateField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.pk} — {self.amount} @ {self.due_date}'