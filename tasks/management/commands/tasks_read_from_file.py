from encodings import utf_8
from django.core.management import BaseCommand
from datetime import datetime, timezone
from tasks.models import TodoItem

class Command(BaseCommand):
    help = u"Read tasks from file (one line = one task)and save them to db"

    def add_arguments(self, parser):
        parser.add_argument('--file', dest='input_file', type=str)

    def handle(self, *args, **options):
        now = datetime.now(timezone.utc)
        with open(options["input_file"],encoding="utf_8") as file:
            for line in file.readlines():
                new_task = TodoItem(description = line)
                new_task.save()
                
    

