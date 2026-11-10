"""
Señales (Signals) del Módulo Core.
Garantiza la creación automática de progreso al dar de alta colaboradores.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Usuario, ProgresoUsuario, RolUsuarioChoices, ParametroGlobal
from .utils import resequenciar_ids_usuarios


@receiver(post_save, sender=Usuario)
def crear_o_actualizar_progreso_usuario(sender, instance, created, **kwargs):
    """
    Crea automáticamente el perfil de ProgresoUsuario si no existe cuando se crea un usuario.
    Toma los valores por defecto configurados en ParametroGlobal o usa valores de respaldo.
    """
    if created:
        from .utils import get_parametro_global
        vidas_def = get_parametro_global('vidas_iniciales', 3, tipo=int)
        oro_def = get_parametro_global('oro_inicial', 100, tipo=int)
        gemas_def = get_parametro_global('gemas_iniciales', 10, tipo=int)

        ProgresoUsuario.objects.get_or_create(
            usuario=instance,
            defaults={
                'nivel': 1,
                'xp': 0,
                'oro': oro_def,
                'gemas': gemas_def,
                'vidas_actuales': vidas_def
            }
        )


@receiver(post_delete, sender=Usuario)
def resequenciar_al_eliminar_usuario(sender, instance, **kwargs):
    """
    Cuando un usuario es eliminado, reorganiza inmediatamente las IDs de los usuarios restantes
    para que se mantengan continuas (1, 2, 3...) sin huecos, sincronizando las tablas relacionadas.
    """
    resequenciar_ids_usuarios()

