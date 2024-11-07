from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import localtime

from datetime import datetime

from .validators import *

class User(AbstractUser):
    identification_number = models.CharField(max_length=13, validators=[validate_identification_num])
    phone_number = models.CharField(max_length=10, validators=[validate_phone_num])

    def get_gender(self):
        gender_id = self.identification_number[6:10]
        if int(gender_id) < 5000: return 'female'
        else: return 'male'

    def get_age(self):
        current_year = datetime.now().year
        age_id = self.identification_number[:2]
        if int(age_id) <= 24:
            return current_year - int('20'+age_id)
        else:
            return current_year - int('19'+age_id)

class Doctor(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='user_as_doctor')
    title = models.CharField(max_length=10)
    specialization = models.CharField(max_length=50)
    profile = models.TextField(max_length=5000)
    career_paths = models.TextField(max_length=5000)
    highlights = models.TextField(max_length=5000)
    focus = models.TextField(max_length=5000)
    experience = models.IntegerField()
    location = models.CharField(max_length=200)
    rating = models.IntegerField()
    charging_rate = models.FloatField(default=0)

    def __str__(self):
        return f'Dr. {self.user.last_name}'

class Appointment(models.Model):
    STATUS_CHOICES = {
        'wait': 'Waiting Approval',
        'approved': 'Approved'
    }

    user = models.ForeignKey(User, models.CASCADE, related_name='user_appointment')
    doctor = models.ForeignKey(Doctor, models.CASCADE, related_name='doctor_appointment')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='wait')
    description = models.TextField(max_length=2000)
    datetime = models.DateTimeField()

    def __str__(self):
        return f'An appointment between {self.user.first_name} and Dr.{self.doctor.user.last_name}'

class Transaction(models.Model):
    appointment = models.ForeignKey(Appointment, models.CASCADE, related_name='appointment_transaction')
    amount_paid = models.FloatField()
    datetime = models.DateTimeField(auto_created=True, default=localtime)
