from django.db import models
from django.urls import reverse
import uuid


# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.id})


class ParticipantType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, default='0000000000')
    type = models.ForeignKey(ParticipantType, on_delete=models.SET_NULL, null=True, related_name='participants')
    qr_code_reference = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    in_event = models.BooleanField(default=False)
    time_in = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class CouponType(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.name
    

class AccessCoupon(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    coupon_type = models.ForeignKey(CouponType, on_delete=models.CASCADE)
    redeemed = models.BooleanField(default=False)
    redeemed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.participant.full_name} - {self.coupon_type.name}"

