from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view,permission_classes
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated,AllowAny



# FORGET PASSWORD

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str



class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access = response.data["access"]
            refresh = response.data["refresh"]
            
            response.set_cookie(
                key="access",
                value=access,
                httponly=True,
                secure=False,      
                samesite="Lax",
                max_age=60 * 15,
            )

            response.set_cookie(
                key="refresh",
                value=refresh,
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=60 * 60 * 24 * 7,
            )

            # Optional: don't expose the tokens in the JSON body
            del response.data["access"]
            del response.data["refresh"]

        return response

@api_view(['POST'])
def LogoutView(request):
    response = Response({
        'info':'Logged Out successfully.'
    },status=200)

    response.delete_cookie('access')
    response.delete_cookie('refresh')
    return response

class TaskViewSet(ModelViewSet):
    
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self,serializer):
        serializer.save(
            user=self.request.user
        )
    def get_queryset(self):
        return Task.objects.filter(
            user=self.request.user
        )
    



@api_view(['POST'])
def registerView(request):

    serializer = RegisterSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response({'info':'User Registered Sucessfully!'},status=201)


    
@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset(request):
    email = request.data.get('email')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({
            'message':'If the email exists, a reset link has been sent.'
        },status=200)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    print(uid)
    print(token)
    reset_link = (
        f'http://localhost:3000/reset-password/{uid}/{token}'
    )
    send_mail(
        subject="RESET YOUR PASSWORD",
        message=f"Click the link below:\n\n{reset_link}",
        from_email=None,
        recipient_list=[user.email],
    )

    return Response({
        'message':'Password reset email sent.'
    },status=200)



@api_view(["POST"])
@permission_classes([AllowAny])
def password_reset_confirm(request):

    uid = request.data.get("uid")
    token = request.data.get("token")
    password = request.data.get("password")

    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
    except Exception:
        return Response(
            {"error": "Invalid reset link."},
            status=400
        )

    if not default_token_generator.check_token(user, token):
        return Response(
            {"error": "Invalid or expired token."},
            status=400
        )

    user.set_password(password)
    user.save()

    return Response(
        {"message": "Password changed successfully."},
        status=200
    )