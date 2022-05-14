from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'qorb.accounts'

    def ready(self):
        import qorb.accounts.signals
