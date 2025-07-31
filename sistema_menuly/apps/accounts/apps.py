from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    verbose_name = 'Contas de Usuário'
    
    def ready(self):
        # Importar signals se existirem
        try:
            import apps.accounts.signals
        except ImportError:
            pass
