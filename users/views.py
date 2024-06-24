from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from .models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny

import jwt, datetime

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found")    # 404
        
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")
        
        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, "secret",algorithm="HS256")

        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)

        response.data = {
            "jwt": token
        }
        return response
        # return Response({
        #     "message": "Login successful",
        #     "token": token})
    

class UserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated")
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unathenticated")
        
        user = User.objects.filter(id=payload["id"]).first()

        serializer = UserSerializer(user)

        return Response(serializer.data)
    

class LogoutView(APIView):
        permission_classes = [AllowAny]
        
        def post(self, request):
            response = Response()
            response.delete_cookie("jwt")
            response.data = {
                "message":"success"
            }
        
            return response