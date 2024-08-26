from django.db import models
from accounts.models import Account
from seller.models import Vehicle
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True
class FavouriteVehicle(TimeStampedModel):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='fav')

    def __str__(self):
        return f"{self.user.full_name} - {self.vehicle.name}"

