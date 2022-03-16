import os
from traceback import print_tb
import jwt
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.urls import reverse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import (GenericAPIView, ListAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, ConfirmCode
from .serializers import (EmailVerificationSerializer, LogoutSerializer,
                          ResetPasswordEmailRequestSerializer,
                          SetNewPasswordSerializer, UserLoginSerializer,
                          UserRegistrationSerializer, UserSerializer,
                          UserRegisterRequestSerializer)

from.renderer import UserJSONRenderer
from django.contrib.auth import login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponsePermanentRedirect
from django.utils.encoding import (DjangoUnicodeDecodeError, force_str,
                                   smart_bytes, smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .utils import Util

from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
from rest_framework.parsers import FileUploadParser 
from rest_framework.parsers import FormParser, MultiPartParser

class UserRegistrationView(GenericAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            code = ConfirmCode.objects.create(user=user)
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)
            login(request, user)
            Util.send_code_to_email(user, code.code)

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data,
                'access_token': access_token,
                'refresh_token': refresh_token
            }

            return Response(response, status=status_code)

class VerifyEmail(APIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer,)

    def get(self, request, code):

        try:
            if ConfirmCode.objects.filter(code=code):
                token = request.headers['Authorization'].split(' ').pop()
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')         
                user = User.objects.get(id=payload['user_id'])
                code = ConfirmCode.objects.get(code=code, user=user)
                if not code.confirm:
                    code.confirm = True
                    code.user.is_verified = True
                    code.user.save()
                    code.save()
                    return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
                return Response({'email': 'Already activated'}, status=status.HTTP_200_OK)        
        
           
            return Response({'email': 'Code is outdated or incorrect'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            print(identifier)
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    


class ResendVerifyEmailView(GenericAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
            code = ConfirmCode.objects.create(user=user)
       
            if user.is_verified:
                return Response({'msg':'User is already verified'})
                        
            Util.send_code_to_email(user, code.code)
            return Response({'msg':'The verification email has been sent'}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'msg':'No such user, register first'})


class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'email': serializer.data['email'],
                    'role': serializer.data['role']
                }
            }

            return Response(response, status=status_code)

class LogoutView(GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserView(GenericAPIView):
    """
    Put access token into Authorize section at the top of the documentation
    """
    serializer_class = UserSerializer
    authenticated_class = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)

    def get(self, request):
        token = request.headers['Authorization'].split(' ').pop()

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')         
        user = User.objects.get(id=payload['user_id'])
        response = {
                'email': user.email,
                'role': user.get_role_display(),
            }
            
        return Response(response,)



class RequestPasswordResetEmail(GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_reset_email(data)
           
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)



class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']

class PasswordTokenCheckAPI(GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = (AllowAny, )

    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
    

class SetNewPasswordAPIView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = (AllowAny, )

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class SendRequestToRegisterAPIView(GenericAPIView):
    serializer_class = UserRegisterRequestSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser)
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        fio = request.data.get('fio', '')
        object_name = request.data.get('object_name', '')
        phone = request.data.get('phone', '')
        email = request.data.get('email', '')
        gos_register = request.FILES['gos_register']
        reshenie_o_sozd_yr_lisa = request.data.get('reshenie_o_sozd_yr_lisa', '')
        uchredit_dogovor = request.data.get('uchredit_dogovor', '')
        spravka_iz_nalogovoi = request.data.get('spravka_iz_nalogovoi', '')
        spravka_iz_sozfond = request.data.get('spravka_iz_sozfond', '')
        pasport = request.data.get('pasport', '')
        message = f'Заявка от юр. лица: {object_name}<br>'\
            f'ФИО заявителя: {fio}<br>'\
            f'Контактный номер: {phone}<br>'\
            f'Email: {email}<br>'\
            f'Свидетельво о гос. регистрации: {gos_register}<br>'\
            f'Решение о создании юр. лица: {reshenie_o_sozd_yr_lisa}<br>'\
            f'Учредительный договор: {uchredit_dogovor}<br>'\
            f'Справка с налоговой о неимении задолженности: {spravka_iz_nalogovoi}<br>'\
            f'Справка из соц. фонда о неимении задолженности: {spravka_iz_sozfond}<br>'\
            f'Копия паспорта директора: {pasport}'
        subject = 'Заявка на регистрацию'

        email = EmailMessage(subject, message, settings.EMAIL_HOST, [settings.EMAIL_HOST_USER])
        email.content_subtype = 'html'

        email.attach("Свидетельво о гос. регистрации", gos_register.read(), gos_register.content_type)
        email.attach("Решение о создании юр. лица", reshenie_o_sozd_yr_lisa.read(), reshenie_o_sozd_yr_lisa.content_type)
        email.attach("Учредительный договор", uchredit_dogovor.read(), uchredit_dogovor.content_type)
        email.attach("Справка с налоговой о неимении задолженности", spravka_iz_nalogovoi.read(), spravka_iz_nalogovoi.content_type)
        email.attach("Справка из соц. фонда о неимении задолженности", spravka_iz_sozfond.read(), spravka_iz_sozfond.content_type)
        email.attach("Копия паспорта директора", pasport.read(), pasport.content_type)

        email.send()
        return HttpResponse("Заявка была отправлена")


class SendRequestToRegisterHotelAPIView(GenericAPIView):
    serializer_class = UserRegisterRequestSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser)
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        fio = request.data.get('fio', '')
        object_name = request.data.get('object_name', '')
        phone = request.data.get('phone', '')
        email = request.data.get('email', '')
        gos_register = request.FILES['gos_register']
        reshenie_o_sozd_yr_lisa = request.data.get('reshenie_o_sozd_yr_lisa', '')
        uchredit_dogovor = request.data.get('uchredit_dogovor', '')
        spravka_iz_nalogovoi = request.data.get('spravka_iz_nalogovoi', '')
        spravka_iz_sozfond = request.data.get('spravka_iz_sozfond', '')
        pasport = request.data.get('pasport', '')
        message = f'Заявка от юр. лица: {object_name}<br>'\
            f'ФИО заявителя: {fio}<br>'\
            f'Контактный номер: {phone}<br>'\
            f'Email: {email}<br>'\
            f'Свидетельво о гос. регистрации: {gos_register}<br>'\
            f'Решение о создании юр. лица: {reshenie_o_sozd_yr_lisa}<br>'\
            f'Учредительный договор: {uchredit_dogovor}<br>'\
            f'Справка с налоговой о неимении задолженности: {spravka_iz_nalogovoi}<br>'\
            f'Справка из соц. фонда о неимении задолженности: {spravka_iz_sozfond}<br>'\
            f'Копия паспорта директора: {pasport}'
        subject = 'Заявка на регистрацию'

        email = EmailMessage(subject, message, settings.EMAIL_HOST, [settings.EMAIL_HOST_USER])
        email.content_subtype = 'html'

        email.attach("Свидетельво о гос. регистрации", gos_register.read(), gos_register.content_type)
        email.attach("Решение о создании юр. лица", reshenie_o_sozd_yr_lisa.read(), reshenie_o_sozd_yr_lisa.content_type)
        email.attach("Учредительный договор", uchredit_dogovor.read(), uchredit_dogovor.content_type)
        email.attach("Справка с налоговой о неимении задолженности", spravka_iz_nalogovoi.read(), spravka_iz_nalogovoi.content_type)
        email.attach("Справка из соц. фонда о неимении задолженности", spravka_iz_sozfond.read(), spravka_iz_sozfond.content_type)
        email.attach("Копия паспорта директора", pasport.read(), pasport.content_type)

        email.send()
        return HttpResponse("Заявка была отправлена")