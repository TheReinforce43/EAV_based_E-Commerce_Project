from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status 

from rest_framework.generics import CreateAPIView , UpdateAPIView, RetrieveDestroyAPIView


from ecommerce_project.user.Serializer.user_serializer import (
    UserLoginSerializer,
    UserSignUpSerializer,
    LogoutSerializer
)

from rest_framework.permissions import AllowAny



class UserSignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
    


class UserLoginView(APIView):

    permission_classes=[AllowAny]
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Logged out successfully."}, status=status.HTTP_204_NO_CONTENT)