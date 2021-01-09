from typing import Optional

from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'address', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def update(self, instance, validated_data) -> User:
        password: Optional[str] = validated_data.pop('password', None)
        user: User = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'},
        min_length=5, max_length=255
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data) -> User:
        password: Optional[str] = validated_data.pop('password')
        instance: User = User(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
