# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BoardSerializer, FileSerializer, BoardJoinSerializer, UserJoinSerializer
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework import generics, permissions
from .models import BoardFile, Board
from api_user.models import User, User_Group, Group
from django.db.models import F


# Create your views here.
class BoardView(APIView):
    def get(self, request, **kwargs):
        # 모든 게시글 조회
        if kwargs.get('post_num') is None:
            print('모든 게시물 조회')
            board_queryset = Board.objects.all().order_by('-id')
            board_serializer = BoardSerializer(board_queryset, many=True)
            return Response(board_serializer.data, status=status.HTTP_200_OK)
        # 단일 게시글 조회
        else:
            print('단일 게시물 조회')

            # 글 정보
            board_queryset = Board.objects.filter(id=kwargs.get('post_num'))
            board_serializer = BoardJoinSerializer(board_queryset, many=True)
            file_queryset = BoardFile.objects.filter(num_id=kwargs.get('post_num'))
            file_serializer = FileSerializer(file_queryset, many=True)
            #print(file_serializer.data)
            #print(board_serializer.data)

            # 글 작성자에 대한 정보
            writer_queryset = User_Group.objects.filter(user_id=board_queryset[0].user_id)
            writerjoin = UserJoinSerializer(writer_queryset, many=True)
            #print(writerjoin.data)
            
            # 조회자에 대한 정보
            viewer_id = request.GET['viewer']
            viewer_queryset = User_Group.objects.filter(user_id=viewer_id)
            viewerjoin = UserJoinSerializer(viewer_queryset, many=True)
            #print(viewerjoin.data)

            # 이전글/다음글에 대한 정보
            next = Board.objects.filter(id__gt=kwargs.get('post_num')).first()
            prev = Board.objects.filter(id__lt=kwargs.get('post_num')).last()
            next_serializer = BoardSerializer(next)
            prev_serializer = BoardSerializer(prev)

            return Response({'basic_info': board_serializer.data, 'file_info': file_serializer.data, 'writer_info': writerjoin.data, 'viewer_info': viewerjoin.data, 'next_post': next_serializer.data, 'prev_post': prev_serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        print('게시물 작성')
        board_serializer = BoardSerializer(data=request.data)
        # 게시물 저장
        if board_serializer.is_valid():
            board_serializer.save()

            # 파일 저장
            for file in request.FILES.getlist('file'):
                file_data = {'file': file, 'num': board_serializer.data['id']}
                file_serializer = FileSerializer(data=file_data)
                if file_serializer.is_valid():
                    file_serializer.save()

            return Response(board_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(None, status=status.HTTP_200_OK)

    def delete(self, request, **kwargs):
        print(kwargs.get('post_num'))
        if kwargs.get('post_num') is not None:
            deletable_data = Board.objects.filter(id=kwargs.get('post_num'))
            deletable_data.delete()
            return Response({'message': 'Deleted'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid Request'}, status=status.HTTP_200_OK)
