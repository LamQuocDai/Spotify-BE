from django.core.management.base import BaseCommand
from apps.users.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@gmail.com',
                password='123456'
            )
            self.stdout.write(self.style.SUCCESS('Admin user created'))