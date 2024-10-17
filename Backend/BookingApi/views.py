from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ReservationSerializer, PostSerializer
from .models import Reservation, Post
from django.utils.dateparse import parse_time  
from datetime import time

class ReservationView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to create a reservation!'}, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data.copy()
        data['user'] = request.user.id
        date = data.get('date')

        start_time = parse_time(data.get('start_time'))
        end_time = parse_time(data.get('end_time'))

        if not date or not start_time or not end_time:
            return Response({'error': 'Invalid date or time provided!'}, status=status.HTTP_400_BAD_REQUEST)
        overlapping_reservations = Reservation.objects.filter(
            date=date, 
            start_time__lt=end_time, 
            end_time__gt=start_time 
        )
        if overlapping_reservations.exists():
            return Response({'error': 'This time slot is already booked on this day!'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReservationSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, reservation_id=None):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to see your reservations!'}, status=status.HTTP_401_UNAUTHORIZED)

        if reservation_id is not None:
            try:
                reservation = Reservation.objects.get(id=reservation_id, user=request.user)
                serializer = ReservationSerializer(reservation)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Reservation.DoesNotExist:
                return Response({'error': 'Reservation not found or you do not have permission to access this reservation.'}, status=status.HTTP_404_NOT_FOUND)

        reservations = Reservation.objects.filter(user=request.user)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def delete(self,request, reservation_id):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to delete a reservation!'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            reservation = Reservation.objects.get(id=reservation_id, user= request.user)
        except Reservation.DoesNotExist:
            return Response({'error': 'Reservation not found or you do not have permission to delete this reservation.'}, status=status.HTTP_404_NOT_FOUND)
        reservation.delete()
        return Response({'message': 'Reservation deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)



class AllReservationsView(APIView):
    def get(self,request):
        if not request.user.is_authenticated:
                return Response({'error': 'You must be logged in to see all reservations!'}, status=status.HTTP_401_UNAUTHORIZED)
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to create a post!'}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data.copy()
        data['user'] = request.user.id  

        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user = request.user)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, post_id=None):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to see your posts!'}, status=status.HTTP_401_UNAUTHORIZED)

        if post_id is not None:
            try:
                post = Post.objects.get(id=post_id, user=request.user)
                serializer = PostSerializer(post)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Post.DoesNotExist:
                return Response({'error': 'Post not found or you do not have permission to access this post.'}, status=status.HTTP_404_NOT_FOUND)

        
        posts = Post.objects.filter(user=request.user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self,request, post_id):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to delete a post!'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            post = Post.objects.get(id=post_id, user= request.user)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found or you do not have permission to delete this post.'}, status=status.HTTP_404_NOT_FOUND)
        post.delete()
        return Response({'message': 'Post deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


class AllPostView(APIView):
    def get(self,request):
        if not request.user.is_authenticated:
                return Response({'error': 'You must be logged in to see all posts!'}, status=status.HTTP_401_UNAUTHORIZED)
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)