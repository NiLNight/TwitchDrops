from rest_framework import serializers
from django.contrib.auth.models import User
from mainapp.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Passwords do not match')
        return data


class ProfileSerializer(serializers.ModelSerializer):
    auth_user = UserSerializer(source='user')

    class Meta:
        model = UserProfile
        fields = ['auth_user', 'id', 'user', 'phone', 'birth_date', 'avatar']
