import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser

from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, email, user_id=None, password=None, promo_code=None):
        if user_id is None:
            user_id = uuid.uuid4().hex
        if email is None:
            raise TypeError("Users should have a Email")
        if promo_code:
            user = self.model(user_id=user_id, email=self.normalize_email(email), promo_code=promo_code)
        else:
            user = self.model(user_id=user_id, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        id = uuid.uuid4().hex
        if password is None:
            raise TypeError("Users should have a Password")

        user = self.create_user(user_id=id, email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    user_id = models.UUIDField(
        primary_key=True, db_index=True, unique=True, default=uuid.uuid4
    )
    email = models.EmailField(max_length=255, unique=True, db_index=True,
                              error_messages={'unique': "Alrady rregistred with us."})
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def access_tokens(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh.access_token)

    def refresh_tokens(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh)


class PersonalDetails(models.Model):
    pd_id= models.UUIDField(primary_key=True, db_index=True, unique=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=256, null=True, blank=True)
    last_name = models.CharField(max_length=256, null=True, blank=True)
    dob = models.DateTimeField(null=True, blank=True)
    phone_number = models.CharField(max_length=256, null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

