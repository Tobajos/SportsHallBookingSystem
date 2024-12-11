from rest_framework import serializers
from .models import Reservation, Post, Comment, Team
from Authentication.models import CustomUser
from django.utils.timezone import localtime

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'firstname','lastname']

class ReservationSerializer(serializers.ModelSerializer):  
    user=UserSerializer(read_only = True)
    participants = UserSerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()
    available_spots = serializers.SerializerMethodField()
    is_full = serializers.SerializerMethodField()
    
    class Meta:
        model = Reservation
        fields = '__all__'  
    def get_participant_count(self, obj):
        return obj.get_participant_count()

    def get_available_spots(self, obj):
        return obj.get_available_spots()

    def get_is_full(self, obj):
        return obj.is_full()

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    reservation = ReservationSerializer(read_only=True, required=False) 
    
    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        reservation_data = validated_data.pop('reservation', None)
        post = Post.objects.create(**validated_data)
        if reservation_data:
            post.reservation = reservation_data
        post.save()
        return post


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)

    class Meta:
        model = Comment
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    participants = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Team
        fields = '__all__'
