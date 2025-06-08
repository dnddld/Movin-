from rest_framework import serializers
from .models import Movie

# 영화 간단 정보 (리뷰 목록용)
class MovieSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path', 'release_date', 'vote_average')