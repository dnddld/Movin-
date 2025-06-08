from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import ProfileSerializer, ProfileUpdateSerializer, MyProfileSerializer


@api_view(['GET'])
def user_profile(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    serializer = ProfileSerializer(user)
    return Response(serializer.data)


# 팔로우 / 언팔로우 토글 (로그인 사용자만)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, user_pk):
    me = request.user
    you = get_object_or_404(User, pk=user_pk)
    if me != you:
        if you in me.followings.all():
            me.followings.remove(you)  # 언팔로우
        else:
            me.followings.add(you)  # 팔로우
    serializer = ProfileSerializer(you)
    return Response(serializer.data)


# 프로필 사진 수정 (본인만 가능)
@api_view(['POST','PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    if request.user != user:
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    # 잘못된 부분: files=request.FILES 제거
    serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        # 비밀번호 변경 처리
        password = request.data.get('password')
        if password:
            user.set_password(password)
            user.save()
        return Response(serializer.data)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    serializer = MyProfileSerializer(request.user)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    if request.user != user:
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    user.delete()
    return Response({'detail': '회원 탈퇴가 완료되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
