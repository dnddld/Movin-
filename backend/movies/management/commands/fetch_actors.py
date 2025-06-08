import os
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from movies.models import Movie, Actor
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_URL = "https://api.themoviedb.org/3"

class Command(BaseCommand):
    help = "Fetch actors for each movie from TMDB"

    def handle(self, *args, **kwargs):
        movies = Movie.objects.all()
        for movie in movies:
            print(f"🎬 Fetching actors for: {movie.title}")
            url = f"{TMDB_URL}/movie/{movie.id}/credits"
            params = {
                "api_key": TMDB_API_KEY,
                "language": "ko-KR"
            }
            response = requests.get(url, params=params)

            if response.status_code != 200:
                print(f"❌ 배우 불러오기 실패: {movie.title}")
                continue

            data = response.json()
            cast_list = data.get("cast", [])[:10]  # 상위 10명 배우만

            for cast in cast_list:
                name = cast.get("name")
                if name:
                    actor, _ = Actor.objects.get_or_create(name=name)
                    movie.actors.add(actor)

        print("✅ 모든 영화에 배우 연결 완료")
