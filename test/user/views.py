from django.contrib import auth
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import  Response
from rest_framework_simplejwt.tokens import RefreshToken

from test.user.models import User, PersonalDetails
from test.user.serializers import RegisterSerializer, LoginSerializer, PersonaldetailSerializer


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):

        user = request.data
        serializer  = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user_obj = auth.authenticate(email=user["email"], password=request.data['password'])
        user = User.objects.get(email=user["email"])
        token = RefreshToken.for_user(user).access_token
        user_data['access_token'] = str(token)
        data = {}
        data['email'] = user.email
        data["user_id"] = user.user_id
        data['access_token'] = user_data.get('access_token')
        return Response(data, status = status.HTTP_200_OK)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PersonaldetailsView(generics.GenericAPIView):
    # authentication_classes =
    permission_classes = [IsAuthenticated]
    serializer_class = PersonaldetailSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        validated_data = serializer.validated_data
        # validated_data['user_id'] = request.user
        print(validated_data)
        #chec if pi aready there for this user

        data['user_id'] = request.user

        personal_info = PersonalDetails.objects.create(**data)
        return  Response({"success":'saved successfully'}, status.HTTP_200_OK)



