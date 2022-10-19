from django.core.management import BaseCommand
from datetime import datetime, timezone
from tasks.models import TodoItem
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = u"Display top users by amount of tasks"
    
    def add_arguments(self, parser):
        parser.add_argument('--users', dest='users', type=int, default=10)
    
    @staticmethod
    def count_user_tasks(user):
        task_amount = 0            
        for t in user.tasks.all():
            task_amount += 1
        return task_amount
    
    @staticmethod
    def count_completed_tasks(user, flag):
        task_amount = 0            
        for t in user.tasks.all():
            if t.is_completed == flag:
                task_amount += 1

        return task_amount
    
    def handle(self, *args, **options):
        all_completed_tasks = 0
        users_tasks_dict = {}
        users_completed_tasks_dict = {}
        users_uncompleted_tasks_dict = {}
        users_less_20 = 0
        
        for user in User.objects.all():
            users_tasks_dict[user.pk] = self.count_user_tasks(user)
            users_completed_tasks_dict[user.pk] = self.count_completed_tasks(user, True)
            users_uncompleted_tasks_dict[user.pk] = self.count_completed_tasks(user, False)
        
        for i in users_completed_tasks_dict.values():
            all_completed_tasks += i
        
        for i in users_uncompleted_tasks_dict.values():
            if i < 20:
                users_less_20 += 1

        sorted_users_tasks_dict = dict(sorted(users_tasks_dict.items(), key=lambda x: x[1], reverse=True))
        users_uncompleted_tasks_dict = dict(sorted(users_uncompleted_tasks_dict.items(), key=lambda x: x[1], reverse=True))
        
        print(f"Пользователь номер 2 по невып.:{User.objects.get(pk=list(users_uncompleted_tasks_dict.items())[1][0])}. Кол-во невып.:{list(users_uncompleted_tasks_dict.items())[1][1]}")
        print(f"Пользователей у которых меньше 20 невыполненных: {users_less_20}")
        print(f"Всего выполнено задач: {all_completed_tasks}")
        print(f"TOP {options['users']} пользователей по количеству задач:")
        i = 0
        while i < options['users']:

            cursor = list(sorted_users_tasks_dict.items())[i]
            username = User.objects.get(pk=cursor[0])
            tasks_amount = cursor[1]
            
            print(f"{i+1}: {username}: {tasks_amount} задач")
            i += 1
