from django.db import models
from django.conf import settings

# 장르 (예: 액션, 코미디 등)
class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# 배우
class Actor(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# 영화
class Movie(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    release_date = models.DateField(null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True)
    poster_path = models.TextField(null=True, blank=True)

    vote_average = models.FloatField(default=0)
    popularity = models.FloatField(default=0)

    genres = models.ManyToManyField(Genre, related_name='movies')
    actors = models.ManyToManyField(Actor, related_name='movies')

    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_movies', blank=True
    )
    bookmark_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='bookmark_movies', blank=True
    )

    def __str__(self):
        return self.title


# 유저 리뷰 (게시글)
class Article(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='articles')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='articles')
    title = models.CharField(max_length=100)
    content = models.TextField()
    rate = models.IntegerField(default=5)  # 1~10점

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_articles', blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.title}"


# 댓글
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}의 댓글"
