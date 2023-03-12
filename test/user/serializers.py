from django.contrib import auth
from rest_framework import  serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from test.user.models import  User, PersonalDetails


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    # phone_number = serializers.CharField(max_length=15, min_length=10, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password",]

    def validate(self, attrs):
        email = attrs.get("email", "")

        if email == "":
            raise serializers.ValidationError("El correo electrónico está vacío")

        try:
            User.objects.get(email=email.strip().lower())
            raise serializers.ValidationError("el Email ya existe")
        except User.DoesNotExist:
            return attrs

    def create(self, validated_data):

        user_obj = User.objects.create_user(email=validated_data['email'].lower(),
                                                password=validated_data['password'])
        return user_obj



class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=55,trim_whitespace=False)
    password = serializers.CharField(max_length=68,trim_whitespace=False, write_only=True)
    user_id = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = [
            "user_id",
            "password",
            "email",
            "access_token",
            "refresh_token"
        ]

    def validate(self, validated_data):
        email = validated_data.get("email", "").lower()
        password = validated_data.get("password", "")
        try:
            obj = User.objects.get(email=email)
        except Exception:
            raise AuthenticationFailed("Cuenta no encontrada")
        user = auth.authenticate(email=email, password=password)
        if type(user) is None:
            raise AuthenticationFailed("Credenciales no válidas")
        if not user:
            raise AuthenticationFailed("Credenciales no válidas")
        return {
            "email": user.email,
            "user_id": user.user_id,
            "access_token": user.access_tokens,
            "refresh_token": user.refresh_tokens,
        }


class PersonaldetailSerializer(serializers.ModelSerializer):
    # pd_id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=256, allow_blank=False, allow_null=False)
    last_name = serializers.CharField(max_length=256,allow_blank=False, allow_null=False )
    dob = serializers.DateTimeField(allow_null=False)
    phone_number = serializers.CharField(max_length=256,allow_blank=False, allow_null=False )

    class Meta:
        model= PersonalDetails
        fields = [ "first_name", "last_name", "dob", "phone_number"  ]

    def validat(self, attrs):
        # piobj = PersonalDetails.objects.get(user_id=data['user_id'])
        # if piobj:
        #new comment
        pass



