from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ReservationSerializer, PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Reservation, Post, Comment
from django.utils.dateparse import parse_time  
from datetime import time
from rest_framework.authentication import TokenAuthentication
from .models import CustomUser

class ReservationView(APIView):
    # permission_classes=[IsAuthenticated]
    # authentication_classes=[TokenAuthentication]
    
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to create a reservation!'}, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data.copy()
        data['user'] = request.user.id
        date = data.get('date')

        start_time = parse_time(data.get('start_time'))
        end_time = parse_time(data.get('end_time'))

        if start_time >= end_time:
            return Response({'error': 'Start time cannot be later than end time!'}, status=status.HTTP_400_BAD_REQUEST)

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
        
    def delete(self, request, reservation_id):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to delete a reservation!'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            reservation = Reservation.objects.get(id=reservation_id)
            if request.user != reservation.user and not request.user.is_staff:
                return Response({'error': 'You do not have permission to delete this reservation.'}, status=status.HTTP_403_FORBIDDEN)
        except Reservation.DoesNotExist:
            return Response({'error': 'Reservation not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        reservation.delete()
        return Response({'message': 'Reservation deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


    def put(self, request, reservation_id):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to edit a reservation!'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            reservation = Reservation.objects.get(id=reservation_id)
            if request.user != reservation.user and not request.user.is_staff:
                return Response({'error': 'You do not have permission to edit this reservation.'}, status=status.HTTP_403_FORBIDDEN)
        except Reservation.DoesNotExist:
            return Response({'error': 'Reservation not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReservationSerializer(reservation, data=request.data, partial=True)
        if serializer.is_valid():
            max_participants = serializer.validated_data.get('max_participants', reservation.max_participants)
            current_participants = reservation.get_participant_count()
            if max_participants < current_participants:
                return Response({'error': 'New max participants cannot be less than current participants count!'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JoinReservationView(APIView):
    def post(self, request, reservation_id):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to join a reservation!'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            reservation = Reservation.objects.get(id=reservation_id)
        except Reservation.DoesNotExist:
            return Response({'error': 'Reservation not found!'}, status=status.HTTP_404_NOT_FOUND)

        if request.user in reservation.participants.all():
            return Response({'error': 'You are already a participant in this reservation!'}, status=status.HTTP_400_BAD_REQUEST)

        if reservation.user == request.user:
            return Response({'error': 'You cannot join your own reservation!'}, status=status.HTTP_400_BAD_REQUEST)

        if reservation.is_open and reservation.participants.count() < reservation.max_participants:
            reservation.participants.add(request.user)
            return Response({'message': 'You have successfully joined the reservation!'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'This reservation is closed or full!'}, status=status.HTTP_400_BAD_REQUEST)

class ParticipantReservationsView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to see reservations you joined!'}, status=status.HTTP_401_UNAUTHORIZED)

        reservations = Reservation.objects.filter(participants=request.user).exclude(user=request.user)

        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 


class AllReservationsView(APIView):
    def get(self,request):
        if not request.user.is_authenticated:
                return Response({'error': 'You must be logged in to see all reservations!'}, status=status.HTTP_401_UNAUTHORIZED)
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LeaveReservationView(APIView):
    def post(self, request, reservation_id):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to leave a reservation!'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            reservation = Reservation.objects.get(id=reservation_id)
        except Reservation.DoesNotExist:
            return Response({'error': 'Reservation not found!'}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in reservation.participants.all():
            return Response({'error': 'You are not a participant in this reservation!'}, status=status.HTTP_400_BAD_REQUEST)

        reservation.participants.remove(request.user)
        return Response({'message': 'You have successfully left the reservation!'}, status=status.HTTP_200_OK)

class ReservationParticipantView(APIView):
    def delete(self, request, reservation_id, user_id):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to remove a participant!'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            reservation = Reservation.objects.get(id=reservation_id, user=request.user)
        except Reservation.DoesNotExist:
            return Response({'error': 'Reservation not found or you do not have permission to remove a participant.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            user_to_remove = CustomUser.objects.get(id=user_id)  
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)

        if user_to_remove not in reservation.participants.all():
            return Response({'error': 'This user is not a participant in this reservation!'}, status=status.HTTP_400_BAD_REQUEST)

        reservation.participants.remove(user_to_remove)
        return Response({'message': 'User has been removed from the reservation successfully!'}, status=status.HTTP_200_OK)

class PostView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to create a post!'}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data.copy()
        data['user'] = request.user.id  

        reservation_id = data.get('reservationId', None)
        if reservation_id:
            try:
                reservation = Reservation.objects.get(id=reservation_id)
                data['reservation'] = reservation
                print(f"Assigned reservation with ID {reservation_id} to post.")
            except Reservation.DoesNotExist:
                print(f"Reservation with ID {reservation_id} does not exist.")
                return Response({'error': 'Reservation not found'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save(user=request.user)  
            if reservation_id:
                post.reservation = reservation
                post.save()  
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


    def delete(self, request, post_id):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to delete a post!'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            post = Post.objects.get(id=post_id)
            if request.user == post.user or request.user.is_superuser:
                post.delete()
                return Response({'message': 'Post deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'You do not have permission to delete this post.'}, status=status.HTTP_403_FORBIDDEN)
        
        except Post.DoesNotExist:
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, post_id):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to edit a post!'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            post = Post.objects.get(id=post_id)
            if request.user != post.user and not request.user.is_superuser:
                return Response({'error': 'You do not have permission to edit this post.'}, status=status.HTTP_403_FORBIDDEN)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        reservation_id = data.get('reservationId', None)

        if reservation_id:
            try:
                reservation = Reservation.objects.get(id=reservation_id)
                data['reservation'] = reservation.id
            except Reservation.DoesNotExist:
                return Response({'error': 'Reservation not found.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PostSerializer(post, data=data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllPostView(APIView):
    def get(self,request):
        if not request.user.is_authenticated:
                return Response({'error': 'You must be logged in to see all posts!'}, status=status.HTTP_401_UNAUTHORIZED)
        posts = Post.objects.all()
        print("Posts from DB:", posts)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CommentView(APIView):
    def post(self, request, post_id):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to add a comment!'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found!'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['user'] = request.user.id  
        data['post'] = post.id  

        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, post_id=None, comment_id=None):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to view comments!'}, status=status.HTTP_401_UNAUTHORIZED)
        if comment_id is not None:
            try:
                comment = Comment.objects.get(id=comment_id) # get_object_or_404
                serializer = CommentSerializer(comment)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Comment.DoesNotExist:
                return Response({'error': 'Comment not found!'}, status=status.HTTP_404_NOT_FOUND)

        if post_id is not None:
            try:
                post = Post.objects.get(id=post_id)
                comments = Comment.objects.filter(post=post)
                serializer = CommentSerializer(comments, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Post.DoesNotExist:
                return Response({'error': 'Post not found!'}, status=status.HTTP_404_NOT_FOUND)


        def delete(self, request, comment_id):
            if not request.user.is_authenticated:
                return Response({'error': 'You must be logged in to delete a comment!'}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                comment = Comment.objects.get(id=comment_id)
            except Comment.DoesNotExist:
                return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

            if request.user.is_superuser or request.user == comment.user:
                comment.delete()
                return Response({'message': 'Comment deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'You do not have permission to delete this comment.'}, status=status.HTTP_403_FORBIDDEN)
    
    
class AllCommentView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to view all comments!'}, status=status.HTTP_401_UNAUTHORIZED)

        comments = Comment.objects.all() 
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
