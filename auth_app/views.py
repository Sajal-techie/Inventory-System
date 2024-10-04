import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializer import LoginSerializer, RegisterSerializer


logger = logging.getLogger(__name__)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            logger.info("user registration attempt")
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info("User registered successfully: %s", serializer.data['username'])
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            logger.warning("Registration failed with errors: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Error during registration: %s", str(e))
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            logger.info("User login attempt")
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data
                print(user)
                refresh = RefreshToken.for_user(user)
                logger.info("User logged in successfully: %s", user.username)

                return Response({
                    'access': str(refresh.access_token)
                }, status=status.HTTP_200_OK)
            
            logger.warning("Login failed with errors: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Error during login: %s", str(e))
            return Response({str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    