from django.db import models
from accounts.models import Account

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class ContactUs(TimeStampedModel):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=32)
    email = models.EmailField()
    phone_number = models.CharField(max_length=32, null=True, blank=True)
    message = models.TextField()


    def __str__(self):
        return self.full_name