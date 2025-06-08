import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from movies.models import Actor

class Command(BaseCommand):
    help = "Fast bulk load actors.json without FK concerns"

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, "movies", "fixtures", "actors.json")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
        except FileNotFoundError:
            self.stderr.write(f"[ERROR] 파일을 찾을 수 없습니다: {file_path}")
            return

        actors_to_create = []
        for entry in raw_data:
            try:
                pk = entry["pk"]  # 배우 기본키, 무시해도 됨
                name = entry["fields"]["name"]
                actors_to_create.append(Actor(id=pk, name=name))
            except Exception as e:
                self.stderr.write(f"[SKIP] pk={entry.get('pk', 'unknown')} 오류: {e}")

        Actor.objects.bulk_create(actors_to_create, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f"✅ 배우 insert 완료: {len(actors_to_create)}개"))
