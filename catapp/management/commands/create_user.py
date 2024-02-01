# from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User
#
# class Command(BaseCommand):
#     help = 'Create a new user'
#
#     def handle(self,your_username,your_password, *args, **options):
#         username = your_username
#         password = your_password
#
#         if not User.objects.filter(username=username).exists():
#             User.objects.create_user(username=username, password=password)
#             self.stdout.write(self.style.SUCCESS('User created successfully'))
#         else:
#             self.stdout.write(self.style.WARNING('User already exists'))



from django.core.management.base import BaseCommand
from catapp.utils import create_user

class Command(BaseCommand):
    help = 'Create a new user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username for the new user')
        parser.add_argument('password', type=str, help='Password for the new user')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']

        if create_user(username, password):
            self.stdout.write(self.style.SUCCESS('User created successfully'))
        else:
            self.stdout.write(self.style.WARNING('User already exists'))