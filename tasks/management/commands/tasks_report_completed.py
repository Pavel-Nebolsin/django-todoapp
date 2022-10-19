from django.core.management import BaseCommand
from datetime import datetime, timezone
from tasks.models import TodoItem

class Command(BaseCommand):
    help = u"Display tasks completed in entered number of days"
    
    def add_arguments(self, parser):
        parser.add_argument('--days', dest='days', type=int, default=3)
    
    def handle(self, *args, **options):
        now = datetime.now(timezone.utc)
        for t in TodoItem.objects.filter(is_completed=True):
            if (now - t.updated).days <= options['days']:
                print(f"Выполненная за последние {options['days']} дней задача:", f"Была выполена {t.updated}")
