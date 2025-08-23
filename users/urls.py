from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView
)
from . import views

urlpatterns = [
    path('magic-link-request', views.magic_link_request, name='magic_link_request'),
    path('magic-link-verify', views.magic_link_verify, name='magic_link_verify'),
    path("register", views.register, name="register"),
    path("me", views.me, name="me"),
    path("request-email-verification", views.request_email_verification, name="request_email_verification"),
    path("verify-email", views.verify_email, name="verify_email"),
    path("password-reset", views.password_reset, name="password_reset"),
    path("password-reset-confirm", views.password_reset_confirm, name="password_reset_confirm"),
    path("token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify", TokenVerifyView.as_view(), name="token_verify"),
    path("token/blacklist", TokenBlacklistView.as_view(), name="token_blacklist"),
]