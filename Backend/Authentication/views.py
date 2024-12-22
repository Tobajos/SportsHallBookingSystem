from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class RegisterUser(APIView):
    permission_classes = ()
    
    def post(self, request, format=None):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Account created successfully!'}, status=status.HTTP_201_CREATED)
        
        errors = serializer.errors
        error_messages = []
        for field, messages in errors.items():
            for message in messages:
                error_messages.append(f"{field}: {message}")
        
        return Response({'errors': error_messages}, status=status.HTTP_400_BAD_REQUEST)

      
class Login(APIView):
    permission_classes = ()

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None:
            return Response({'error': 'You must provide both email and password!'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)

        if not user:
            return Response({'error': 'Invalid email or password!'}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'Logged in successfully!',
            'token': token.key,
            'user_id': user.id,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'email': user.email
        }, status=status.HTTP_200_OK)



class Logout(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        token = get_object_or_404(Token,user=request.user)
        token.delete()
        logout(request)
        return Response({'message':'Logged out succesfully!'},status=status.HTTP_200_OK)

    
    
    
