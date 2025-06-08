from rest_framework import serializers
from .models import Article
from movies.serializers_movie import MovieSimpleSerializer
from accounts.serializers_simple import SimpleUserSerializer

# 유저 프로필용 간단 리뷰 목록
class UserArticleSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    movie = MovieSimpleSerializer(read_only=True)  

    class Meta:
        model = Article
        fields = ('id', 'user', 'movie', 'title', 'rate', 'content', 'created_at')