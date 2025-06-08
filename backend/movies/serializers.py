from rest_framework import serializers
from .models import Movie, Genre, Actor, Article, Comment
from accounts.serializers_user import UserSerializer  
from movies.serializers_movie import MovieSimpleSerializer

# 장르
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')

# 배우
class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('id', 'name')

# 영화 목록용
class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path', 'vote_average')

# 영화 상세용
class MovieDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)
    like_users = UserSerializer(many=True, read_only=True)        
    bookmark_users = UserSerializer(many=True, read_only=True)    

    class Meta:
        model = Movie
        fields = '__all__'

# 리뷰
class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie = MovieSimpleSerializer(read_only=True)  #  영화 간단 정보 포함
    like_users = UserSerializer(many=True, read_only=True)
    like_user_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('movie', 'user')

    def get_like_user_count(self, obj):
        return obj.like_users.count()

# 댓글
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) 
    article = serializers.PrimaryKeyRelatedField(read_only=True)                      

    class Meta:
        model = Comment
        fields = '__all__'
