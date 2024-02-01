# utils.py
from django.contrib.auth.models import User

def create_user(username, password,email):
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username=username, password=password,email=email)
        return True
    else:
        return False
