from django.urls import path
from . import views

urlpatterns = [
    # 영화 목록 & 상세
    path('', views.movie_list),
    path('<int:movie_id>/', views.movie_detail),
    path('simple/', views.simple_movies, name='simple-movies'),
    # 찜(북마크) 토글
    path('<int:movie_id>/bookmark/', views.toggle_bookmark),
    # 좋아요 토글
    path('<int:movie_id>/like/', views.toggle_like),


    # 리뷰 목록 & 작성
    path('<int:movie_id>/articles/', views.article_list_or_create),
    # 리뷰 상세 / 수정 / 삭제 / 좋아요
    path('<int:movie_id>/articles/<int:article_id>/', views.article_detail),
    path('<int:movie_id>/articles/<int:article_id>/like/', views.toggle_article_like),
    # 전체 리뷰 조회 & 단일 리뷰 상세
    path('articles/', views.all_reviews),  # 전체 리뷰 목록
    path('articles/<int:article_id>/detail/', views.review_detail),  # 단일 리뷰 상세
    

    # 댓글 목록 & 작성
    path('<int:movie_id>/articles/<int:article_id>/comments/', views.comment_list_or_create),
    # 댓글 삭제
    path('<int:movie_id>/articles/<int:article_id>/comments/<int:comment_id>/', views.delete_comment),

    

]
