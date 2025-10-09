from django.apps import AppConfig


class IndexConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "autograder.apps.index"

    def ready(self):
        import autograder.apps.index.signals  # noqa: F401
