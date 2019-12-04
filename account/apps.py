from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'account'

    def ready(self):
        import authentication.signals
        from utils.cron_jobs import start
        start()
