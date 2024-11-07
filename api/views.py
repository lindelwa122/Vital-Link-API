from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *

@api_view(['POST'])
@csrf_exempt
def register_view(request, format=None):
    serializer = UserWriteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(pk=serializer.data['id'])
        login(request, user)
        serializer = UserReadSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@csrf_exempt
def login_view(request, format=None):
    logout(request)
    username, password = request.data['username'], request.data['password']
    print(username, password) 
    user = authenticate(request, username=username, password=password)

    if user:
        login(request, user)
        doctor = Doctor.objects.get(user=user)
        if doctor:
            serializer = DoctorSerializer(doctor)
        else:
            serializer = UserReadSerializer(user)
        return Response(serializer.data)
    return Response(
        { 'error': 'Username/Password is invalid' }, 
        status=status.HTTP_401_UNAUTHORIZED
    )

@api_view(['POST'])
@csrf_exempt
def create_doctor(request, format=None):
    if not request.user.is_authenticated:
        return Response(
            { 'error': 'Unauthorized to create a doctor profile.' }, 
            status=status.HTTP_401_UNAUTHORIZED
        )

    serializer = DoctorSerializer(data={ 'user': request.user, **request.data })
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@csrf_exempt
def update_doctor(request, format=None):
    doctor = Doctor.objects.get(user=request.user)
    if not doctor:
        return Response({ 'error': 'Doctor not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = DoctorSerializer(doctor, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@csrf_exempt
def get_doctors(request, format=None):
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data, safe=False)

@api_view(['GET'])
@csrf_exempt
def get_doctor(request, doctor_id, format=None):
    doctor = Doctor.objects.get(pk=doctor_id)
    if doctor:
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)
    return Response({ 'error': 'Doctor not found.' }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@csrf_exempt
def get_user(request, format=None):
    if request.user.is_authenticated:
        # Check if user is a doctor
        doctor = Doctor.objects.get(user=request.user)
        if doctor:
            serializer = DoctorSerializer(doctor)
        else:
            serializer = UserReadSerializer(request.user)

        return Response(serializer.data)
    return Response(
        { 'error': 'User is not authenticated' }, 
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['PUT'])
@csrf_exempt
def update_user(request, format=None):
    serializer = UserWriteSerializer(request.user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@csrf_exempt
def create_appointment(request, doctor_id, format=None):
    doctor = Doctor.objects.get(pk=doctor_id)
    if not doctor:
        return Response({ 'error': 'Doctor not found.' }, status=status.HTTP_404_NOT_FOUND)

    serializer = AppointmentSerializer(data={ 'user': request.user, 'doctor': doctor, **request.data })
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@csrf_exempt
def update_appointment(request, appointment_id, format=None):
    appointment = Appointment.objects.get(pk=appointment_id)
    if not appointment:
        return Response({ 'error': 'Appointment not found.' }, status=status.HTTP_404_NOT_FOUND)

    serializer = AppointmentSerializer(appointment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@csrf_exempt
def get_appointment(request, appointment_id, format=None):
    appointment = Appointment.objects.get(pk=appointment_id)
    if not appointment:
        return Response({ 'error': 'Appointment not found.' }, status=status.HTTP_404_NOT_FOUND)

    serializer = AppointmentSerializer(appointment)
    return Response(serializer.data)

@api_view(['GET'])
@csrf_exempt
def get_appointments_for_user(request, format=None):
    appointments = Appointment.objects.filter(user=request.user)
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data, safe=False)

@api_view(['GET'])
@csrf_exempt
def get_appointments_for_doctor(request, format=None):
    doctor = Doctor.objects.get(user=request.user)
    if not doctor:
        return Response({ 'error': 'Doctor not found.' }, status=status.HTTP_404_NOT_FOUND)

    appointments = Appointment.objects.filter(doctor=doctor)
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data, safe=False)

@api_view(['POST'])
@csrf_exempt
def create_transaction(request, appointment_id, format=None):
    appointment = Appointment.objects.get(pk=appointment_id)
    if not appointment:
        return Response({ 'error': 'Appointment not found.' }, status=status.HTTP_404_NOT_FOUND)

    serializer = TransactionSerializer(data={ 'appointment': appointment, **request.data })
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
