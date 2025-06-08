import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from movies.models import Movie, Genre, Actor

class Command(BaseCommand):
    help = "Fast bulk load movie_cleaned.json with direct M2M through-table insert"

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, "movies", "fixtures", "movie.json")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
        except FileNotFoundError:
            self.stderr.write(f"[ERROR] 파일을 찾을 수 없습니다: {file_path}")
            return

        movies_to_create = []
        movie_actor_links = []
        movie_genre_links = []
        failed = 0

        for entry in raw_data:
            try:
                pk = entry["pk"]
                fields = entry["fields"]

                # 영화 객체 준비
                movie = Movie(
                    pk=pk,
                    title=fields["title"],
                    overview=fields["overview"],
                    release_date=fields["release_date"],
                    runtime=fields["runtime"],
                    poster_path=fields["poster_path"],
                    vote_average=fields["vote_average"],
                    popularity=fields["popularity"],
                )
                movies_to_create.append(movie)

                # 중간 테이블용 FK 저장
                for genre_id in fields["genres"]:
                    movie_genre_links.append(
                        Movie.genres.through(movie_id=pk, genre_id=genre_id)
                    )
                for actor_id in fields["actors"]:
                    movie_actor_links.append(
                        Movie.actors.through(movie_id=pk, actor_id=actor_id)
                    )

            except Exception as e:
                failed += 1
                self.stderr.write(f"[SKIP] pk={entry['pk']} 오류: {e}")

        # 1. Movie bulk insert
        Movie.objects.bulk_create(movies_to_create, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f"🎬 Movie insert 완료: {len(movies_to_create)}개"))

        # 2. M2M through insert
        Movie.genres.through.objects.bulk_create(movie_genre_links, ignore_conflicts=True)
        Movie.actors.through.objects.bulk_create(movie_actor_links, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS(f"✅ 중간 테이블 insert 완료: actors={len(movie_actor_links)}개, genres={len(movie_genre_links)}개"))
        self.stdout.write(self.style.WARNING(f"❌ 영화 스킵된 항목: {failed}개"))
