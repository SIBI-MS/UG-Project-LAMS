from django.db import models
from django.utils import timezone
from datetime import timedelta


# Create your models here.
class Student(models.Model):
    card_id= models.IntegerField(primary_key=True, default=0)
    admission_no = models.IntegerField(default=0)
    name = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    department = models.CharField(max_length=50)
    level = models.CharField(max_length=50)
    phone = models.CharField(max_length=10,default=0)
    sex = models.CharField(max_length=50,default='gender')
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    time_spend=models.IntegerField(default=0)

    def __str__(self):
        if self.name is None:
            return str(self.card_id)
        else:
            return str(self.name) 


class Log(models.Model):
    card_id = models.IntegerField(default=0)
    admission_no = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    level = models.CharField(max_length=50)
    date = models.DateField(default=timezone.now)  # Use timezone.now for date
    time_in = models.TimeField(default=timezone.now)  # Use timezone.now for time_in
    time_out = models.TimeField(blank=True, null=True)
    total_hours=models.CharField(max_length=50)
    status = models.TextField(max_length=100)

    def __str__(self):
        return str(self.name) + ' : ' + str(self.date)

