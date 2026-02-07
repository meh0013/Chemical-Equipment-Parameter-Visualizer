from django.apps import AppConfig
from django.conf import settings
import os


class EquipmentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'equipment'

    def ready(self):
        from django.db.models.signals import post_migrate
        from django.contrib.auth.models import User
        import os

        def create_demo_user(sender, **kwargs):
            if not User.objects.filter(username="demo").exists():
                User.objects.create_superuser(
                    "demo",
                    "demo@example.com",
                    os.environ.get("DEMO_PASSWORD", "changeme123"),
                )

        post_migrate.connect(create_demo_user, sender=self)