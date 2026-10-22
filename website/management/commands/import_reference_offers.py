import json
from pathlib import Path
from datetime import datetime, time
from django.core.management.base import BaseCommand
from django.utils import timezone
from website.models import JobOffer


class Command(BaseCommand):
    help = 'Importer les offres du modèle sans écraser les modifications du cabinet.'

    def handle(self, *args, **options):
        data = json.loads((Path(__file__).resolve().parents[3] / 'static/reference/content.json').read_text())
        count = 0
        for j in data['jobs']:
            _, created = JobOffer.objects.get_or_create(slug=j['id'], defaults=dict(
                title=j['title'], location=j['location'], contract_type='freelance',
                short_description=j['contract'], description=j['description'],
                published_at=timezone.now(), closing_date=timezone.make_aware(datetime.combine(datetime.fromisoformat(j['deadline']).date(), time(23, 59, 59))),
                is_published=True))
            count += created
        self.stdout.write(self.style.SUCCESS(f'{count} offre(s) importée(s).'))
