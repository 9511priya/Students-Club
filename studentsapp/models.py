from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=300, blank=True, null=True)
    last_name = models.CharField(max_length=300, blank=True, null=True)
    shu_id = models.CharField(max_length=300, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ("shu_id",)


class Events(models.Model):
    event_id = models.CharField(max_length=50, null=False, blank=False)
    event_name = models.CharField(max_length=50, null=False, blank=False)
    event_date_time = models.DateTimeField(null=False, blank=False)
    event_place = models.TextField()

    class Meta:
        unique_together = ("event_id",)


class EventsRegistered(models.Model):
    event_id = models.ForeignKey(Events, null=False, blank=False, on_delete=models.CASCADE, default="-")
    student_id = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, default="-")

    class Meta:
        unique_together = ("event_id", "student_id")


# SPORTS
class Sports(models.Model):
    sport_id = models.CharField(max_length=50, null=False, blank=False)
    sport_name = models.CharField(max_length=50, null=False, blank=False)
    sport_date_time = models.DateTimeField(null=False, blank=False)
    sport_place = models.TextField()

    class Meta:
        unique_together = ("sport_id",)


class SportsRegistered(models.Model):
    sport_id = models.ForeignKey(Sports, null=False, blank=False, on_delete=models.CASCADE, default="-")
    student_id = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, default="-")

    class Meta:
        unique_together = ("sport_id", "student_id")


class Accommodation(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    gender_choices = [("male", "male"), ("female", "female"), ("any", "any")]
    city = models.CharField(null=False, blank=False, max_length=500)
    state = models.CharField(null=False, blank=False, max_length=500)
    contact = models.CharField(null=False, blank=False, max_length=500)
    gender_type = models.CharField(choices=gender_choices, null=False, blank=False, max_length=500)
    available = models.BooleanField(default=True)
    availability_count = models.IntegerField(null=False, default=0)
    address1 = models.TextField()
    address2 = models.TextField()
