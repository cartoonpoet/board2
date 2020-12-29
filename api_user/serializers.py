from rest_framework import serializers
from django.contrib.auth import authenticate
from . import models
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

