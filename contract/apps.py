from django.apps import AppConfig


class ContractConfig(AppConfig):
    name = 'contract'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):       
        import contract.models