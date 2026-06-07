import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from tracker.models import User

user1, created1 = User.objects.get_or_create(email='test1@coupleapp.com', defaults={'username': 'test1@coupleapp.com', 'name': 'Test User 1'})
user1.set_password('testing123')
user1.save()

user2, created2 = User.objects.get_or_create(email='test2@coupleapp.com', defaults={'username': 'test2@coupleapp.com', 'name': 'Test User 2'})
user2.set_password('testing123')
user2.save()

print("Created test accounts:")
print("1. Email: test1@coupleapp.com | Password: testing123")
print("2. Email: test2@coupleapp.com | Password: testing123")
