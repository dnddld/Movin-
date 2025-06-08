from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import User
from movies.serializers_article import UserArticleSerializer


class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=True, max_length=100)
    birth = serializers.DateField(required=False, allow_null=True)
    profile_img = serializers.CharField(required=False, allow_blank=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname', '')
        data['birth'] = self.validated_data.get('birth', None)
        data['profile_img'] = self.validated_data.get('profile_img', None)
        return data

    def save(self, request):
        user = super().save(request)
        cleaned_data = self.get_cleaned_data()
        user.nickname = cleaned_data.get('nickname', '')
        user.birth = cleaned_data.get('birth')
        user.profile_img = cleaned_data.get('profile_img')
        print("✅ [DEBUG] 닉네임 저장됨:", user.nickname)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    articles = UserArticleSerializer(many=True, read_only=True)  # 내가 쓴 리뷰 추가

    class Meta:
        model = User
        fields = (
            'id', 'username', 'nickname', 'birth', 'profile_img',
            'like_movies', 'bookmark_movies', 'articles'
        )
