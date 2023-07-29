import base64
import re
from datetime import datetime

import pyotp
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.core.mail import send_mail
from config.settings import  base
# Create your views here.
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import  Response
from rest_framework_simplejwt.tokens import RefreshToken
from test.utils.customotp import TOTPVerification

from test.user.models import User, PersonalDetails, CustomOtp
from test.user.serializers import RegisterSerializer, LoginSerializer, PersonaldetailSerializer, CustomoptSerializer, VerifyOTPSerializer


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
        send_mail(
            'Subject here',
            'Here is the message.',
            base.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
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



class GenerateotpView(generics.GenericAPIView):
    serializer_class =CustomoptSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        key = pyotp.random_base32() # Key is generated
        otp = pyotp.totp.TOTP(key, interval=10)
        print(otp.generate_otp(1))

        data = dict()
        data['user_id_id'] = request.user.user_id
        data['token'] = key
        data['email'] = request.user.email

        send_mail(
            'Your Verification OTP',
            F'YOUR OTP IS {otp.generate_otp(1)}.',
            base.EMAIL_HOST_USER,
            [data['email']],
            fail_silently=False,
        )

        CustomOtp.objects.create(**data)

        return  Response({"status":" token created successfully"},  status.HTTP_200_OK)





class VerifyOTP(generics.GenericAPIView):
    serializer_class = VerifyOTPSerializer
    permission_classes =[IsAuthenticated]

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_otp_input = request.data['otp']
        get_token = CustomOtp.objects.filter(email =request.user.email).order_by('-created_at').first()
        key = get_token.token
        otp  = pyotp.TOTP(key, interval=10)
        validating_otp = otp.generate_otp(1)
        print(validating_otp)
        if user_otp_input == validating_otp :  # Verifying the OTP
            get_token.isVerified = True
            get_token.save()
            return Response("You are authorised", status=200)
        else:
            return Response("wrong OTP")



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



