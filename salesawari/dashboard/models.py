from django.db import models
from accounts.models import Account
from seller.models import *
from uuid import uuid4

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True

def generate_slug():
    return str(uuid4())[:8]

class Bargain(TimeStampedModel):
    slug = models.SlugField(max_length=32, unique=True, blank=True, default=generate_slug)
    seller = models.ForeignKey(Account, on_delete=models.DO_NOTHING, related_name='bargain_seller')
    buyer = models.ForeignKey(Account, on_delete=models.DO_NOTHING, related_name='bargain_buyer')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"Bargain {self.slug} - {self.vehicle}"

    
class SoldVehicleHistory(TimeStampedModel):
    seller = models.ForeignKey(Account, on_delete=models.DO_NOTHING, related_name='sold_vehicle_seller')
    buyer = models.ForeignKey(Account, on_delete=models.DO_NOTHING, related_name='sold_vehicle_buyer')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.DO_NOTHING)
    sale_price = models.PositiveIntegerField()
    sold_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle} sold by {self.seller} to {self.buyer}"

class Order(TimeStampedModel):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    seller = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='order_seller')
    buyer = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='order_buyer')
    vehicle_price = models.PositiveIntegerField()
    is_confirmed = models.CharField(max_length=32, choices=(('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')))
    full_name = models.CharField(max_length=32, default="Khalid Test")
    email = models.EmailField(default="Khalid@email.com")
    phone = models.CharField(max_length=20, default=000)
    cnic = models.PositiveIntegerField(default=1234567890)
    address = models.TextField(default="")

    def __str__(self):
        return f"Order for {self.vehicle} - {self.is_confirmed}"
