from django.apps import AppConfig
from django.db.models.signals import post_migrate
import os


class EquipmentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "equipment"

    def ready(self):
        from django.contrib.auth import get_user_model

        def create_demo_user(sender, **kwargs):
            User = get_user_model()
            password = os.environ.get("DEMO_PASSWORD", "changeme123")

            user, created = User.objects.get_or_create(
                username="demo",
                defaults={
                    "email": "demo@example.com",
                    "is_staff": True,
                    "is_superuser": True,
                },
            )

            # Always sync password from env
            user.set_password(password)
            user.save()

        post_migrate.connect(create_demo_user, sender=self)
