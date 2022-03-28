from django.urls import path, re_path
from rest_framework_simplejwt import views as jwt_views

from .views import (
    UserRegistrationView,
    UserLoginView,
    LogoutView,
    UserView,
    VerifyEmail,
    ResendVerifyEmailView,
    RequestPasswordResetEmail,
    PasswordTokenCheckAPI,
    SetNewPasswordAPIView,
    SendRequestToRegisterAPIView
)

urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('email-verify/<code>/', VerifyEmail.as_view(), name="email-verify"),
    path('resend-email-verify/', ResendVerifyEmailView.as_view(), name='resend-email-verify'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'), 
    path('user/', UserView.as_view(), name='user'),
    path('request-reset-password-by-email/', RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    re_path(r'^password-reset/(?uidb=<uidb64>&token=<token>)$/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
    path('request-to-register/', SendRequestToRegisterAPIView.as_view(), name='request-to-register'),
]