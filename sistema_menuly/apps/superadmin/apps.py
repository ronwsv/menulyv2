from django.apps import AppConfig


class SuperadminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.superadmin'
    verbose_name = 'Super Admin - Controle da Plataforma'
