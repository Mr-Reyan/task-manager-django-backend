from .models import *
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

User = get_user_model()

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']
        extra_kwargs = {
            "password": {"write_only": True}
        }
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)





class LoginSerializer(TokenObtainPairSerializer):
    username_field = "username"

    username = serializers.EmailField()

    def validate(self, attrs):
        username = attrs.get("username")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials.")

        attrs["email"] = user.email

        return super().validate(attrs)