from rest_framework import serializers
from django.contrib.auth import authenticate
from . import models
from .models import Board, BoardFile
from api_user.serializers import UserSerializer, UserGroupSerializer


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardFile
        fields = '__all__'


class BoardJoinSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Board
        fields = '__all__'