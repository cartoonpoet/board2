from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BoardSerializer, FileSerializer, BoardJoinSerializer
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework import generics, permissions
from .models import BoardFile, Board


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
            board_queryset = Board.objects.filter(id=kwargs.get('post_num'))
            board_serializer = BoardJoinSerializer(board_queryset, many=True)
            file_queryset = BoardFile.objects.filter(num_id=kwargs.get('post_num'))
            file_serializer = FileSerializer(file_queryset, many=True)
            print(board_serializer.data)
            return Response({'basic_info': board_serializer.data, 'file_info': file_serializer.data}, status=status.HTTP_200_OK)

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