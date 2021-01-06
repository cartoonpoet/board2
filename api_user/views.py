from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from knox.models import AuthToken
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserSerializer, LoginSerializer, UserGroupSerializer
from .models import User, Group, User_Group


# Create your views here.
# https://d-yong.tistory.com/61?category=751110
class UserView(APIView):
    # 모든 또는 특정 ID 정보 불러오기
    def get(self, request, **kwargs):
        if kwargs.get('user_id') is None:
            user_queryset = User.objects.all()  # 모든 User의 정보를 불러온다.
            user_queryset_serializer = UserSerializer(user_queryset, many=True)
            return Response(user_queryset_serializer.data, status=status.HTTP_200_OK)
        else:
            user_id = kwargs.get('user_id')
            user_serializer = UserSerializer(User.objects.get(id=user_id))  # id에 해당하는 User의 정보를 불러온다
            return Response(user_serializer.data, status=status.HTTP_200_OK)

    # 회원가입
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)  # Request의 data를 UserSerializer로 변환

        if user_serializer.is_valid():
            user_serializer.save()  # UserSerializer의 유효성 검사를 한 뒤 DB에 저장
            usergroup = {'user_id': request.data['id'], 'group_id': request.data['group']}
            usergroup_serializer = UserGroupSerializer(data=usergroup)

            if usergroup_serializer.is_valid():
                usergroup_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_201_CREATED)  # client에게 JSON response 전달
        else:
            return Response({None}, status=status.HTTP_200_OK)

    # 회원정보 수정
    def patch(self, request, **kwargs):
        if kwargs.get('user_id') is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            user_id = kwargs.get('user_id')
            user_object = User.objects.get(id=user_id)

            update_user_serializer = UserSerializer(user_object, data=request.data)
            if update_user_serializer.is_valid():
                update_user_serializer.save()
                return Response(update_user_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)

    # 회원탈퇴
    def delete(self, request, **kwargs):
        if kwargs.get('user_id') is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            user_id = kwargs.get('user_id')
            user_object = User.objects.get(id=user_id)
            user_object.delete()
            return Response("delete ok", status=status.HTTP_200_OK)


# 로그인은 아래 정보 참조
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    # 로그인
    def post(self, request):
        # ID/PW 확인
        if authenticate(id=request.data['id'], password=request.data['password']) is None:
            return Response({
                'user': 'none',
                'token': 'none'
            }, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        if user is not None:
            login(request, user)
            print(request.user)
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data, "token": AuthToken.objects.create(user)[1]
            }, status=status.HTTP_200_OK)

    # 로그아웃
    def delete(self, request):
        if request.data.get('user_token') is not None:
            logout(request)
            return Response({'message': 'logout complete'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'invalid request'}, status=status.HTTP_200_OK)


class GroupView(APIView):
    def post(self, request):
        if request.data.get('group') is not None:
            data = Group.objects.create(id=request.data.get('group'))
            return Response({'message': 'group created'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'invalid request'}, status=status.HTTP_200_OK)