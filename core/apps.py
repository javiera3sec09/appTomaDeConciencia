from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Gestión del Videojuego y Cumplimiento ISO'

    def ready(self):
        # Registro de señales automáticas (creación de progreso de usuario, etc.)
        import core.signals  # noqa
