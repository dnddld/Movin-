import os
import requests
from django.core.management.base import BaseCommand
from movies.models import Movie, Genre, Actor
from django.conf import settings

API_KEY = os.environ.get('TMDB_API_KEY')  # .env에서 가져옴
BASE_URL = 'https://api.themoviedb.org/3'


class Command(BaseCommand):
    help = 'Fetch movies from TMDB API and store in DB'

    def handle(self, *args, **kwargs):
        total_pages = 500  # TMDB는 최대 500페이지까지 제공
        count = 0

        for page in range(1, total_pages + 1):
            print(f'📦 Fetching page {page}')
            res = requests.get(f'{BASE_URL}/movie/popular', params={
                'api_key': API_KEY,
                'language': 'ko-KR',
                'page': page
            })

            if res.status_code != 200:
                print('❌ API 요청 실패', res.status_code)
                break

            for item in res.json().get('results', []):
                movie, created = Movie.objects.get_or_create(
                    id=item['id'],
                    defaults={
                        'title': item.get('title'),
                        'overview': item.get('overview', ''),
                        'release_date': item.get('release_date') or None,
                        'poster_path': item.get('poster_path'),
                        'vote_average': item.get('vote_average', 0),
                        'popularity': item.get('popularity', 0),
                    }
                )

                # 장르 처리
                for genre_id in item.get('genre_ids', []):
                    genre_name = self.get_genre_name(genre_id)
                    genre_obj, _ = Genre.objects.get_or_create(name=genre_name)
                    movie.genres.add(genre_obj)

                count += 1

            print(f'✅ {count} movies fetched so far')

        print('🎉 완료!')

    def get_genre_name(self, genre_id):
        genre_map = {
            28: '액션', 12: '모험', 16: '애니메이션', 35: '코미디', 80: '범죄',
            99: '다큐멘터리', 18: '드라마', 10751: '가족', 14: '판타지',
            36: '역사', 27: '공포', 10402: '음악', 9648: '미스터리',
            10749: '로맨스', 878: 'SF', 10770: 'TV 영화', 53: '스릴러',
            10752: '전쟁', 37: '서부'
        }
        return genre_map.get(genre_id, '기타')
