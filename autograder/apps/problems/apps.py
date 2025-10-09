from django.apps import AppConfig


class ProblemsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "autograder.apps.problems"

    def ready(self):
        import autograder.apps.problems.signals  # noqa: F401
