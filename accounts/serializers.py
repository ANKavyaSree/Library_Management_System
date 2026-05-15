from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True
    )
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'role',
            'password'
        ]
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role'],
            password=validated_data['password']
        )
        return user
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True
    )
    role = serializers.CharField()
    def validate(self, data):
        user = authenticate(
            username=data['username'],
            password=data['password']
        )
        if not user:
            raise serializers.ValidationError(
                "Invalid username or password"
            )
        if user.role != data['role']:
            raise serializers.ValidationError(
                "Selected role is incorrect"
            )
        data['user'] = user
        return data