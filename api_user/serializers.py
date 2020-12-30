from rest_framework import serializers
from django.contrib.auth import authenticate
from . import models
from .models import User, User_Group, Group


class UserSerializer(serializers.ModelSerializer):
    # 오버라이딩, 그냥 save하니까 계정 패스워드 암호화가 안됨.
    def save(self, **kwargs):
        User.objects.create_user(id=self.data['id'], name=self.data['name'], password=self.data['password'])
        print(self.data)

    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    id = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

