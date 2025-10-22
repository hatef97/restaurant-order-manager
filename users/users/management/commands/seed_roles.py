from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


ROLES = ["owner", "manager", "chef", "server", "cashier"]


class Command(BaseCommand):
    help = "Create default role groups"

    def handle(self, *args, **kwargs):
        for r in ROLES:
            Group.objects.get_or_create(name=r)
        self.stdout.write(
            self.style.SUCCESS("Roles created/ensured: " + ", ".join(ROLES))
        )
