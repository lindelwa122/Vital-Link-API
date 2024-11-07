from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import *

class UserReadSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'age', 'gender', 'email']

    def get_age(self, obj):
        return obj.get_age()

    def get_gender(self, obj):
        return obj.get_gender()

class UserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super(UserWriteSerializer, self).create(validated_data)

class DoctorSerializer(serializers.ModelSerializer):
    user = UserReadSerializer()

    class Meta:
        model = Doctor
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    user = UserReadSerializer()
    doctor = DoctorSerializer()

    class Meta:
        model = Appointment
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    appointment = AppointmentSerializer()

    class Meta:
        model = Transaction
        fields = '__all__'
