from django.apps import AppConfig


class RobotsConfig(AppConfig):
    name = 'robots'

    def ready(self):
        import signals
        from . import signals
