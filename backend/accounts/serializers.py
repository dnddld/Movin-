from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from dj_rest_auth.registration.serializers import RegisterSerializer
from movies.serializers import MovieListSerializer
from movies.serializers_article import UserArticleSerializer
from .serializers_user import UserSerializer
from django.utils.dateparse import parse_date

User = get_user_model()


# 유저 상세 조회 (팔로워 포함)
class ProfileSerializer(serializers.ModelSerializer):
    followers = UserSerializer(many=True, read_only=True)
    followings = UserSerializer(many=True, read_only=True)
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    like_movies = serializers.SerializerMethodField()
    bookmark_movies = serializers.SerializerMethodField()
    articles = UserArticleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'profile_img',
            'followers', 'followings',
            'follower_count', 'following_count',
            'like_movies', 'bookmark_movies',
            'articles','nickname',
        )

    def get_follower_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.followings.count()

    def get_like_movies(self, obj):
        from movies.models import Movie
        movies = Movie.objects.filter(like_users=obj)
        return MovieListSerializer(movies, many=True).data

    def get_bookmark_movies(self, obj):
        from movies.models import Movie
        movies = Movie.objects.filter(bookmark_users=obj)
        return MovieListSerializer(movies, many=True).data



# 내 프로필 (마이페이지)
class MyProfileSerializer(serializers.ModelSerializer):
    like_movies = MovieListSerializer(many=True, read_only=True)
    bookmark_movies = MovieListSerializer(many=True, read_only=True)
    articles = UserArticleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'nickname', 'birth', 'profile_img',
            'like_movies', 'bookmark_movies', 'articles'
        )


# 프로필 수정용 (비번 포함)
class ProfileUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True, required=False)
    profile_img = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('nickname', 'password', 'password2','profile_img')

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')        

        if password or password2:
            if password != password2:
                raise serializers.ValidationError({'password': '비밀번호가 일치하지 않습니다.'})
            validate_password(password)

        return data

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        profile_img = validated_data.pop('profile_img', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        if profile_img:
            instance.profile_img = profile_img

        instance.save()
        return super().update(instance, validated_data)


