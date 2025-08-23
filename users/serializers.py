from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=Profile.Role.choices, default=Profile.Role.FARMER)

    class Meta:
        model = User
        fields = ("username", "email", "password", "role")

    def create(self, validated_data):
        role = validated_data.pop("role", Profile.Role.FARMER)
        user = User.objects.create_user(**validated_data)
        user.profile.role = role
        user.profile.save()
        return user

class MeSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="profile.role", read_only=True)
    class Meta:
        model = User
        fields = ("id", "username", "email", "role")
