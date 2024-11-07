from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

urlpatterns = [
    path('register', register_view, name='register'),
    path('login', login_view, name='login'),

    path('doctor/create', create_doctor, name='create_doctors'),
    path('doctor/update', update_doctor, name='update_doctors'),
    path('doctor/<int:doctor_id>/get', get_doctor, name='get_doctor'),
    path('doctors/get', get_doctors, name='get_doctors'),

    path('user', get_user, name='get_user'),
    path('user/update', update_user, name='update_user'),

    path('appointment/create/<int:doctor_id>', create_appointment, name='create_appointment'),
    path('appointment/update/<int:appointment_id>', update_appointment, name='update_appointment'),
    path('appointment/<int:appointment_id>/get', get_appointment, name='get_appointment'),
    path('appointments/user/get', get_appointments_for_user, name='get_appointments_for_user'),
    path('appointments/doctor/get', get_appointments_for_doctor, name='get_appointments_for_doctor'),

    path('transaction/create/<int:appointment_id>', create_transaction, name='create_transaction'),
]

urlpatterns = format_suffix_patterns(urlpatterns)