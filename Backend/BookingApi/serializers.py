from rest_framework import serializers
from .models import Reservation, Post, Comment
from Authentication.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'firstname','lastname']

class ReservationSerializer(serializers.ModelSerializer):  
    user=UserSerializer(read_only = True)
    participants = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Reservation
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    
    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)

    class Meta:
        model = Comment
        fields = '__all__'