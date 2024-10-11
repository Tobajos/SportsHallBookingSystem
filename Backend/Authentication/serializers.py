from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password


class RegisterUserSerializer(serializers.Serializer):
    firstname = serializers.CharField(required=False, allow_blank=True)
    lastname = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    
    def validate_password(self,value):
        validate_password(value)
        return value
    
    def validate_email(self,value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email is already in use!')
        return value
    
    def create(self,validated_data):  
        print(validated_data)
        user = CustomUser.objects.create_user(**validated_data)
        return user
    