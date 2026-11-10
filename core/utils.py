"""
Utilidades auxiliares para Auditoría, Seguridad y Gestión de Red.
"""
from django.forms.models import model_to_dict
from .models import RegistroAuditoria, AccionAuditoriaChoices


def get_parametro_global(clave: str, default=None, tipo=str):
    """
    Obtiene el valor configurado de un Parámetro Global desde la base de datos SQLite.
    Convierte al tipo solicitado (int, float, bool, str). Si no existe o falla, retorna default.
    """
    from .models import ParametroGlobal
    try:
        p = ParametroGlobal.objects.filter(clave=clave).first()
        if p and p.valor is not None:
            val_str = str(p.valor).strip()
            if tipo == int:
                return int(val_str)
            elif tipo == float:
                return float(val_str)
            elif tipo == bool:
                return val_str.lower() in ('true', '1', 'si', 'yes', 'verdadero', 'activo')
            return val_str
    except Exception:
        pass
    return default


def aplicar_regeneracion_vidas(progreso):
    """
    Calcula y aplica la regeneración periódica de vidas (Energía Arcana)
    usando los parámetros globales 'vidas_maximas' y 'regeneracion_minutos'.
    Retorna: (progreso, vidas_maximas, segundos_para_siguiente, regeneracion_min)
    """
    from django.utils import timezone
    from datetime import timedelta

    vidas_maximas = get_parametro_global('vidas_maximas', 3, tipo=int)
    regeneracion_min = get_parametro_global('regeneracion_minutos', 5, tipo=int)

    if vidas_maximas <= 0:
        vidas_maximas = 3
    if regeneracion_min <= 0:
        regeneracion_min = 5

    ahora = timezone.now()
    segundos_ciclo = regeneracion_min * 60
    segundos_para_siguiente = 0

    if progreso.vidas_actuales >= vidas_maximas:
        if progreso.vidas_actuales > vidas_maximas:
            progreso.vidas_actuales = vidas_maximas
            progreso.save(update_fields=['vidas_actuales'])
        # Si tiene vidas al máximo, marcamos el punto de inicio para cuando pierda una vida
        progreso.ultimo_reinicio_vidas = ahora
        progreso.save(update_fields=['ultimo_reinicio_vidas'])
        segundos_para_siguiente = 0
    else:
        # Vidas por debajo del tope configurado
        if not progreso.ultimo_reinicio_vidas:
            progreso.ultimo_reinicio_vidas = ahora
            progreso.save(update_fields=['ultimo_reinicio_vidas'])

        delta = (ahora - progreso.ultimo_reinicio_vidas).total_seconds()
        if delta < 0:
            delta = 0
            progreso.ultimo_reinicio_vidas = ahora
            progreso.save(update_fields=['ultimo_reinicio_vidas'])

        if delta >= segundos_ciclo:
            vidas_a_recuperar = int(delta // segundos_ciclo)
            nueva_vida = min(vidas_maximas, progreso.vidas_actuales + vidas_a_recuperar)
            segundos_sobrantes = delta % segundos_ciclo

            progreso.vidas_actuales = nueva_vida
            if nueva_vida >= vidas_maximas:
                progreso.ultimo_reinicio_vidas = ahora
                segundos_para_siguiente = 0
            else:
                progreso.ultimo_reinicio_vidas = ahora - timedelta(seconds=segundos_sobrantes)
                segundos_para_siguiente = max(0, int(segundos_ciclo - segundos_sobrantes))
            progreso.save(update_fields=['vidas_actuales', 'ultimo_reinicio_vidas'])
        else:
            segundos_para_siguiente = max(0, int(segundos_ciclo - delta))

    return progreso, vidas_maximas, segundos_para_siguiente, regeneracion_min


def sincronizar_efecto_parametro_global(parametro_obj):
    """
    Propaga y aplica inmediatamente los efectos de un Parámetro Global en el juego
    para que los cambios realizados por el administrador sean visibles y reales para los jugadores:
    - vidas_maximas: Actualiza el tope de vidas y el display de energía para todos los usuarios.
    - vidas_iniciales: Actualiza usuarios sin partidas o en nivel 1.
    - oro_inicial: Actualiza usuarios que no han modificado su balance inicial.
    - gemas_iniciales: Actualiza usuarios que no han modificado su balance inicial.
    """
    from .models import ProgresoUsuario, PartidaJugada
    clave = getattr(parametro_obj, 'clave', '')
    valor = str(getattr(parametro_obj, 'valor', '')).strip()

    try:
        if clave == 'vidas_maximas' and valor.isdigit():
            nuevo_max = int(valor)
            if nuevo_max > 0:
                # Topar a los que excedan el nuevo máximo
                ProgresoUsuario.objects.filter(vidas_actuales__gt=nuevo_max).update(vidas_actuales=nuevo_max)
                # Actualizar a los jugadores para que disfruten del nuevo tope de vidas/energía de inmediato
                ProgresoUsuario.objects.all().update(vidas_actuales=nuevo_max)

        elif clave == 'vidas_iniciales' and valor.isdigit():
            nuevas_vidas = int(valor)
            if nuevas_vidas > 0:
                usuarios_con_partidas = PartidaJugada.objects.values_list('usuario_id', flat=True).distinct()
                ProgresoUsuario.objects.exclude(usuario_id__in=usuarios_con_partidas).filter(nivel=1, xp=0).update(
                    vidas_actuales=nuevas_vidas
                )

        elif clave == 'oro_inicial' and valor.isdigit():
            nuevo_oro = int(valor)
            usuarios_con_partidas = PartidaJugada.objects.values_list('usuario_id', flat=True).distinct()
            ProgresoUsuario.objects.exclude(usuario_id__in=usuarios_con_partidas).filter(nivel=1, xp=0).update(
                oro=nuevo_oro
            )

        elif clave == 'gemas_iniciales' and valor.isdigit():
            nuevas_gemas = int(valor)
            usuarios_con_partidas = PartidaJugada.objects.values_list('usuario_id', flat=True).distinct()
            ProgresoUsuario.objects.exclude(usuario_id__in=usuarios_con_partidas).filter(nivel=1, xp=0).update(
                gemas=nuevas_gemas
            )
    except Exception:
        pass


def get_client_ip(request):
    """
    Extrae la dirección IP real del cliente considerando proxies y balanceadores de carga.
    """
    if not request:
        return None
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def registrar_auditoria(
    admin,
    accion: str,
    modulo_afectado: str,
    registro_id: str,
    datos_anteriores: dict = None,
    datos_nuevos: dict = None,
    request=None,
    ip: str = None
):
    """
    Registra de forma inmutable una acción administrativa en el modelo RegistroAuditoria.
    """
    client_ip = ip or get_client_ip(request)
    admin_user = admin if (admin and getattr(admin, 'is_authenticated', False)) else None

    return RegistroAuditoria.objects.create(
        admin=admin_user,
        accion=accion,
        modulo_afectado=modulo_afectado,
        registro_id=str(registro_id),
        datos_anteriores=datos_anteriores,
        datos_nuevos=datos_nuevos,
        direccion_ip=client_ip
    )


def serialize_instance(instance):
    """
    Convierte una instancia de modelo a un diccionario serializable para la bitácora de auditoría.
    """
    if not instance:
        return None
    try:
        data = model_to_dict(instance)
        # Convertir tipos no serializables en texto plano
        for key, value in list(data.items()):
            if hasattr(value, 'isoformat'):
                data[key] = value.isoformat()
            elif hasattr(value, 'url'):
                try:
                    data[key] = value.url
                except Exception:
                    data[key] = str(value)
            elif hasattr(value, 'name'):
                data[key] = str(value.name)
            elif not isinstance(value, (str, int, float, bool, list, dict, type(None))):
                data[key] = str(value)
        return data
    except Exception:
        return {'str_repr': str(instance)}


def resequenciar_ids_usuarios():
    """
    Reordena y reasigna los IDs de todos los usuarios de forma estrictamente secuencial:
    1, 2, 3, 4, 5... actualizando de forma coherente todas las tablas relacionadas
    (ProgresoUsuario, PartidaJugada, RegistroAuditoria) y actualizando la secuencia SQLite
    para que la siguiente ID generada sea N + 1.
    """
    from django.db import connection, transaction
    from .models import Usuario

    with transaction.atomic():
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA foreign_keys = OFF;")
            usuarios = list(Usuario.objects.order_by('id'))
            if not usuarios:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'core_usuario';")
                cursor.execute("PRAGMA foreign_keys = ON;")
                return

            # Fase 1: Pasar a IDs temporales negativas para evitar colisiones
            for idx, u in enumerate(usuarios, start=1):
                temp_id = -(10000 + idx)
                old_id = u.id
                cursor.execute("UPDATE core_usuario SET id = %s WHERE id = %s", [temp_id, old_id])
                cursor.execute("UPDATE core_progreso_usuario SET usuario_id = %s WHERE usuario_id = %s", [temp_id, old_id])
                cursor.execute("UPDATE core_partida_jugada SET usuario_id = %s WHERE usuario_id = %s", [temp_id, old_id])
                cursor.execute("UPDATE core_registro_auditoria SET admin_id = %s WHERE admin_id = %s", [temp_id, old_id])
                cursor.execute("UPDATE core_registro_auditoria SET registro_id = %s WHERE modulo_afectado = 'Usuario' AND registro_id = %s", [str(temp_id), str(old_id)])

            # Fase 2: Asignar IDs consecutivas finales (1, 2, 3, ...)
            for idx, u in enumerate(usuarios, start=1):
                temp_id = -(10000 + idx)
                final_id = idx
                cursor.execute("UPDATE core_usuario SET id = %s WHERE id = %s", [final_id, temp_id])
                cursor.execute("UPDATE core_progreso_usuario SET usuario_id = %s WHERE usuario_id = %s", [final_id, temp_id])
                cursor.execute("UPDATE core_partida_jugada SET usuario_id = %s WHERE usuario_id = %s", [final_id, temp_id])
                cursor.execute("UPDATE core_registro_auditoria SET admin_id = %s WHERE admin_id = %s", [final_id, temp_id])
                cursor.execute("UPDATE core_registro_auditoria SET registro_id = %s WHERE modulo_afectado = 'Usuario' AND registro_id = %s", [str(final_id), str(temp_id)])

            # Fase 3: Ajustar sqlite_sequence
            max_id = len(usuarios)
            cursor.execute("SELECT 1 FROM sqlite_sequence WHERE name = 'core_usuario'")
            if cursor.fetchone():
                cursor.execute("UPDATE sqlite_sequence SET seq = %s WHERE name = 'core_usuario'", [max_id])
            else:
                cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('core_usuario', %s)", [max_id])
            cursor.execute("PRAGMA foreign_keys = ON;")

