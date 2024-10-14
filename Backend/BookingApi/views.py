from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ReservationSerializer
from .models import Reservation
# Create your views here.


class ReservationView(APIView):

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to create a reservation!'}, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = ReservationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to see your reservations!'}, status=status.HTTP_401_UNAUTHORIZED)
        
        reservations = Reservation.objects.filter(user=request.user)
        serializer = ReservationSerializer(reservations, many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK)