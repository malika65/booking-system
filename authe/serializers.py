from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (DjangoUnicodeDecodeError, force_str,
                                   smart_bytes, smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User
from rest_framework.fields import ChoiceField



class UserRegistrationSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = User
        fields = (
            'email',
            'password'
        )
        # this field does not be in response
        extra_kwargs = {
            'password': {'write_only':True}
        }

    def create(self, validated_data):
        auth_user = User.objects.create_user(**validated_data)
        return auth_user



class EmailVerificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password']


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
                'role': user.role,
            }

            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    role = serializers.CharField(min_length=1)
    token = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['email', 'role', 'token']


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


class UserRegisterRequestSerializer(serializers.Serializer):
    fio = serializers.CharField(max_length=120)
    object_name = serializers.CharField(max_length=120)
    phone = serializers.CharField(max_length=120)
    email = serializers.EmailField()
    gos_register = serializers.FileField(max_length=200, allow_empty_file=False, write_only=True)
    reshenie_o_sozd_yr_lisa = serializers.FileField(max_length=200, allow_empty_file=False, write_only=True)
    uchredit_dogovor = serializers.FileField(max_length=200, allow_empty_file=False, write_only=True)
    spravka_iz_nalogovoi = serializers.FileField(max_length=200, allow_empty_file=False, write_only=True)
    spravka_iz_sozfond = serializers.FileField(max_length=200, allow_empty_file=False, write_only=True)
    pasport = serializers.FileField(max_length=200, allow_empty_file=False, write_only=True)

    class Meta:
        fields = ['fio', 'object_name', 
        'phone', 'email', 'gos_register', 
        'reshenie_o_sozd_yr_lisa', 'uchredit_dogovor',
        'spravka_iz_nalogovoi', 'spravka_iz_sozfond',
        'pasport']


