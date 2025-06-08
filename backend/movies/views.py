from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Movie, Article, Comment
from .serializers import (
    MovieListSerializer, MovieDetailSerializer,
    ArticleSerializer, CommentSerializer
)
from .serializers_movie import MovieSimpleSerializer

@api_view(['GET'])
def simple_movies(request):
    movies = Movie.objects.all()
    serializer = MovieSimpleSerializer(movies, many=True)
    return Response(serializer.data)

# 영화 전체 목록
@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


# 영화 상세 정보
@api_view(['GET'])
def movie_detail(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    serializer = MovieDetailSerializer(movie, context={'request': request})
    return Response(serializer.data)


# 영화 북마크 토글 (찜)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_bookmark(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    user = request.user
    if user in movie.bookmark_users.all():
        movie.bookmark_users.remove(user)
    else:
        movie.bookmark_users.add(user)
    return Response({'status': 'ok'})


# 리뷰 목록 조회 & 작성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list_or_create(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == 'GET':
        articles = movie.articles.all().order_by('-created_at')
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 리뷰 상세조회 / 수정 / 삭제 / 좋아요
@api_view(['GET', 'PUT', 'DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def article_detail(request, movie_id, article_id):
    article = get_object_or_404(Article, pk=article_id, movie__id=movie_id)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if request.user != article.user:
            return Response({'detail': '수정 권한 없음'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if request.user != article.user:
            return Response({'detail': '삭제 권한 없음'}, status=status.HTTP_403_FORBIDDEN)
        article.delete()
        return Response({'status': 'deleted'})

    elif request.method == 'POST':
        # 좋아요 토글
        user = request.user
        if user in article.like_users.all():
            article.like_users.remove(user)
        else:
            article.like_users.add(user)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)


# 전체 리뷰 목록 (모든 영화 통합)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_reviews(request):
    sort = request.GET.get('sort', 'latest')
    if sort == 'likes':
        articles = Article.objects.all().order_by('-like_users__count', '-created_at')
    else:
        articles = Article.objects.all().order_by('-created_at')
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


# 리뷰 상세 (리뷰 ID 기준)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def review_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    serializer = ArticleSerializer(article)
    return Response(serializer.data)    


# 댓글 목록 조회 & 작성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def comment_list_or_create(request, movie_id, article_id):
    article = get_object_or_404(Article, pk=article_id, movie__id=movie_id)

    if request.method == 'GET':
        comments = article.comments.all().order_by('created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 댓글 삭제
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, movie_id, article_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, article__id=article_id, article__movie__id=movie_id)
    if request.user != comment.user:
        return Response({'detail': '삭제 권한 없음'}, status=status.HTTP_403_FORBIDDEN)
    comment.delete()
    return Response({'status': 'deleted'})

# 영화 좋아요 토글
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    user = request.user
    if user in movie.like_users.all():
        movie.like_users.remove(user)
    else:
        movie.like_users.add(user)
    return Response({'status': 'ok'})

# 리뷰 좋아요 토글
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_article_like(request, movie_id, article_id):
    article = get_object_or_404(Article, pk=article_id, movie__id=movie_id)
    user = request.user
    if user in article.like_users.all():
        article.like_users.remove(user)
    else:
        article.like_users.add(user)
    serializer = ArticleSerializer(article)
    return Response(serializer.data)