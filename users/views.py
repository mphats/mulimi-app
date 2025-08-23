from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from .serializers import RegisterSerializer, MeSerializer

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    # new users inactive until verify
    user.is_active = False
    user.save()
    _send_verification_email(user, request)
    return Response({"detail": "registered; verification email sent"}, status=status.HTTP_201_CREATED)

def _send_verification_email(user: User, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    verify_url = f"{settings.FRONTEND_BASE_URL}/verify-email?uid={uid}&token={token}"
    alt = f"/api/v1/auth/verify-email?uid={uid}&token={token}"
    send_mail(
        subject="Verify your account",
        message=f"Hi {user.username}, verify your account: {verify_url}\nAlternatively (API): {alt}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email] if user.email else [],
        fail_silently=True,
    )

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(MeSerializer(request.user).data)

@api_view(["POST"])
@permission_classes([AllowAny])
def request_email_verification(request):
    email = request.data.get("email")
    try:
        user = User.objects.get(email=email)
        if user.is_active:
            return Response({"detail": "already verified"}, status=200)
        _send_verification_email(user, request)
    except User.DoesNotExist:
        pass  # don't leak existence
    return Response({"detail": "if the account exists, an email was sent"}, status=200)

@api_view(["POST"])
@permission_classes([AllowAny])
def verify_email(request):
    uidb64 = request.data.get("uid") or request.query_params.get("uid")
    token = request.data.get("token") or request.query_params.get("token")
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        return Response({"detail": "invalid uid"}, status=400)
    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({"detail": "verified"})
    return Response({"detail": "invalid token"}, status=400)

@api_view(["POST"])
@permission_classes([AllowAny])
def password_reset(request):
    email = request.data.get("email")
    try:
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = f"{settings.FRONTEND_BASE_URL}/reset-password?uid={uid}&token={token}"
        send_mail(
            subject="Password reset",
            message=f"Reset your password: {reset_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
    except User.DoesNotExist:
        pass
    return Response({"detail": "if the account exists, an email was sent"}, status=200)

@api_view(["POST"])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    uidb64 = request.data.get("uid")
    token = request.data.get("token")
    new_password = request.data.get("new_password")
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        return Response({"detail": "invalid uid"}, status=400)
    if not default_token_generator.check_token(user, token):
        return Response({"detail": "invalid token"}, status=400)
    user.set_password(new_password)
    user.save()
    return Response({"detail": "password updated"})



from django.utils import timezone
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from .models import MagicLink
import datetime

@api_view(['POST'])
@permission_classes([AllowAny])
def magic_link_request(request):
    email = request.data.get('email')
    if not email:
        return Response({'detail': 'email required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # don't leak existence
        return Response({'detail': 'if the account exists, a link was sent'}, status=status.HTTP_200_OK)

    expires = timezone.now() + datetime.timedelta(minutes=15)
    ml = MagicLink.objects.create(user=user, expires_at=expires)
    magic_link = f"{settings.FRONTEND_BASE_URL}/magic-login?token={ml.token}"
    # render template
    text = render_to_string('emails/magic_link.txt', {'user': user, 'magic_link': magic_link})
    html = render_to_string('emails/magic_link.html', {'user': user, 'magic_link': magic_link})
    send_mail('Your magic sign-in link', text, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=html, fail_silently=True)
    return Response({'detail': 'if the account exists, a link was sent'}, status=status.HTTP_200_OK)

@api_view(['POST','GET'])
@permission_classes([AllowAny])
def magic_link_verify(request):
    token = request.data.get('token') or request.query_params.get('token')
    if not token:
        return Response({'detail': 'token required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        ml = get_object_or_404(MagicLink, token=token)
    except Exception:
        return Response({'detail': 'invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    if ml.used or ml.is_expired():
        return Response({'detail': 'token invalid or expired'}, status=status.HTTP_400_BAD_REQUEST)
    user = ml.user
    user.is_active = True
    user.save()
    ml.mark_used()
    refresh = RefreshToken.for_user(user)
    return Response({'access': str(refresh.access_token), 'refresh': str(refresh)}, status=status.HTTP_200_OK)
