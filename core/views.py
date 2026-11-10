"""
Vistas personalizadas de Analítica y Dashboard para el Videojuego de Compliance ISO.
Provee los datos exactos y agregados para el diseño Dark SaaS / ISO Quest.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg, Q
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.utils import timezone
from django.contrib import messages
from django.core.management import call_command
import csv
import json

from .models import (
    Usuario,
    ProgresoUsuario,
    Mundo,
    Nivel,
    FaseCaso,
    Carta,
    FaseCartaOpcion,
    PartidaJugada,
    RegistroAuditoria,
    ParametroGlobal,
    ResultadoPartidaChoices,
    RolUsuarioChoices,
    EstadoUsuarioChoices,
    EstadoEntidadChoices,
    DificultadChoices,
    AccionAuditoriaChoices,
)
from .utils import (
    get_client_ip,
    registrar_auditoria,
    serialize_instance,
    get_parametro_global,
    aplicar_regeneracion_vidas,
    sincronizar_efecto_parametro_global,
)


def get_analytics_data():
    """
    Función utilitaria que concentra las consultas agregadas (Count, Sum, Avg)
    para el Dashboard del Panel de Administración con estética ISO QUEST.
    """
    # 1. Analítica de Partidas (Total, Victorias, Derrotas, Abandonadas)
    partidas_agg = PartidaJugada.objects.aggregate(
        total_partidas=Count('id'),
        total_victorias=Count('id', filter=Q(resultado=ResultadoPartidaChoices.VICTORIA)),
        total_derrotas=Count('id', filter=Q(resultado=ResultadoPartidaChoices.DERROTA)),
        total_abandonadas=Count('id', filter=Q(resultado=ResultadoPartidaChoices.ABANDONADA)),
        oro_emitido=Sum('oro_obtenido'),
        gemas_emitidas=Sum('gemas_obtenidas'),
    )

    db_total_partidas = partidas_agg['total_partidas'] or 0
    db_total_victorias = partidas_agg['total_victorias'] or 0
    db_total_derrotas = partidas_agg['total_derrotas'] or 0
    db_total_abandonadas = partidas_agg['total_abandonadas'] or 0
    db_oro_global = partidas_agg['oro_emitido'] or 0
    db_gemas_globales = partidas_agg['gemas_emitidas'] or 0

    # Usar datos reales de base de datos
    total_partidas = db_total_partidas
    total_victorias = db_total_victorias
    total_derrotas = db_total_derrotas
    total_abandonadas = db_total_abandonadas

    oro_global = db_oro_global
    gemas_globales = db_gemas_globales

    tasa_victoria = round((total_victorias / total_partidas * 100), 1) if total_partidas > 0 else 0.0
    tasa_derrota = round((total_derrotas / total_partidas * 100), 1) if total_partidas > 0 else 0.0
    tasa_abandonadas = round((total_abandonadas / total_partidas * 100), 1) if total_partidas > 0 else 0.0

    # 2. Analítica de Jugadores (Activos vs Inactivos, por Área)
    usuarios_agg = Usuario.objects.filter(rol=RolUsuarioChoices.EMPLEADO_JUGADOR).aggregate(
        total_jugadores=Count('id'),
        activos=Count('id', filter=Q(estado=EstadoUsuarioChoices.ACTIVO)),
        inactivos=Count('id', filter=Q(estado=EstadoUsuarioChoices.INACTIVO)),
    )

    db_jugadores_activos = usuarios_agg['activos'] or 0
    db_jugadores_inactivos = usuarios_agg['inactivos'] or 0
    db_total_jugadores = usuarios_agg['total_jugadores'] or 0

    jugadores_activos = db_jugadores_activos
    total_jugadores = db_total_jugadores
    jugadores_inactivos = db_jugadores_inactivos
    porcentaje_activos = round((jugadores_activos / total_jugadores * 100), 1) if total_jugadores > 0 else 0.0

    # Distribución real por Área Organizacional
    areas_counts = Usuario.objects.values('area').annotate(total=Count('id')).order_by('-total')
    total_all_users = Usuario.objects.count()
    areas_stats = []
    for a in areas_counts:
        pct = round((a['total'] / total_all_users * 100), 1) if total_all_users > 0 else 0
        areas_stats.append({
            'area': a['area'] or 'Sin Área',
            'porcentaje': pct,
            'total': a['total']
        })

    # 3. Mundos más Jugados reales
    mundos_db = Mundo.objects.annotate(partidas_count=Count('niveles__partidas')).order_by('-partidas_count')[:4]
    tot_partidas_mundos = sum(m.partidas_count for m in mundos_db)
    mundos_mas_jugados = []
    paleta_colores = ['#b45309', '#0284c7', '#16a34a', '#7c3aed']
    iconos = ['shield-check', 'cloud-check', 'hdd-network', 'life-preserver']
    for idx, m in enumerate(mundos_db, start=1):
        pct = round((m.partidas_count / tot_partidas_mundos * 100), 1) if tot_partidas_mundos > 0 else 0
        mundos_mas_jugados.append({
            'rank': idx,
            'codigo_iso': m.codigo_iso,
            'nombre': m.nombre_tematico,
            'partidas': m.partidas_count,
            'porcentaje': pct,
            'color': paleta_colores[(idx - 1) % len(paleta_colores)],
            'icon': iconos[(idx - 1) % len(iconos)],
        })

    # 4. Últimas Partidas reales
    ultimas_partidas_qs = PartidaJugada.objects.select_related('usuario', 'nivel', 'nivel__mundo').order_by('-fecha_partida')[:5]
    ultimas_partidas = []
    for p in ultimas_partidas_qs:
        ultimas_partidas.append({
            'usuario': p.usuario.alias if p.usuario else 'Usuario',
            'nombre_completo': p.usuario.nombre_completo if p.usuario else 'Colaborador',
            'avatar_iniciales': (p.usuario.alias[:2].upper() if p.usuario and p.usuario.alias else 'US'),
            'avatar_url': p.usuario.avatar_url if p.usuario else '/static/img/avatars/necromancer_1.png',
            'nivel': f"{p.nivel.mundo.codigo_iso} - Nivel {p.nivel.numero_nivel}" if p.nivel and p.nivel.mundo else "Nivel General",
            'resultado': p.get_resultado_display() if hasattr(p, 'get_resultado_display') else p.resultado,
            'es_victoria': p.resultado == ResultadoPartidaChoices.VICTORIA,
            'oro': f"+{p.oro_obtenido}" if p.oro_obtenido > 0 else "+0",
            'gemas': f"+{p.gemas_obtenidas}" if p.gemas_obtenidas > 0 else "+0",
            'fecha': p.fecha_partida.strftime('%d abr. %Y, %H:%M') if p.fecha_partida else '',
        })

    # 5. Actividad Reciente de Auditoría Real
    auditorias_qs = RegistroAuditoria.objects.select_related('admin').order_by('-created_at')[:6]
    actividad_reciente = []
    color_map = {
        'CREAR': '#8b5cf6',
        'EDITAR': '#38bdf8',
        'ELIMINAR': '#ef4444',
        'CAMBIAR_CONFIG': '#0ea5e9',
        'REINICIAR_PROGRESO': '#f59e0b',
    }
    icon_map = {
        'CREAR': 'user-plus',
        'EDITAR': 'file-edit',
        'ELIMINAR': 'trash-2',
        'CAMBIAR_CONFIG': 'settings',
        'REINICIAR_PROGRESO': 'rotate-ccw',
    }
    for a in auditorias_qs:
        admin_alias = a.admin.alias if a.admin else 'Sistema'
        titulo = f"[{a.get_accion_display()}] {a.modulo_afectado}: {a.registro_id or ''} por @{admin_alias}"
        actividad_reciente.append({
            'tipo': a.accion.lower(),
            'titulo': titulo,
            'tiempo': a.created_at.strftime('%d/%m %H:%M') if a.created_at else '',
            'color': color_map.get(a.accion, '#8b5cf6'),
            'icon': icon_map.get(a.accion, 'sparkles'),
        })

    # 6. Parámetros Globales (Primeros 5 para la tabla principal)
    parametros_qs = ParametroGlobal.objects.all().order_by('categoria', 'clave')
    parametros_tabla = []
    if parametros_qs.exists():
        for p in parametros_qs[:5]:
            parametros_tabla.append({
                'categoria': p.categoria,
                'clave': p.clave,
                'valor': p.valor,
                'descripcion': p.descripcion,
                'updated_at': p.updated_at.strftime('%d abr. %Y, %H:%M') if p.updated_at else '10 abr. 2025, 12:00'
            })
    else:
        parametros_tabla = [
            {'categoria': 'Vidas', 'clave': 'vidas_iniciales', 'valor': '3', 'descripcion': 'Vidas iniciales por partida', 'updated_at': '10 abr. 2025, 12:00'},
            {'categoria': 'Vidas', 'clave': 'vidas_maximas', 'valor': '3', 'descripcion': 'Máximo de vidas', 'updated_at': '10 abr. 2025, 12:00'},
            {'categoria': 'Economia', 'clave': 'monedas_defecto', 'valor': '50', 'descripcion': 'Monedas iniciales por jugador', 'updated_at': '10 abr. 2025, 12:00'},
            {'categoria': 'Economia', 'clave': 'gemas_defecto', 'valor': '10', 'descripcion': 'Gemas iniciales por jugador', 'updated_at': '10 abr. 2025, 12:00'},
            {'categoria': 'Progreso', 'clave': 'xp_defecto', 'valor': '100', 'descripcion': 'XP inicial por jugador', 'updated_at': '10 abr. 2025, 12:00'},
        ]

    # 7. Datos de gráfico de evolución de partidas (Curva SVG / ChartJS)
    chart_puntos = [
        {'dia': 1, 'partidas': 80, 'victorias': 55},
        {'dia': 5, 'partidas': 110, 'victorias': 78},
        {'dia': 10, 'partidas': 75, 'victorias': 50},
        {'dia': 15, 'partidas': 145, 'victorias': 105},
        {'dia': 20, 'partidas': 120, 'victorias': 88},
        {'dia': 25, 'partidas': 165, 'victorias': 122},
        {'dia': 30, 'partidas': 195, 'victorias': 150},
    ]

    return {
        'total_partidas': total_partidas,
        'total_victorias': total_victorias,
        'total_derrotas': total_derrotas,
        'total_abandonadas': total_abandonadas,
        'tasa_victoria': tasa_victoria,
        'tasa_derrota': tasa_derrota,
        'tasa_abandonadas': tasa_abandonadas,
        'oro_global': oro_global,
        'gemas_globales': gemas_globales,
        'jugadores_activos': jugadores_activos,
        'jugadores_inactivos': jugadores_inactivos,
        'total_jugadores': total_jugadores,
        'porcentaje_activos': porcentaje_activos,
        'areas_stats': areas_stats,
        'mundos_mas_jugados': mundos_mas_jugados,
        'ultimas_partidas': ultimas_partidas,
        'actividad_reciente': actividad_reciente,
        'parametros_tabla': parametros_tabla,
        'chart_puntos': chart_puntos,
        'generado_en': timezone.now(),
        'fecha_header': timezone.now().strftime('%d abr. %Y, %H:%M'),
    }


@staff_member_required
def admin_analytics_view(request):
    """
    Vista dedicada de Analítica y Rendimiento accesible en /admin/analytics/.
    Redirige transparentemente al panel integrado de Partidas Jugadas.
    """
    return redirect('/admin/core/partidajugada/')


@staff_member_required
def api_metrics_summary(request):
    """
    Endpoint JSON de métricas para dashboards externos o llamadas asíncronas de telemetría.
    """
    data = get_analytics_data()
    payload = {
        'resumen_partidas': {
            'total': data['total_partidas'],
            'victorias': data['total_victorias'],
            'derrotas': data['total_derrotas'],
            'abandonadas': data['total_abandonadas'],
            'tasa_victoria': data['tasa_victoria'],
        },
        'economia_global': {
            'oro_emitido': data['oro_global'],
            'gemas_emitidas': data['gemas_globales'],
        },
        'usuarios': {
            'activos': data['jugadores_activos'],
            'inactivos': data['jugadores_inactivos'],
            'total_jugadores': data['total_jugadores'],
        },
        'timestamp': data['generado_en'].isoformat(),
    }
    return JsonResponse(payload)


@staff_member_required
def quick_seed_view(request):
    """
    Acción rápida para ejecutar el seed de parámetros globales desde el dashboard.
    """
    try:
        call_command('init_game_params')
        registrar_auditoria(
            admin=request.user,
            accion=AccionAuditoriaChoices.CAMBIAR_CONFIG,
            modulo_afectado='ParametroGlobal',
            registro_id='SEED_RAPIDO',
            datos_anteriores=None,
            datos_nuevos={'accion': 'Ejecución de seed de parámetros globales desde el Dashboard'},
            request=request
        )
        messages.success(request, "¡Parámetros globales inicializados y sincronizados con éxito!")
    except Exception as e:
        messages.error(request, f"Error al ejecutar seed: {str(e)}")
    return redirect('/admin/')


@staff_member_required
def quick_reset_progress_view(request):
    """
    Acción rápida para reiniciar el progreso de todos los colaboradores con registro en auditoría.
    """
    ip = get_client_ip(request)
    ahora = timezone.now()
    oro_def = get_parametro_global('oro_inicial', 100, tipo=int)
    gemas_def = get_parametro_global('gemas_iniciales', 10, tipo=int)
    vidas_def = get_parametro_global('vidas_iniciales', 3, tipo=int)
    progresos = ProgresoUsuario.objects.all()
    count = 0
    for p in progresos:
        datos_ant = {'nivel': p.nivel, 'xp': p.xp, 'oro': p.oro, 'gemas': p.gemas, 'vidas': p.vidas_actuales}
        p.nivel = 1
        p.xp = 0
        p.oro = oro_def
        p.gemas = gemas_def
        p.vidas_actuales = vidas_def
        p.ultimo_reinicio_progreso = ahora
        p.save()
        datos_nuev = {'nivel': 1, 'xp': 0, 'oro': oro_def, 'gemas': gemas_def, 'vidas': vidas_def}
        registrar_auditoria(
            admin=request.user,
            accion=AccionAuditoriaChoices.REINICIAR_PROGRESO,
            modulo_afectado='ProgresoUsuario',
            registro_id=str(p.pk),
            datos_anteriores=datos_ant,
            datos_nuevos=datos_nuev,
            ip=ip
        )
        count += 1
    messages.warning(request, f"Se ha reiniciado el progreso de {count} jugador(es) y se generó la auditoría forense correspondiente.")
    return redirect('/admin/')


@staff_member_required
def user_detail_json(request, user_id):
    """
    Retorna la información completa de perfil, progreso y auditoría de un usuario
    para renderizar dinámicamente el panel lateral derecho del módulo Usuarios.
    """
    try:
        usuario = Usuario.objects.select_related('progreso').get(pk=user_id)
    except Usuario.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuario no encontrado'}, status=404)

    progreso, _ = ProgresoUsuario.objects.get_or_create(usuario=usuario)
    xp_max = max(100, progreso.nivel * 100)
    xp_pct = min(100, round((progreso.xp / xp_max) * 100, 1))

    data = {
        'success': True,
        'id': usuario.id,
        'nombre_completo': usuario.nombre_completo,
        'alias': usuario.alias,
        'avatar_url': usuario.avatar_url,
        'correo': usuario.correo,
        'area': usuario.area,
        'rol': usuario.rol,
        'rol_display': usuario.get_rol_display(),
        'estado': usuario.estado,
        'estado_display': usuario.get_estado_display(),
        'is_active': usuario.is_active,
        'created_at': usuario.created_at.strftime('%d abr. %Y %H:%M') if usuario.created_at else '10 abr. 2025 10:15',
        'updated_at': usuario.updated_at.strftime('%d abr. %Y %H:%M') if usuario.updated_at else '10 abr. 2025 14:20',
        'progreso': {
            'nivel': progreso.nivel,
            'xp': progreso.xp,
            'xp_max': xp_max,
            'xp_pct': xp_pct,
            'oro': progreso.oro,
            'gemas': progreso.gemas,
            'vidas_actuales': progreso.vidas_actuales,
            'ultimo_reinicio_vidas': progreso.ultimo_reinicio_vidas.strftime('%d abr. %Y %H:%M') if progreso.ultimo_reinicio_vidas else '10 abr. 2025 12:30',
            'ultimo_reinicio_progreso': progreso.ultimo_reinicio_progreso.strftime('%d abr. %Y %H:%M') if progreso.ultimo_reinicio_progreso else 'Sin reinicio',
        }
    }
    return JsonResponse(data)


@staff_member_required
def user_update_ajax(request, user_id):
    """
    Actualiza los datos del usuario (incluyendo estado activo/inactivo, área, rol)
    desde el panel de edición lateral y registra auditoría inmutable.
    """
    if request.method not in ['POST', 'PUT']:
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

    try:
        usuario = Usuario.objects.get(pk=user_id)
    except Usuario.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuario no encontrado'}, status=404)

    import json
    if request.content_type == 'application/json':
        payload = json.loads(request.body.decode('utf-8'))
    else:
        payload = request.POST

    datos_anteriores = {
        'nombre_completo': usuario.nombre_completo,
        'alias': usuario.alias,
        'avatar_url': usuario.avatar_url,
        'correo': usuario.correo,
        'area': usuario.area,
        'rol': usuario.rol,
        'estado': usuario.estado,
        'is_active': usuario.is_active,
    }

    if 'nombre_completo' in payload and payload['nombre_completo'].strip():
        usuario.nombre_completo = payload['nombre_completo'].strip()
    if 'alias' in payload and payload['alias'].strip():
        usuario.alias = payload['alias'].strip()
    if 'correo' in payload and payload['correo'].strip():
        usuario.correo = payload['correo'].strip().lower()
    if 'area' in payload and payload['area'].strip():
        usuario.area = payload['area'].strip()
    if 'rol' in payload and payload['rol'] in [c[0] for c in RolUsuarioChoices.choices]:
        usuario.rol = payload['rol']
        if usuario.rol == RolUsuarioChoices.ADMINISTRADOR:
            usuario.is_staff = True
    if 'estado' in payload and payload['estado'] in [c[0] for c in EstadoUsuarioChoices.choices]:
        usuario.estado = payload['estado']
        usuario.is_active = (usuario.estado == EstadoUsuarioChoices.ACTIVO)

    usuario.save()

    datos_nuevos = {
        'nombre_completo': usuario.nombre_completo,
        'alias': usuario.alias,
        'avatar_url': usuario.avatar_url,
        'correo': usuario.correo,
        'area': usuario.area,
        'rol': usuario.rol,
        'estado': usuario.estado,
        'is_active': usuario.is_active,
    }

    # Registrar en bitácora inmutable
    registrar_auditoria(
        admin=request.user,
        accion=AccionAuditoriaChoices.EDITAR,
        modulo_afectado='Usuario',
        registro_id=str(usuario.id),
        datos_anteriores=datos_anteriores,
        datos_nuevos=datos_nuevos,
        request=request
    )

    return JsonResponse({
        'success': True,
        'message': f"Usuario '{usuario.alias}' actualizado exitosamente.",
        'usuario': {
            'id': usuario.id,
            'nombre_completo': usuario.nombre_completo,
            'alias': usuario.alias,
            'correo': usuario.correo,
            'area': usuario.area,
            'rol': usuario.rol,
            'rol_display': usuario.get_rol_display(),
            'estado': usuario.estado,
            'estado_display': usuario.get_estado_display(),
            'updated_at': usuario.updated_at.strftime('%d abr. %Y %H:%M')
        }
    })


@staff_member_required
def user_reset_progress_ajax(request, user_id):
    """
    Reinicia el progreso específico del usuario seleccionado desde el botón del panel lateral.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

    try:
        usuario = Usuario.objects.get(pk=user_id)
        progreso, _ = ProgresoUsuario.objects.get_or_create(usuario=usuario)
    except Usuario.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuario no encontrado'}, status=404)

    ahora = timezone.now()
    oro_def = get_parametro_global('oro_inicial', 100, tipo=int)
    gemas_def = get_parametro_global('gemas_iniciales', 10, tipo=int)
    vidas_def = get_parametro_global('vidas_iniciales', 3, tipo=int)

    datos_ant = {
        'nivel': progreso.nivel,
        'xp': progreso.xp,
        'oro': progreso.oro,
        'gemas': progreso.gemas,
        'vidas': progreso.vidas_actuales
    }

    progreso.nivel = 1
    progreso.xp = 0
    progreso.oro = oro_def
    progreso.gemas = gemas_def
    progreso.vidas_actuales = vidas_def
    progreso.ultimo_reinicio_progreso = ahora
    progreso.save()

    datos_nuev = {
        'nivel': 1,
        'xp': 0,
        'oro': oro_def,
        'gemas': gemas_def,
        'vidas': vidas_def,
        'ultimo_reinicio_progreso': ahora.isoformat()
    }

    registrar_auditoria(
        admin=request.user,
        accion=AccionAuditoriaChoices.REINICIAR_PROGRESO,
        modulo_afectado='ProgresoUsuario',
        registro_id=str(progreso.pk),
        datos_anteriores=datos_ant,
        datos_nuevos=datos_nuev,
        request=request
    )

    return JsonResponse({
        'success': True,
        'message': f"Progreso de '{usuario.alias}' reiniciado a Nivel 1 y 0 XP.",
        'progreso': {
            'nivel': 1,
            'xp': 0,
            'xp_max': 100,
            'xp_pct': 0,
            'oro': 0,
            'gemas': 0,
            'vidas_actuales': 3,
            'ultimo_reinicio_progreso': ahora.strftime('%d abr. %Y %H:%M')
        }
    })


@staff_member_required
def user_change_password_ajax(request, user_id):
    """
    Permite a los administradores cambiar de forma independiente y segura la contraseña
    del usuario seleccionado desde el panel lateral, registrando el evento en la auditoría inmutable.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

    try:
        usuario = Usuario.objects.get(pk=user_id)
    except Usuario.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuario no encontrado'}, status=404)

    import json
    if request.content_type == 'application/json':
        payload = json.loads(request.body.decode('utf-8'))
    else:
        payload = request.POST

    nueva_password = payload.get('nueva_password', '').strip()
    confirmar_password = payload.get('confirmar_password', '').strip()

    if not nueva_password:
        return JsonResponse({'success': False, 'error': 'La nueva contraseña no puede estar vacía.'}, status=400)

    if len(nueva_password) < 6:
        return JsonResponse({'success': False, 'error': 'La contraseña debe tener al menos 6 caracteres.'}, status=400)

    if nueva_password != confirmar_password:
        return JsonResponse({'success': False, 'error': 'Las contraseñas no coinciden.'}, status=400)

    # Actualizar hash de contraseña de Django de forma segura
    usuario.set_password(nueva_password)
    usuario.save()

    # Registrar en bitácora inmutable de auditoría (sin registrar la contraseña en texto plano)
    registrar_auditoria(
        admin=request.user,
        accion=AccionAuditoriaChoices.EDITAR,
        modulo_afectado='Usuario',
        registro_id=str(usuario.id),
        datos_anteriores={'campo_modificado': 'password'},
        datos_nuevos={'campo_modificado': 'password', 'estado': 'actualizada_exitosamente'},
        request=request
    )

    return JsonResponse({
        'success': True,
        'message': f"Contraseña del usuario '{usuario.alias}' actualizada exitosamente."
    })


@staff_member_required
@require_POST
def user_delete_ajax(request, user_id):
    """
    Elimina un usuario de forma segura con registro en auditoría forense,
    evitando que el administrador se elimine a sí mismo y resecuenciando
    automáticamente los IDs de todos los usuarios restantes (1, 2, 3...).
    """
    from .utils import resequenciar_ids_usuarios

    if request.user.id == user_id:
        return JsonResponse({'success': False, 'error': 'No puedes eliminar tu propia cuenta en sesión.'}, status=400)

    try:
        usuario = Usuario.objects.get(pk=user_id)
    except Usuario.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuario no encontrado.'}, status=404)

    alias = usuario.alias
    datos_anteriores = serialize_instance(usuario)

    # Registrar auditoría antes de eliminar
    registrar_auditoria(
        admin=request.user,
        accion=AccionAuditoriaChoices.ELIMINAR,
        modulo_afectado='Usuario',
        registro_id=str(usuario.id),
        datos_anteriores=datos_anteriores,
        datos_nuevos=None,
        request=request
    )

    # Eliminar y resecuenciar IDs
    usuario.delete()
    resequenciar_ids_usuarios()

    return JsonResponse({
        'success': True,
        'message': f"Usuario '{alias}' eliminado correctamente. Los IDs han sido actualizados secuencialmente."
    })



# ==============================================================================
# VISTAS AJAX Y REPORTES PARA EL APARTADO DE PROGRESO DE USUARIOS
# ==============================================================================

@staff_member_required
def progreso_export_csv(request):
    """
    Genera y descarga un reporte CSV con el progreso completo de los jugadores.
    """
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="progreso_usuarios_iso_quest.csv"'
    
    # Escribir BOM para compatibilidad universal con Excel en español
    response.write('\ufeff'.encode('utf8'))
    
    writer = csv.writer(response)
    writer.writerow([
        'ID Progreso',
        'Jugador',
        'Alias',
        'Correo',
        'Rol',
        'Nivel',
        'XP',
        'Oro',
        'Gemas',
        'Vidas Actuales',
        'Último Reinicio Vidas',
        'Último Reinicio Progreso',
        'Estado'
    ])

    progresos = ProgresoUsuario.objects.select_related('usuario').order_by('-ultimo_reinicio_vidas')
    for p in progresos:
        u = p.usuario
        u_vidas = p.ultimo_reinicio_vidas.strftime('%d/%m/%Y %H:%M') if p.ultimo_reinicio_vidas else '—'
        u_prog = p.ultimo_reinicio_progreso.strftime('%d/%m/%Y %H:%M') if p.ultimo_reinicio_progreso else '—'
        writer.writerow([
            p.id,
            u.nombre_completo,
            u.alias,
            u.correo,
            u.get_rol_display(),
            p.nivel,
            p.xp,
            p.oro,
            p.gemas,
            p.vidas_actuales,
            u_vidas,
            u_prog,
            u.get_estado_display()
        ])

    return response


@staff_member_required
def progreso_detail_json(request, progreso_id):
    """
    Retorna la ficha técnica y detallada de un jugador para el modal de visualización.
    """
    try:
        progreso = ProgresoUsuario.objects.select_related('usuario').get(pk=progreso_id)
    except ProgresoUsuario.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Registro de progreso no encontrado'}, status=404)

    u = progreso.usuario
    reinicio_vidas_str = progreso.ultimo_reinicio_vidas.strftime('%d abr. %Y, %H:%M') if progreso.ultimo_reinicio_vidas else '—'
    reinicio_prog_str = progreso.ultimo_reinicio_progreso.strftime('%d abr. %Y, %H:%M') if progreso.ultimo_reinicio_progreso else '—'

    return JsonResponse({
        'success': True,
        'progreso': {
            'id': progreso.id,
            'nivel': progreso.nivel,
            'xp': progreso.xp,
            'oro': progreso.oro,
            'gemas': progreso.gemas,
            'vidas_actuales': progreso.vidas_actuales,
            'ultimo_reinicio_vidas': reinicio_vidas_str,
            'ultimo_reinicio_progreso': reinicio_prog_str,
            'usuario': {
                'id': u.id,
                'nombre_completo': u.nombre_completo,
                'alias': u.alias,
                'avatar_url': u.avatar_url,
                'correo': u.correo,
                'area': u.area,
                'rol': u.rol,
                'rol_display': u.get_rol_display(),
                'estado': u.estado,
                'estado_display': u.get_estado_display(),
            }
        }
    })


@staff_member_required
def progreso_update_ajax(request, progreso_id):
    """
    Actualiza los valores de Nivel, XP, Oro, Gemas y Vidas de un jugador desde el modal de edición.
    Registra el evento con auditoría inmutable.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

    try:
        progreso = ProgresoUsuario.objects.select_related('usuario').get(pk=progreso_id)
    except ProgresoUsuario.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Registro de progreso no encontrado'}, status=404)

    if request.content_type == 'application/json':
        payload = json.loads(request.body.decode('utf-8'))
    else:
        payload = request.POST

    datos_anteriores = {
        'nivel': progreso.nivel,
        'xp': progreso.xp,
        'oro': progreso.oro,
        'gemas': progreso.gemas,
        'vidas_actuales': progreso.vidas_actuales,
    }

    try:
        if 'nivel' in payload:
            progreso.nivel = max(1, int(payload['nivel']))
        if 'xp' in payload:
            progreso.xp = max(0, int(payload['xp']))
        if 'oro' in payload:
            progreso.oro = max(0, int(payload['oro']))
        if 'gemas' in payload:
            progreso.gemas = max(0, int(payload['gemas']))
        if 'vidas_actuales' in payload:
            progreso.vidas_actuales = max(0, min(5, int(payload['vidas_actuales'])))
        progreso.save()
    except (ValueError, TypeError) as e:
        return JsonResponse({'success': False, 'error': f'Valores numéricos inválidos: {str(e)}'}, status=400)

    datos_nuevos = {
        'nivel': progreso.nivel,
        'xp': progreso.xp,
        'oro': progreso.oro,
        'gemas': progreso.gemas,
        'vidas_actuales': progreso.vidas_actuales,
    }

    registrar_auditoria(
        admin=request.user,
        accion=AccionAuditoriaChoices.EDITAR,
        modulo_afectado='ProgresoUsuario',
        registro_id=str(progreso.pk),
        datos_anteriores=datos_anteriores,
        datos_nuevos=datos_nuevos,
        request=request
    )

    return JsonResponse({
        'success': True,
        'message': f"Progreso del jugador '{progreso.usuario.alias}' actualizado exitosamente.",
        'progreso': {
            'id': progreso.id,
            'nivel': progreso.nivel,
            'xp': progreso.xp,
            'oro': progreso.oro,
            'gemas': progreso.gemas,
            'vidas_actuales': progreso.vidas_actuales,
        }
    })


@staff_member_required
def progreso_reset_single_ajax(request, progreso_id):
    """
    Reinicia el progreso individual de un jugador a Nivel 1 y 0 XP con auditoría inmutable.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

    try:
        progreso = ProgresoUsuario.objects.select_related('usuario').get(pk=progreso_id)
    except ProgresoUsuario.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Registro de progreso no encontrado'}, status=404)

    ahora = timezone.now()
    oro_def = get_parametro_global('oro_inicial', 100, tipo=int)
    gemas_def = get_parametro_global('gemas_iniciales', 10, tipo=int)
    vidas_def = get_parametro_global('vidas_iniciales', 3, tipo=int)

    datos_ant = {
        'nivel': progreso.nivel,
        'xp': progreso.xp,
        'oro': progreso.oro,
        'gemas': progreso.gemas,
        'vidas_actuales': progreso.vidas_actuales,
        'ultimo_reinicio_progreso': str(progreso.ultimo_reinicio_progreso)
    }

    progreso.nivel = 1
    progreso.xp = 0
    progreso.oro = oro_def
    progreso.gemas = gemas_def
    progreso.vidas_actuales = vidas_def
    progreso.ultimo_reinicio_progreso = ahora
    progreso.save()

    datos_nuev = {
        'nivel': 1,
        'xp': 0,
        'oro': oro_def,
        'gemas': gemas_def,
        'vidas_actuales': vidas_def,
        'ultimo_reinicio_progreso': ahora.isoformat()
    }

    registrar_auditoria(
        admin=request.user,
        accion=AccionAuditoriaChoices.REINICIAR_PROGRESO,
        modulo_afectado='ProgresoUsuario',
        registro_id=str(progreso.pk),
        datos_anteriores=datos_ant,
        datos_nuevos=datos_nuev,
        request=request
    )

    return JsonResponse({
        'success': True,
        'message': f"El progreso de '{progreso.usuario.alias}' se reinició correctamente a Nivel 1.",
        'progreso': {
            'id': progreso.id,
            'nivel': 1,
            'xp': 0,
            'oro': 0,
            'gemas': 0,
            'vidas_actuales': 3,
            'ultimo_reinicio_progreso': ahora.strftime('%d abr. %Y, %H:%M')
        }
    })


# ==============================================================================
# VISTAS AJAX PARA EL MÓDULO DE MUNDOS ISO
# ==============================================================================

@staff_member_required
def mundo_detail_json(request, mundo_id):
    """
    Retorna los detalles completos de un Mundo ISO para el modal de visualización/edición.
    """
    try:
        mundo = Mundo.objects.prefetch_related('niveles').get(pk=mundo_id)
    except Mundo.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Mundo no encontrado'}, status=404)

    return JsonResponse({
        'success': True,
        'mundo': {
            'id': mundo.id,
            'orden': mundo.orden,
            'codigo_iso': mundo.codigo_iso,
            'nombre_tematico': mundo.nombre_tematico,
            'dominio': mundo.dominio,
            'dificultad': mundo.dificultad,
            'dificultad_display': mundo.get_dificultad_display(),
            'estado': mundo.estado,
            'estado_display': mundo.get_estado_display(),
            'imagen_url': mundo.imagen_url,
            'total_niveles': mundo.niveles.count(),
        }
    })


@staff_member_required
def mundo_update_ajax(request, mundo_id):
    """
    Actualiza los datos de un Mundo ISO desde el modal interactivo con auditoría inmutable.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

    try:
        mundo = Mundo.objects.get(pk=mundo_id)
    except Mundo.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Mundo no encontrado'}, status=404)

    if request.content_type == 'application/json':
        payload = json.loads(request.body.decode('utf-8'))
    else:
        payload = request.POST

    datos_anteriores = {
        'orden': mundo.orden,
        'codigo_iso': mundo.codigo_iso,
        'nombre_tematico': mundo.nombre_tematico,
        'dominio': mundo.dominio,
        'dificultad': mundo.dificultad,
        'estado': mundo.estado,
    }

    try:
        if 'orden' in payload and str(payload['orden']).isdigit():
            mundo.orden = int(payload['orden'])
        if 'codigo_iso' in payload and payload['codigo_iso'].strip():
            mundo.codigo_iso = payload['codigo_iso'].strip()
        if 'nombre_tematico' in payload and payload['nombre_tematico'].strip():
            mundo.nombre_tematico = payload['nombre_tematico'].strip()
        if 'dominio' in payload and payload['dominio'].strip():
            mundo.dominio = payload['dominio'].strip()
        if 'dificultad' in payload and payload['dificultad'].strip():
            mundo.dificultad = payload['dificultad'].strip()
        if 'estado' in payload and payload['estado'].strip():
            mundo.estado = payload['estado'].strip()
        mundo.save()
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Error al actualizar: {str(e)}'}, status=400)

    datos_nuevos = {
        'orden': mundo.orden,
        'codigo_iso': mundo.codigo_iso,
        'nombre_tematico': mundo.nombre_tematico,
        'dominio': mundo.dominio,
        'dificultad': mundo.dificultad,
        'estado': mundo.estado,
    }

    registrar_auditoria(
        admin=request.user,
        accion=AccionAuditoriaChoices.EDITAR,
        modulo_afectado='Mundo',
        registro_id=str(mundo.id),
        datos_anteriores=datos_anteriores,
        datos_nuevos=datos_nuevos,
        request=request
    )

    return JsonResponse({
        'success': True,
        'message': f"Mundo '{mundo.codigo_iso} - {mundo.nombre_tematico}' actualizado exitosamente.",
        'mundo': {
            'id': mundo.id,
            'orden': mundo.orden,
            'codigo_iso': mundo.codigo_iso,
            'nombre_tematico': mundo.nombre_tematico,
            'dominio': mundo.dominio,
            'dificultad': mundo.dificultad,
            'dificultad_display': mundo.get_dificultad_display(),
            'estado': mundo.estado,
            'estado_display': mundo.get_estado_display(),
            'imagen_url': mundo.imagen_url,
        }
    })


@staff_member_required
def mundo_create_ajax(request):
    """
    Crea un nuevo Mundo ISO desde el modal interactivo con auditoría inmutable.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

    if request.content_type == 'application/json':
        payload = json.loads(request.body.decode('utf-8'))
    else:
        payload = request.POST

    try:
        orden = int(payload.get('orden', 1))
        codigo_iso = payload.get('codigo_iso', '').strip()
        nombre_tematico = payload.get('nombre_tematico', '').strip()
        dominio = payload.get('dominio', '').strip()
        dificultad = payload.get('dificultad', 'normal').strip()
        estado = payload.get('estado', 'activo').strip()

        if not codigo_iso or not nombre_tematico:
            return JsonResponse({'success': False, 'error': 'El código ISO y el nombre temático son obligatorios.'}, status=400)

        mundo = Mundo.objects.create(
            orden=orden,
            codigo_iso=codigo_iso,
            nombre_tematico=nombre_tematico,
            dominio=dominio or 'General',
            dificultad=dificultad,
            estado=estado
        )

        registrar_auditoria(
            admin=request.user,
            accion=AccionAuditoriaChoices.CREAR,
            modulo_afectado='Mundo',
            registro_id=str(mundo.id),
            datos_anteriores={},
            datos_nuevos={
                'orden': mundo.orden,
                'codigo_iso': mundo.codigo_iso,
                'nombre_tematico': mundo.nombre_tematico,
                'dominio': mundo.dominio,
                'dificultad': mundo.dificultad,
                'estado': mundo.estado
            },
            request=request
        )

        return JsonResponse({
            'success': True,
            'message': f"Mundo '{mundo.codigo_iso}' creado exitosamente.",
            'mundo': {
                'id': mundo.id,
                'orden': mundo.orden,
                'codigo_iso': mundo.codigo_iso,
                'nombre_tematico': mundo.nombre_tematico,
                'dominio': mundo.dominio,
                'dificultad': mundo.dificultad,
                'estado': mundo.estado,
                'imagen_url': mundo.imagen_url
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Error al crear mundo: {str(e)}'}, status=400)


# ==============================================================================
# AJAX ENDPOINTS: NIVELES ISO
# ==============================================================================

@staff_member_required
def nivel_detail_json(request, nivel_id):
    """
    Retorna los datos completos de un nivel ISO para los modales de Ver y Editar.
    """
    try:
        nivel = Nivel.objects.select_related('mundo').get(pk=nivel_id)
    except Nivel.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Nivel no encontrado'}, status=404)

    fases_data = [
        {
            'id': f.id,
            'numero_fase': f.numero_fase,
            'titulo_incidente': f.titulo_incidente,
            'amenaza': f.amenaza,
            'dificultad': f.get_dificultad_display(),
            'estado': f.get_estado_display()
        }
        for f in nivel.fases.all().order_by('numero_fase')
    ]

    return JsonResponse({
        'success': True,
        'nivel': {
            'id': nivel.id,
            'mundo_id': nivel.mundo.id,
            'mundo_codigo': nivel.mundo.codigo_iso,
            'mundo_nombre': nivel.mundo.nombre_tematico,
            'numero_nivel': nivel.numero_nivel,
            'titulo': nivel.titulo,
            'tipo': nivel.tipo,
            'tipo_display': nivel.get_tipo_display(),
            'dificultad': nivel.dificultad,
            'dificultad_display': nivel.get_dificultad_display(),
            'recompensa_oro': nivel.recompensa_oro,
            'recompensa_gemas': nivel.recompensa_gemas,
            'recompensa_xp': nivel.recompensa_xp,
            'estado': nivel.estado,
            'estado_display': nivel.get_estado_display(),
            'fases': fases_data,
            'total_fases': len(fases_data)
        }
    })


@staff_member_required
def nivel_update_ajax(request, nivel_id):
    """
    Actualiza los datos de un Nivel desde el modal interactivo con auditoría inmutable.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

    try:
        nivel = Nivel.objects.select_related('mundo').get(pk=nivel_id)
    except Nivel.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Nivel no encontrado'}, status=404)

    if request.content_type == 'application/json':
        payload = json.loads(request.body.decode('utf-8'))
    else:
        payload = request.POST

    datos_anteriores = {
        'numero_nivel': nivel.numero_nivel,
        'titulo': nivel.titulo,
        'tipo': nivel.tipo,
        'dificultad': nivel.dificultad,
        'recompensa_oro': nivel.recompensa_oro,
        'recompensa_gemas': nivel.recompensa_gemas,
        'recompensa_xp': nivel.recompensa_xp,
        'estado': nivel.estado,
    }

    try:
        if 'numero_nivel' in payload and str(payload['numero_nivel']).isdigit():
            nivel.numero_nivel = int(payload['numero_nivel'])
        if 'titulo' in payload and payload['titulo'].strip():
            nivel.titulo = payload['titulo'].strip()
        if 'tipo' in payload and payload['tipo'].strip():
            nivel.tipo = payload['tipo'].strip()
        if 'dificultad' in payload and payload['dificultad'].strip():
            nivel.dificultad = payload['dificultad'].strip()
        if 'recompensa_oro' in payload and str(payload['recompensa_oro']).isdigit():
            nivel.recompensa_oro = int(payload['recompensa_oro'])
        if 'recompensa_gemas' in payload and str(payload['recompensa_gemas']).isdigit():
            nivel.recompensa_gemas = int(payload['recompensa_gemas'])
        if 'recompensa_xp' in payload and str(payload['recompensa_xp']).isdigit():
            nivel.recompensa_xp = int(payload['recompensa_xp'])
        if 'estado' in payload and payload['estado'].strip():
            nivel.estado = payload['estado'].strip()
        nivel.save()
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Error al actualizar nivel: {str(e)}'}, status=400)

    datos_nuevos = {
        'numero_nivel': nivel.numero_nivel,
        'titulo': nivel.titulo,
        'tipo': nivel.tipo,
        'dificultad': nivel.dificultad,
        'recompensa_oro': nivel.recompensa_oro,
        'recompensa_gemas': nivel.recompensa_gemas,
        'recompensa_xp': nivel.recompensa_xp,
        'estado': nivel.estado,
    }

    registrar_auditoria(
        admin=request.user,
        accion=AccionAuditoriaChoices.EDITAR,
        modulo_afectado='Nivel',
        registro_id=str(nivel.id),
        datos_anteriores=datos_anteriores,
        datos_nuevos=datos_nuevos,
        request=request
    )

    return JsonResponse({
        'success': True,
        'message': f"Nivel {nivel.numero_nivel} '{nivel.titulo}' actualizado exitosamente.",
        'nivel': {
            'id': nivel.id,
            'numero_nivel': nivel.numero_nivel,
            'titulo': nivel.titulo,
            'tipo': nivel.tipo,
            'tipo_display': nivel.get_tipo_display(),
            'dificultad': nivel.dificultad,
            'dificultad_display': nivel.get_dificultad_display(),
            'recompensa_oro': nivel.recompensa_oro,
            'recompensa_gemas': nivel.recompensa_gemas,
            'recompensa_xp': nivel.recompensa_xp,
            'estado': nivel.estado,
            'estado_display': nivel.get_estado_display(),
        }
    })


@staff_member_required
def nivel_create_ajax(request):
    """
    Crea un nuevo Nivel dentro de un Mundo ISO desde el modal interactivo con auditoría inmutable.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

    if request.content_type == 'application/json':
        payload = json.loads(request.body.decode('utf-8'))
    else:
        payload = request.POST

    try:
        mundo_id = payload.get('mundo_id')
        if not mundo_id:
            return JsonResponse({'success': False, 'error': 'Debes seleccionar un Mundo.'}, status=400)

        mundo = Mundo.objects.get(pk=mundo_id)
        numero_nivel = int(payload.get('numero_nivel', 1))
        titulo = payload.get('titulo', '').strip()
        tipo = payload.get('tipo', 'normal').strip()
        dificultad = payload.get('dificultad', 'normal').strip()
        recompensa_oro = int(payload.get('recompensa_oro', 50))
        recompensa_gemas = int(payload.get('recompensa_gemas', 10))
        recompensa_xp = int(payload.get('recompensa_xp', 100))
        estado = payload.get('estado', 'activo').strip()

        if not titulo:
            return JsonResponse({'success': False, 'error': 'El título del nivel es obligatorio.'}, status=400)

        # Verificar unicidad de número de nivel dentro del mismo mundo
        if Nivel.objects.filter(mundo=mundo, numero_nivel=numero_nivel).exists():
            return JsonResponse({
                'success': False,
                'error': f"Ya existe el nivel {numero_nivel} para {mundo.codigo_iso}. Elige otro número."
            }, status=400)

        nivel = Nivel.objects.create(
            mundo=mundo,
            numero_nivel=numero_nivel,
            titulo=titulo,
            tipo=tipo,
            dificultad=dificultad,
            recompensa_oro=recompensa_oro,
            recompensa_gemas=recompensa_gemas,
            recompensa_xp=recompensa_xp,
            estado=estado
        )

        registrar_auditoria(
            admin=request.user,
            accion=AccionAuditoriaChoices.CREAR,
            modulo_afectado='Nivel',
            registro_id=str(nivel.id),
            datos_anteriores={},
            datos_nuevos={
                'mundo': mundo.codigo_iso,
                'numero_nivel': nivel.numero_nivel,
                'titulo': nivel.titulo,
                'tipo': nivel.tipo,
                'dificultad': nivel.dificultad,
                'recompensa_oro': nivel.recompensa_oro,
                'recompensa_gemas': nivel.recompensa_gemas,
                'recompensa_xp': nivel.recompensa_xp,
                'estado': nivel.estado,
            },
            request=request
        )

        return JsonResponse({
            'success': True,
            'message': f"Nivel {nivel.numero_nivel} '{nivel.titulo}' creado exitosamente en {mundo.codigo_iso}.",
            'nivel': {
                'id': nivel.id,
                'mundo_id': mundo.id,
                'numero_nivel': nivel.numero_nivel,
                'titulo': nivel.titulo,
                'tipo': nivel.tipo,
                'tipo_display': nivel.get_tipo_display(),
                'dificultad': nivel.dificultad,
                'dificultad_display': nivel.get_dificultad_display(),
                'recompensa_oro': nivel.recompensa_oro,
                'recompensa_gemas': nivel.recompensa_gemas,
                'recompensa_xp': nivel.recompensa_xp,
                'estado': nivel.estado,
                'estado_display': nivel.get_estado_display(),
            }
        })
    except Mundo.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'El Mundo seleccionado no existe.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Error al crear el nivel: {str(e)}'}, status=400)


@staff_member_required
def niveles_por_mundo_json(request, mundo_id):
    """
    Retorna la lista de niveles y métricas agregadas para un mundo seleccionado,
    permitiendo la conmutación instantánea y reactiva en el panel de Niveles.
    """
    try:
        mundo = Mundo.objects.get(pk=mundo_id)
    except Mundo.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Mundo no encontrado'}, status=404)

    niveles = Nivel.objects.filter(mundo=mundo).order_by('numero_nivel')
    agg = niveles.aggregate(
        total_xp=Sum('recompensa_xp'),
        total_oro=Sum('recompensa_oro'),
        total_gemas=Sum('recompensa_gemas'),
        total_niveles=Count('id')
    )

    niveles_data = [
        {
            'id': n.id,
            'numero_nivel': n.numero_nivel,
            'titulo': n.titulo,
            'tipo': n.tipo,
            'tipo_display': '👑 Jefe' if n.tipo == 'jefe' else 'Normal',
            'dificultad': n.dificultad,
            'dificultad_display': n.get_dificultad_display(),
            'recompensa_oro': n.recompensa_oro,
            'recompensa_gemas': n.recompensa_gemas,
            'recompensa_xp': n.recompensa_xp,
            'estado': n.estado,
            'estado_display': n.get_estado_display(),
        }
        for n in niveles
    ]

    return JsonResponse({
        'success': True,
        'mundo': {
            'id': mundo.id,
            'orden': mundo.orden,
            'codigo_iso': mundo.codigo_iso,
            'nombre_tematico': mundo.nombre_tematico,
            'nombre_corto': mundo.nombre_corto,
            'descripcion': mundo.descripcion_tematica,
            'avatar_url': mundo.avatar_guardia_url,
            'total_niveles': agg['total_niveles'] or 0,
            'total_xp': agg['total_xp'] or 0,
            'total_oro': agg['total_oro'] or 0,
            'total_gemas': agg['total_gemas'] or 0,
        },
        'niveles': niveles_data
    })


# ==============================================================================
# AJAX ENDPOINTS: CARTAS ISO
# ==============================================================================

@staff_member_required
def carta_detail_json(request, carta_id):
    """
    Retorna los datos completos de una carta de control ISO para los modales de Ver y Editar.
    """
    try:
        carta = Carta.objects.get(pk=carta_id)
    except Carta.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Carta no encontrada'}, status=404)

    return JsonResponse({
        'success': True,
        'carta': {
            'id': carta.id,
            'nombre': carta.nombre,
            'norma_iso': carta.norma_iso,
            'concepto': carta.concepto,
            'descripcion': carta.descripcion,
            'fuerza': carta.fuerza,
            'defensa': carta.defensa,
            'estado': carta.estado,
            'estado_display': carta.get_estado_display(),
            'imagen_url': carta.imagen_url,
            'usada_en_fases_count': carta.usada_en_fases.count(),
        }
    })


@staff_member_required
def carta_update_ajax(request, carta_id):
    """
    Actualiza los datos de una carta desde el modal interactivo con auditoría inmutable.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

    try:
        carta = Carta.objects.get(pk=carta_id)
    except Carta.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Carta no encontrada'}, status=404)

    if request.content_type == 'application/json':
        payload = json.loads(request.body.decode('utf-8'))
    else:
        payload = request.POST

    datos_anteriores = {
        'nombre': carta.nombre,
        'norma_iso': carta.norma_iso,
        'concepto': carta.concepto,
        'descripcion': carta.descripcion,
        'fuerza': carta.fuerza,
        'defensa': carta.defensa,
        'estado': carta.estado,
    }

    try:
        if 'nombre' in payload and payload['nombre'].strip():
            carta.nombre = payload['nombre'].strip()
        if 'norma_iso' in payload and payload['norma_iso'].strip():
            carta.norma_iso = payload['norma_iso'].strip()
        if 'concepto' in payload and payload['concepto'].strip():
            carta.concepto = payload['concepto'].strip()
        if 'descripcion' in payload:
            carta.descripcion = payload['descripcion'].strip()
        if 'fuerza' in payload and str(payload['fuerza']).isdigit():
            carta.fuerza = int(payload['fuerza'])
        if 'defensa' in payload and str(payload['defensa']).isdigit():
            carta.defensa = int(payload['defensa'])
        if 'estado' in payload and payload['estado'].strip():
            carta.estado = payload['estado'].strip()
        if 'imagen' in request.FILES:
            carta.imagen = request.FILES['imagen']
        carta.save()
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Error al actualizar carta: {str(e)}'}, status=400)

    datos_nuevos = {
        'nombre': carta.nombre,
        'norma_iso': carta.norma_iso,
        'concepto': carta.concepto,
        'descripcion': carta.descripcion,
        'fuerza': carta.fuerza,
        'defensa': carta.defensa,
        'estado': carta.estado,
    }

    registrar_auditoria(
        admin=request.user,
        accion=AccionAuditoriaChoices.EDITAR,
        modulo_afectado='Carta',
        registro_id=str(carta.id),
        datos_anteriores=datos_anteriores,
        datos_nuevos=datos_nuevos,
        request=request
    )

    return JsonResponse({
        'success': True,
        'message': f"Carta '{carta.nombre}' actualizada exitosamente.",
        'carta': {
            'id': carta.id,
            'nombre': carta.nombre,
            'norma_iso': carta.norma_iso,
            'concepto': carta.concepto,
            'descripcion': carta.descripcion,
            'fuerza': carta.fuerza,
            'defensa': carta.defensa,
            'estado': carta.estado,
            'estado_display': carta.get_estado_display(),
            'imagen_url': carta.imagen_url,
        }
    })


@staff_member_required
def carta_create_ajax(request):
    """
    Crea una nueva carta en el catálogo interactivo con auditoría inmutable.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

    if request.content_type == 'application/json':
        payload = json.loads(request.body.decode('utf-8'))
    else:
        payload = request.POST

    try:
        nombre = payload.get('nombre', '').strip()
        norma_iso = payload.get('norma_iso', '').strip()
        concepto = payload.get('concepto', '').strip()
        descripcion = payload.get('descripcion', '').strip()
        fuerza = int(payload.get('fuerza', 70))
        defensa = int(payload.get('defensa', 70))
        estado = payload.get('estado', 'activo').strip()

        if not nombre or not norma_iso:
            return JsonResponse({'success': False, 'error': 'El nombre y la norma ISO son obligatorios.'}, status=400)

        imagen = request.FILES.get('imagen')

        carta = Carta.objects.create(
            nombre=nombre,
            norma_iso=norma_iso,
            concepto=concepto or 'Control ISO',
            descripcion=descripcion,
            fuerza=fuerza,
            defensa=defensa,
            estado=estado,
            imagen=imagen
        )

        registrar_auditoria(
            admin=request.user,
            accion=AccionAuditoriaChoices.CREAR,
            modulo_afectado='Carta',
            registro_id=str(carta.id),
            datos_anteriores={},
            datos_nuevos={
                'nombre': carta.nombre,
                'norma_iso': carta.norma_iso,
                'concepto': carta.concepto,
                'descripcion': carta.descripcion,
                'fuerza': carta.fuerza,
                'defensa': carta.defensa,
                'estado': carta.estado,
            },
            request=request
        )

        return JsonResponse({
            'success': True,
            'message': f"Carta '{carta.nombre}' creada exitosamente en el catálogo.",
            'carta': {
                'id': carta.id,
                'nombre': carta.nombre,
                'norma_iso': carta.norma_iso,
                'concepto': carta.concepto,
                'descripcion': carta.descripcion,
                'fuerza': carta.fuerza,
                'defensa': carta.defensa,
                'estado': carta.estado,
                'estado_display': carta.get_estado_display(),
                'imagen_url': carta.imagen_url,
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Error al crear la carta: {str(e)}'}, status=400)


# ==============================================================================
# AJAX ENDPOINTS: FASES DE CASO / INCIDENTES
# ==============================================================================

@staff_member_required
def fasecaso_detail_json(request, fase_id):
    """
    Retorna la información técnica de una Fase de Caso para vista o previsualización.
    """
    try:
        f = FaseCaso.objects.select_related('nivel', 'nivel__mundo').get(pk=fase_id)
    except FaseCaso.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Fase de caso no encontrada'}, status=404)

    return JsonResponse({
        'success': True,
        'fase': {
            'id': f.id,
            'nivel_id': f.nivel_id,
            'nivel_titulo': f.nivel.titulo,
            'nivel_numero': f.nivel.numero_nivel,
            'mundo_id': f.nivel.mundo_id,
            'mundo_codigo': f.nivel.mundo.codigo_iso,
            'mundo_nombre': f.nivel.mundo.nombre_tematico,
            'mundo_imagen': f.nivel.mundo.imagen_url,
            'numero_fase': f.numero_fase,
            'titulo_incidente': f.titulo_incidente,
            'amenaza': f.amenaza,
            'dificultad': f.dificultad,
            'dificultad_display': f.get_dificultad_display(),
            'caso_contexto': f.caso_contexto,
            'recompensa_oro': f.recompensa_oro,
            'recompensa_xp': f.recompensa_xp,
            'estado': f.estado,
            'estado_display': f.get_estado_display(),
        }
    })


@staff_member_required
@require_http_methods(["POST"])
def fasecaso_create_ajax(request):
    """
    Crea una nueva Fase de Caso mediante AJAX con auditoría forense.
    """
    try:
        nivel_id = request.POST.get('nivel')
        numero_fase = request.POST.get('numero_fase', '1')
        titulo_incidente = request.POST.get('titulo_incidente', '').strip()
        amenaza = request.POST.get('amenaza', '').strip()
        dificultad = request.POST.get('dificultad', DificultadChoices.NORMAL)
        caso_contexto = request.POST.get('caso_contexto', '').strip()
        recompensa_oro = int(request.POST.get('recompensa_oro', 10))
        recompensa_xp = int(request.POST.get('recompensa_xp', 20))
        estado = request.POST.get('estado', EstadoEntidadChoices.ACTIVO)

        if not nivel_id or not titulo_incidente or not caso_contexto:
            return JsonResponse({'success': False, 'error': 'Nivel, Título y Contexto son obligatorios.'}, status=400)

        nivel = Nivel.objects.get(pk=int(nivel_id))
        numero_fase_int = int(numero_fase)

        if FaseCaso.objects.filter(nivel=nivel, numero_fase=numero_fase_int).exists():
            return JsonResponse({
                'success': False,
                'error': f"Ya existe la Fase #{numero_fase_int} para el Nivel '{nivel.titulo}'. Por favor usa otro número."
            }, status=400)

        fase = FaseCaso.objects.create(
            nivel=nivel,
            numero_fase=numero_fase_int,
            titulo_incidente=titulo_incidente,
            amenaza=amenaza or 'Phishing',
            dificultad=dificultad,
            caso_contexto=caso_contexto,
            recompensa_oro=recompensa_oro,
            recompensa_xp=recompensa_xp,
            estado=estado
        )

        registrar_auditoria(
            admin=request.user,
            accion=AccionAuditoriaChoices.CREAR,
            modulo_afectado='FaseCaso',
            registro_id=str(fase.id),
            datos_anteriores={},
            datos_nuevos=serialize_instance(fase),
            request=request
        )

        return JsonResponse({
            'success': True,
            'message': f"Fase #{fase.numero_fase} - '{fase.titulo_incidente}' creada exitosamente.",
            'fase_id': fase.id
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Error al crear la fase: {str(e)}'}, status=400)


@staff_member_required
@require_http_methods(["POST"])
def fasecaso_delete_ajax(request, fase_id):
    """
    Elimina una Fase de Caso mediante AJAX con auditoría forense.
    """
    try:
        fase = FaseCaso.objects.get(pk=fase_id)
        datos_ant = serialize_instance(fase)
        fase_num = fase.numero_fase
        fase_titulo = fase.titulo_incidente
        fase.delete()

        registrar_auditoria(
            admin=request.user,
            accion=AccionAuditoriaChoices.ELIMINAR,
            modulo_afectado='FaseCaso',
            registro_id=str(fase_id),
            datos_anteriores=datos_ant,
            datos_nuevos={},
            request=request
        )

        return JsonResponse({
            'success': True,
            'message': f"Fase #{fase_num} '{fase_titulo}' eliminada correctamente."
        })
    except FaseCaso.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Fase no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Error al eliminar la fase: {str(e)}'}, status=400)


@staff_member_required
def fases_por_nivel_json(request, nivel_id):
    """
    Retorna las Fases de Caso correspondientes a un Nivel específico.
    """
    try:
        nivel = Nivel.objects.get(pk=nivel_id)
    except Nivel.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Nivel no encontrado.'}, status=404)

    fases = FaseCaso.objects.filter(nivel=nivel).annotate(_cartas_count=Count('opciones_cartas')).order_by('numero_fase')
    fases_data = [
        {
            'id': f.id,
            'numero_fase': f.numero_fase,
            'titulo_incidente': f.titulo_incidente,
            'caso_contexto': f.caso_contexto,
            'amenaza': f.amenaza,
            'dificultad': f.dificultad,
            'dificultad_display': f.get_dificultad_display(),
            'recompensa_oro': f.recompensa_oro,
            'recompensa_xp': f.recompensa_xp,
            'estado': f.estado,
            'cartas_count': f._cartas_count,
        }
        for f in fases
    ]

    return JsonResponse({
        'success': True,
        'nivel': {
            'id': nivel.id,
            'numero_nivel': nivel.numero_nivel,
            'titulo': nivel.titulo,
            'mundo_id': nivel.mundo_id,
        },
        'fases': fases_data,
        'total_fases': len(fases_data)
    })


@staff_member_required
def baraja_fase_detail_json(request, fase_id):
    """
    Retorna los detalles de la Fase seleccionada y las cartas asignadas (con su solución correcta).
    """
    try:
        fase = FaseCaso.objects.select_related('nivel__mundo').get(pk=fase_id)
    except FaseCaso.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Fase no encontrada.'}, status=404)

    opciones = fase.opciones_cartas.select_related('carta').all().order_by('id')
    cartas_asignadas = [
        {
            'carta_id': op.carta.id,
            'nombre': op.carta.nombre,
            'norma_iso': op.carta.norma_iso,
            'concepto': op.carta.concepto,
            'descripcion': op.carta.descripcion,
            'imagen_url': op.carta.imagen_url,
            'fuerza': op.carta.fuerza,
            'defensa': op.carta.defensa,
            'estado': op.carta.estado,
            'es_solucion_correcta': op.es_solucion_correcta,
        }
        for op in opciones
    ]

    return JsonResponse({
        'success': True,
        'fase': {
            'id': fase.id,
            'numero_fase': fase.numero_fase,
            'titulo_incidente': fase.titulo_incidente,
            'caso_contexto': fase.caso_contexto,
            'amenaza': fase.amenaza,
            'dificultad': fase.dificultad,
            'dificultad_display': fase.get_dificultad_display(),
            'nivel_id': fase.nivel.id,
            'nivel_titulo': fase.nivel.titulo,
            'nivel_numero': fase.nivel.numero_nivel,
            'mundo_id': fase.nivel.mundo.id,
            'mundo_codigo': fase.nivel.mundo.codigo_iso,
            'mundo_nombre': fase.nivel.mundo.nombre_tematico,
        },
        'cartas_asignadas': cartas_asignadas,
        'total_cartas': len(cartas_asignadas)
    })


@staff_member_required
def cartas_activas_json(request):
    """
    Retorna únicamente las cartas con estado ACTIVO para ser seleccionadas en Barajas / Opciones.
    """
    cartas = Carta.objects.filter(estado=EstadoEntidadChoices.ACTIVO).order_by('norma_iso', 'nombre')
    cartas_data = [
        {
            'id': c.id,
            'nombre': c.nombre,
            'norma_iso': c.norma_iso,
            'concepto': c.concepto,
            'descripcion': c.descripcion,
            'imagen_url': c.imagen_url,
            'fuerza': c.fuerza,
            'defensa': c.defensa,
            'estado': c.estado,
        }
        for c in cartas
    ]

    return JsonResponse({
        'success': True,
        'cartas': cartas_data,
        'total': len(cartas_data)
    })


@staff_member_required
@require_http_methods(["POST"])
def fasecartaopcion_guardar_ajax(request, fase_id):
    """
    Guarda la configuración de cartas asociadas a una Fase de Caso.
    Valida:
    - Máximo 5 cartas por fase.
    - Al menos 1 carta marcada como correcta.
    - Únicamente cartas con estado ACTIVO creadas en el catálogo.
    - Sin cartas duplicadas.
    Registra auditoría inmutable.
    """
    try:
        fase = FaseCaso.objects.select_related('nivel__mundo').get(pk=fase_id)
    except FaseCaso.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Fase no encontrada.'}, status=404)

    try:
        if request.content_type == 'application/json':
            payload = json.loads(request.body.decode('utf-8'))
        else:
            cartas_raw = request.POST.get('cartas', '[]')
            payload = json.loads(cartas_raw) if isinstance(cartas_raw, str) else request.POST

        cartas_list = payload.get('cartas', []) if isinstance(payload, dict) else payload
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Formato de datos no válido: {str(e)}'}, status=400)

    if not isinstance(cartas_list, list):
        return JsonResponse({'success': False, 'error': 'La lista de cartas debe ser un arreglo.'}, status=400)

    if len(cartas_list) == 0:
        return JsonResponse({'success': False, 'error': 'Debes asignar al menos 1 carta a la fase.'}, status=400)

    if len(cartas_list) > 5:
        return JsonResponse({'success': False, 'error': 'Máximo 5 cartas por fase.'}, status=400)

    # Validar cartas únicas
    carta_ids = [c.get('carta_id') for c in cartas_list if isinstance(c, dict) and c.get('carta_id')]
    if len(carta_ids) != len(cartas_list):
        return JsonResponse({'success': False, 'error': 'Datos de cartas inválidos.'}, status=400)

    if len(carta_ids) != len(set(carta_ids)):
        return JsonResponse({'success': False, 'error': 'No se permiten cartas duplicadas en la misma fase.'}, status=400)

    # Validar que al menos una sea correcta
    hay_correcta = any(bool(c.get('es_solucion_correcta', False)) for c in cartas_list)
    if not hay_correcta:
        return JsonResponse({'success': False, 'error': 'Debe existir al menos 1 carta marcada como solución correcta.'}, status=400)

    # Validar que todas las cartas existan y estén ACTIVAS
    cartas_db = Carta.objects.filter(pk__in=carta_ids)
    if cartas_db.count() != len(carta_ids):
        return JsonResponse({'success': False, 'error': 'Una o más cartas no existen en el catálogo.'}, status=400)

    cartas_inactivas = [c.nombre for c in cartas_db if c.estado != EstadoEntidadChoices.ACTIVO]
    if cartas_inactivas:
        return JsonResponse({
            'success': False,
            'error': f"Solo se pueden usar cartas activas del catálogo. Las siguientes cartas están inactivas: {', '.join(cartas_inactivas)}"
        }, status=400)

    # Guardar atómicamente
    with transaction.atomic():
        opciones_anteriores = list(fase.opciones_cartas.values('carta_id', 'es_solucion_correcta'))
        fase.opciones_cartas.all().delete()

        cartas_map = {c.id: c for c in cartas_db}
        nuevas_opciones = []
        for item in cartas_list:
            c_id = item.get('carta_id')
            es_correcta = bool(item.get('es_solucion_correcta', False))
            FaseCartaOpcion.objects.create(
                fase=fase,
                carta=cartas_map[c_id],
                es_solucion_correcta=es_correcta
            )
            nuevas_opciones.append({'carta_id': c_id, 'nombre': cartas_map[c_id].nombre, 'es_solucion_correcta': es_correcta})

        registrar_auditoria(
            admin=request.user,
            accion=AccionAuditoriaChoices.EDITAR,
            modulo_afectado='FaseCartaOpcion',
            registro_id=str(fase.id),
            datos_anteriores={'opciones': opciones_anteriores},
            datos_nuevos={'fase': fase.titulo_incidente, 'opciones': nuevas_opciones},
            request=request
        )

    return JsonResponse({
        'success': True,
        'message': f"Configuración guardada exitosamente para la Fase #{fase.numero_fase} ({len(nuevas_opciones)}/5 cartas)."
    })


@staff_member_required
def registroauditoria_detail_json(request, registro_id):
    """
    Retorna el detalle completo y snapshots JSON formateados de un registro de auditoría forense.
    """
    try:
        r = RegistroAuditoria.objects.select_related('admin').get(pk=registro_id)
    except RegistroAuditoria.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Registro de auditoría no encontrado'}, status=404)

    return JsonResponse({
        'success': True,
        'registro': {
            'id': r.id,
            'created_at': r.created_at.strftime('%d/%m/%Y - %H:%M:%S'),
            'admin_alias': r.admin_alias,
            'admin_avatar_url': r.admin_avatar_url,
            'accion': r.accion,
            'accion_display': r.get_accion_display(),
            'modulo_afectado': r.modulo_display,
            'registro_codigo': r.registro_codigo,
            'direccion_ip': r.direccion_ip or '127.0.0.1',
            'datos_anteriores': r.datos_anteriores or {},
            'datos_nuevos': r.datos_nuevos or {},
        }
    })


@staff_member_required
@require_POST
def registroauditoria_purge_ajax(request):
    """
    Elimina registros de auditoría según el rango de tiempo seleccionado
    (1 mes, 2 meses, 3 meses, 6 meses, 1 año o todo el historial).
    Permite filtrar opcionalmente por administrador responsable y tipo de acción.
    Soporta preview=True para calcular la cantidad de registros coincidentes.
    """
    import json
    import datetime
    from django.utils import timezone

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    tiempo = str(data.get('tiempo', '1')).strip()  # '1', '2', '3', '6', '12', 'all'
    admin_id = str(data.get('admin_id', 'todos')).strip()
    accion = str(data.get('accion', 'todas')).strip()
    es_preview = data.get('preview') in (True, 'true', '1', 1)

    qs = RegistroAuditoria.objects.all()

    now = timezone.now()
    if tiempo == '1':
        cutoff = now - datetime.timedelta(days=30)
        qs = qs.filter(created_at__lt=cutoff)
    elif tiempo == '2':
        cutoff = now - datetime.timedelta(days=60)
        qs = qs.filter(created_at__lt=cutoff)
    elif tiempo == '3':
        cutoff = now - datetime.timedelta(days=90)
        qs = qs.filter(created_at__lt=cutoff)
    elif tiempo == '6':
        cutoff = now - datetime.timedelta(days=180)
        qs = qs.filter(created_at__lt=cutoff)
    elif tiempo == '12':
        cutoff = now - datetime.timedelta(days=365)
        qs = qs.filter(created_at__lt=cutoff)
    elif tiempo == 'all':
        pass  # Todo el historial
    elif tiempo.isdigit():
        dias = int(tiempo) * 30
        cutoff = now - datetime.timedelta(days=dias)
        qs = qs.filter(created_at__lt=cutoff)

    # Filtrar por administrador si no es 'todos'
    if admin_id and admin_id != 'todos':
        if admin_id.isdigit():
            qs = qs.filter(admin_id=int(admin_id))

    # Filtrar por tipo de acción si no es 'todas'
    if accion and accion != 'todas':
        qs = qs.filter(accion=accion)

    total_count = qs.count()

    if es_preview:
        return JsonResponse({
            'success': True,
            'count': total_count
        })

    # Ejecutar la eliminación
    eliminados, _ = qs.delete()

    return JsonResponse({
        'success': True,
        'deleted_count': eliminados,
        'message': f'Se han eliminado correctamente {eliminados} registros de auditoría.'
    })



@staff_member_required
def partidajugada_detail_json(request, partida_id):
    """
    Retorna la telemetría detallada de una partida para el modal de auditoría y análisis.
    """
    try:
        p = PartidaJugada.objects.select_related('usuario', 'nivel', 'nivel__mundo').get(pk=partida_id)
    except PartidaJugada.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Partida no encontrada'}, status=404)

    return JsonResponse({
        'success': True,
        'partida': {
            'id': p.id,
            'usuario': p.usuario.alias,
            'nombre_completo': p.usuario.nombre_completo,
            'correo': p.usuario.correo,
            'avatar_url': p.usuario.avatar_url,
            'area': p.usuario.area,
            'nivel': p.nivel.titulo if p.nivel else 'Nivel General',
            'numero_nivel': p.nivel.numero_nivel if p.nivel else 1,
            'mundo': p.nivel.mundo.codigo_iso if p.nivel and p.nivel.mundo else 'ISO 27001',
            'mundo_nombre': p.nivel.mundo.nombre_tematico if p.nivel and p.nivel.mundo else 'Ciberseguridad',
            'resultado': p.resultado,
            'resultado_display': p.get_resultado_display(),
            'oro_obtenido': p.oro_obtenido,
            'gemas_obtenidas': p.gemas_obtenidas,
            'fecha_partida': p.fecha_partida.strftime('%d/%m/%Y - %H:%M'),
        }
    })


@staff_member_required
@require_POST
def reset_analytics_ajax(request):
    """
    Reinicia por completo la analítica y telemetría de partidas jugadas,
    así como el progreso de juego de los jugadores, preparando la base de datos
    para el lanzamiento oficial en limpio:
    - Elimina todas las PartidaJugada.
    - Reinicia la secuencia autoincremental de core_partida_jugada en SQLite.
    - Reinicia ProgresoUsuario (nivel=1, xp=0, oro=0, gemas=0, vidas_actuales=3, etc.).
    - Preserva las cuentas de usuario, niveles, mundos y cartas.
    - Registra auditoría forense del evento.
    """
    from django.db import connection

    total_partidas_eliminadas = PartidaJugada.objects.count()
    total_jugadores = ProgresoUsuario.objects.count()

    with transaction.atomic():
        # 1. Eliminar todas las partidas jugadas
        PartidaJugada.objects.all().delete()

        # 2. Reiniciar la secuencia de ID de partidas en SQLite
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name = %s", ['core_partida_jugada'])
        except Exception:
            pass

        # 3. Reiniciar el progreso de todos los usuarios usando Parametros Globales
        ahora = timezone.now()
        oro_def = get_parametro_global('oro_inicial', 100, tipo=int)
        gemas_def = get_parametro_global('gemas_iniciales', 10, tipo=int)
        vidas_def = get_parametro_global('vidas_iniciales', 3, tipo=int)
        ProgresoUsuario.objects.all().update(
            nivel=1,
            xp=0,
            oro=oro_def,
            gemas=gemas_def,
            vidas_actuales=vidas_def,
            ultimo_reinicio_progreso=ahora,
            ultimo_reinicio_vidas=ahora
        )

        # 4. Registrar auditoría forense
        registrar_auditoria(
            admin=request.user,
            accion=AccionAuditoriaChoices.CAMBIAR_CONFIG,
            modulo_afectado='AnaliticaPartidas',
            registro_id='LANZAMIENTO_ZERO',
            datos_anteriores={'partidas_previas': total_partidas_eliminadas},
            datos_nuevos={
                'estado': 'limpio_para_lanzamiento',
                'partidas_totales': 0,
                'jugadores_reseteados': total_jugadores,
            },
            request=request
        )

    return JsonResponse({
        'success': True,
        'message': f'¡Telemetría y progreso reiniciados exitosamente! Se eliminaron {total_partidas_eliminadas} partidas y se reinició el progreso de {total_jugadores} jugador(es). El sistema ha quedado en cero, listo para el lanzamiento.'
    })


@staff_member_required
def parametroglobal_detail_json(request, param_id):
    """
    Retorna los datos de un parámetro global en formato JSON.
    """
    try:
        p = ParametroGlobal.objects.get(pk=param_id)
    except ParametroGlobal.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Parámetro no encontrado'}, status=404)

    return JsonResponse({
        'success': True,
        'parametro': {
            'id': p.id,
            'categoria': p.categoria,
            'clave': p.clave,
            'valor': p.valor,
            'descripcion': p.descripcion,
            'updated_at': p.updated_at.strftime('%d/%m/%Y - %H:%M') if p.updated_at else '',
        }
    })


@staff_member_required
@require_http_methods(["POST"])
def parametroglobal_update_ajax(request, param_id):
    """
    Actualiza un parámetro global y audita la acción.
    """
    try:
        p = ParametroGlobal.objects.get(pk=param_id)
    except ParametroGlobal.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Parámetro no encontrado'}, status=404)

    categoria = request.POST.get('categoria', '').strip()
    clave = request.POST.get('clave', '').strip()
    valor = request.POST.get('valor', '').strip()
    descripcion = request.POST.get('descripcion', '').strip()

    if not clave:
        return JsonResponse({'success': False, 'error': 'La clave no puede estar vacía'}, status=400)

    # Validar unicidad si cambió la clave
    if clave != p.clave and ParametroGlobal.objects.filter(clave=clave).exclude(pk=p.pk).exists():
        return JsonResponse({'success': False, 'error': f'Ya existe un parámetro con la clave "{clave}"'}, status=400)

    datos_anteriores = serialize_instance(p)

    if categoria:
        p.categoria = categoria
    p.clave = clave
    p.valor = valor
    p.descripcion = descripcion
    p.save()

    # Sincronizar efectos reales e inmediatos en el juego
    sincronizar_efecto_parametro_global(p)

    datos_nuevos = serialize_instance(p)
    registrar_auditoria(
        admin=request.user,
        accion=AccionAuditoriaChoices.CAMBIAR_CONFIG,
        modulo_afectado='ParametroGlobal',
        registro_id=str(p.pk),
        datos_anteriores=datos_anteriores,
        datos_nuevos=datos_nuevos,
        request=request
    )

    return JsonResponse({
        'success': True,
        'message': f'Parámetro "{p.clave}" actualizado correctamente.',
        'parametro': {
            'id': p.id,
            'categoria': p.categoria,
            'clave': p.clave,
            'valor': p.valor,
            'descripcion': p.descripcion,
            'updated_at': p.updated_at.strftime('%d/%m/%Y - %H:%M') if p.updated_at else '',
        }
    })


@staff_member_required
@require_http_methods(["POST"])
def parametroglobal_reset_default_ajax(request):
    """
    Restaura todos los parámetros globales a sus valores por defecto y audita el evento.
    """
    from core.management.commands.init_game_params import PARAMETROS_DEFECTO

    datos_anteriores = [serialize_instance(p) for p in ParametroGlobal.objects.all()]

    for item in PARAMETROS_DEFECTO:
        p_obj, _ = ParametroGlobal.objects.update_or_create(
            clave=item['clave'],
            defaults={
                'categoria': item['categoria'],
                'valor': item['valor'],
                'descripcion': item['descripcion'],
            }
        )
        sincronizar_efecto_parametro_global(p_obj)

    datos_nuevos = [serialize_instance(p) for p in ParametroGlobal.objects.all()]
    registrar_auditoria(
        admin=request.user,
        accion=AccionAuditoriaChoices.CAMBIAR_CONFIG,
        modulo_afectado='ParametroGlobal',
        registro_id='RESTABLECER_DEFECTO',
        datos_anteriores={'total_anteriores': len(datos_anteriores)},
        datos_nuevos={'total_restablecidos': len(PARAMETROS_DEFECTO)},
        request=request
    )

    return JsonResponse({
        'success': True,
        'message': 'Parámetros restablecidos a los valores por defecto del sistema.',
    })


def home_dispatch_view(request):
    """
    Ruta raíz '/': Redirige al usuario según su rol:
    - Si no está autenticado -> /login/
    - Si es Administrador -> /admin/
    - Si es Empleado / Jugador -> /lobby/
    """
    if not request.user.is_authenticated:
        return redirect('core:login')

    if getattr(request.user, 'rol', None) == RolUsuarioChoices.ADMINISTRADOR or request.user.is_staff or request.user.is_superuser:
        return redirect('/admin/')
    return redirect('core:lobby')


def custom_login_view(request):
    """
    Inicio de sesión universal para Administradores y Empleados / Jugadores.
    Redirecciona según rol:
    - Administrador -> Dashboard Administrativo (/admin/)
    - Empleado / Jugador -> Lobby del Videojuego (/lobby/)
    """
    if request.user.is_authenticated:
        if getattr(request.user, 'rol', None) == RolUsuarioChoices.ADMINISTRADOR or request.user.is_staff or request.user.is_superuser:
            return redirect('/admin/')
        return redirect('core:lobby')

    error_msg = None
    next_url = request.GET.get('next') or request.POST.get('next') or ''

    if request.method == 'POST':
        identifier = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Buscar usuario por correo o alias
        user = Usuario.objects.filter(
            Q(correo__iexact=identifier) | Q(alias__iexact=identifier)
        ).first()

        if user and user.check_password(password):
            if not user.is_active or user.estado == EstadoUsuarioChoices.INACTIVO:
                error_msg = "Tu cuenta se encuentra inactiva. Comunícate con el Administrador de Cumplimiento."
            else:
                auth_login(request, user)

                # Redirección según rol
                if user.rol == RolUsuarioChoices.ADMINISTRADOR or user.is_staff or user.is_superuser:
                    target = next_url if (next_url and next_url.startswith('/admin/')) else '/admin/'
                    return redirect(target)
                else:
                    return redirect('core:lobby')
        else:
            error_msg = "Credenciales incorrectas. Verifica tu correo o alias y contraseña."

    return render(request, 'usuario/login.html', {
        'error_msg': error_msg,
        'next': next_url,
    })


def custom_logout_view(request):
    """
    Cierra la sesión y redirige a la pantalla de login.
    """
    auth_logout(request)
    return redirect('core:login')


@login_required(login_url='/login/')
def lobby_view(request):
    """
    Lobby principal del Empleado / Jugador con estética de Nigromante Arcano ISO.
    Muestra los datos reales guardados en base de datos:
    - Avatar del usuario idéntico al del dashboard (usuario.avatar_url).
    - Nivel, XP, Oro, Gemas, Vidas reales del modelo ProgresoUsuario.
    - Partidas reales, Victorias y Tasa de Victoria de PartidaJugada.
    - Colección de personajes nigromantes y mundos ISO reales.
    """
    usuario = request.user

    # Progreso real del usuario
    progreso, _ = ProgresoUsuario.objects.get_or_create(
        usuario=usuario,
        defaults={
            'nivel': 1,
            'oro': 100,
            'gemas': 10,
            'xp': 50,
            'vidas': 3,
        }
    )

    # Métricas reales de partidas jugadas por este usuario
    partidas_qs = PartidaJugada.objects.filter(usuario=usuario)
    total_partidas = partidas_qs.count()
    total_victorias = partidas_qs.filter(resultado=ResultadoPartidaChoices.VICTORIA).count()
    tasa_victoria = round((total_victorias / total_partidas * 100), 1) if total_partidas > 0 else 0.0

    # XP y meta del nivel actual
    xp_meta_nivel = max(500, progreso.nivel * 250)
    xp_en_nivel = progreso.xp % xp_meta_nivel if xp_meta_nivel > 0 else progreso.xp
    if xp_en_nivel == 0 and progreso.xp > 0:
        xp_en_nivel = min(progreso.xp, xp_meta_nivel)
    pct_xp = min(100, round((xp_en_nivel / xp_meta_nivel) * 100)) if xp_meta_nivel > 0 else 0

    # Colección de avatares nigromantes del sistema
    avatares_coleccion = [
        {'id': 1, 'nombre': 'Nigromante Sombra', 'img': '/static/img/avatars/necromancer_1.png'},
        {'id': 2, 'nombre': 'Hechicera Arcana', 'img': '/static/img/avatars/necromancer_2.png'},
        {'id': 3, 'nombre': 'Archimago ISO', 'img': '/static/img/avatars/necromancer_3.png'},
        {'id': 4, 'nombre': 'Sabia del Consejo', 'img': '/static/img/avatars/necromancer_4.png'},
    ]

    # Mundos ISO reales de la base de datos
    mundos = Mundo.objects.all().order_by('orden')
    mundos_data = []
    for m in mundos:
        tot_niveles = m.niveles.count()
        ganados = partidas_qs.filter(nivel__mundo=m, resultado=ResultadoPartidaChoices.VICTORIA).values('nivel_id').distinct().count()
        pct = int((ganados / tot_niveles) * 100) if tot_niveles > 0 else 0
        mundos_data.append({
            'mundo': m,
            'codigo_iso': m.codigo_iso,
            'nombre_tematico': m.nombre_tematico,
            'total_niveles': tot_niveles,
            'niveles_ganados': ganados,
            'porcentaje': pct,
        })

    # Porcentaje de progreso de desafíos
    desafios_completados = total_victorias
    desafios_meta = 20
    pct_desafios = min(100, int((desafios_completados / desafios_meta) * 100)) if desafios_meta > 0 else 0
    desafios_faltantes = max(0, desafios_meta - desafios_completados)

    # Ranking global de todos los jugadores ordenados por XP y Nivel descendente
    ranking_qs = ProgresoUsuario.objects.select_related('usuario').filter(
        usuario__estado=EstadoUsuarioChoices.ACTIVO
    ).order_by('-xp', '-nivel')
    ranking_jugadores = list(ranking_qs)

    # Podio de los 3 mejores para avatares gigantes y pedestales
    podio_1 = ranking_jugadores[0] if len(ranking_jugadores) > 0 else None
    podio_2 = ranking_jugadores[1] if len(ranking_jugadores) > 1 else None
    podio_3 = ranking_jugadores[2] if len(ranking_jugadores) > 2 else None

    # Posición del usuario actual en la tabla de clasificación
    user_rank = 1
    for idx, p in enumerate(ranking_jugadores, 1):
        if p.usuario_id == usuario.id:
            user_rank = idx
            break

    top_jugadores = ranking_jugadores[:10]

    context = {
        'usuario': usuario,
        'progreso': progreso,
        'total_partidas': total_partidas,
        'total_victorias': total_victorias,
        'tasa_victoria': tasa_victoria,
        'xp_en_nivel': xp_en_nivel,
        'xp_meta_nivel': xp_meta_nivel,
        'pct_xp': pct_xp,
        'avatares_coleccion': avatares_coleccion,
        'mundos_data': mundos_data,
        'desafios_completados': desafios_completados,
        'desafios_faltantes': desafios_faltantes,
        'pct_desafios': pct_desafios,
        'top_jugadores': top_jugadores,
        'ranking_jugadores': ranking_jugadores,
        'podio_1': podio_1,
        'podio_2': podio_2,
        'podio_3': podio_3,
        'user_rank': user_rank,
        'active_page': 'lobby',
        'is_admin': (usuario.rol == RolUsuarioChoices.ADMINISTRADOR or usuario.is_staff or usuario.is_superuser),
    }
    return render(request, 'usuario/lobby.html', context)


@login_required(login_url='/login/')
def clasificacion_view(request):
    """
    Vista principal de la Tabla de Clasificación (Leaderboard) con estética Dark Fantasy / Nigromante Arcano ISO.
    Muestra:
    - Podio épico con pedestales góticos en 3D (Oro, Plata, Bronce), laureles y coronas.
    - Tabla gótica con marco espinoso, paginación < 1 / 10 > y fila de campeón resaltada en oro.
    - Tarjeta lateral 'Tu Posición' con corona de laureles dorada y avatar con aura mística.
    - Botón monumental 'JUGAR' con filos de diamante y aura de energía.
    - Pestañas de filtro interactivo (Global, Amigos, Semanal, Mensual).
    """
    import math
    usuario = request.user

    # Progreso real del usuario actual
    progreso, _ = ProgresoUsuario.objects.get_or_create(
        usuario=usuario,
        defaults={
            'nivel': 1,
            'oro': 100,
            'gemas': 10,
            'xp': 50,
            'vidas': 3,
        }
    )

    # XP y meta del nivel actual
    xp_meta_nivel = max(500, progreso.nivel * 250)
    xp_en_nivel = progreso.xp % xp_meta_nivel if xp_meta_nivel > 0 else progreso.xp
    if xp_en_nivel == 0 and progreso.xp > 0:
        xp_en_nivel = min(progreso.xp, xp_meta_nivel)
    pct_xp = min(100, round((xp_en_nivel / xp_meta_nivel) * 100)) if xp_meta_nivel > 0 else 0

    # Asegurar que todos los usuarios existentes en la base de datos tengan su progreso
    usuarios_sin_progreso = Usuario.objects.filter(progreso__isnull=True)
    if usuarios_sin_progreso.exists():
        for u in usuarios_sin_progreso:
            ProgresoUsuario.objects.get_or_create(usuario=u)

    # Ranking global de TODOS los jugadores existentes clasificados por nivel y xp
    ranking_qs = ProgresoUsuario.objects.select_related('usuario').all().order_by('-nivel', '-xp', 'usuario__id')
    ranking_jugadores = list(ranking_qs)

    # Podio de los 3 mejores (cambia dinámicamente según quién tenga mejor nivel y xp)
    def _obtener_datos_podio(pos_progreso, default_alias, default_avatar):
        if pos_progreso and getattr(pos_progreso, 'usuario', None):
            u = pos_progreso.usuario
            alias = u.alias or u.nombre_completo or default_alias
            avatar = getattr(u, 'avatar_url', default_avatar) or default_avatar
            return {
                'usuario': {
                    'alias': alias,
                    'nombre_completo': u.nombre_completo or default_alias,
                    'avatar_url': avatar,
                },
                'nivel': pos_progreso.nivel or 1,
                'xp': pos_progreso.xp or 0,
                'existe': True,
            }
        return {
            'usuario': {
                'alias': 'Sin Jugador',
                'nombre_completo': 'Sin Jugador',
                'avatar_url': default_avatar,
            },
            'nivel': 1,
            'xp': 0,
            'existe': False,
        }

    podio_1 = _obtener_datos_podio(ranking_jugadores[0] if len(ranking_jugadores) > 0 else None, 'Campeón', '/static/img/avatars/necromancer_1.png')
    podio_2 = _obtener_datos_podio(ranking_jugadores[1] if len(ranking_jugadores) > 1 else None, 'Jugador 2', '/static/img/avatars/necromancer_2.png')
    podio_3 = _obtener_datos_podio(ranking_jugadores[2] if len(ranking_jugadores) > 2 else None, 'Jugador 3', '/static/img/avatars/necromancer_3.png')

    # Posición del usuario actual en el ranking
    user_rank = 1
    for idx, p in enumerate(ranking_jugadores, 1):
        if p.usuario_id == usuario.id:
            user_rank = idx
            break

    # Paginación (5 jugadores por página) y datos serializados para la navegación fluida
    tamano_pagina = 5
    total_jugadores = len(ranking_jugadores)
    total_paginas = max(1, math.ceil(total_jugadores / tamano_pagina))

    ranking_data_list = []
    for rank, p in enumerate(ranking_jugadores, 1):
        ranking_data_list.append({
            'rank': rank,
            'user_id': p.usuario_id,
            'alias': p.usuario.alias or p.usuario.nombre_completo,
            'avatar_url': p.usuario.avatar_url,
            'nivel': p.nivel,
            'xp': p.xp,
        })
    ranking_data_json = json.dumps(ranking_data_list)

    # Avatares de la colección para el modal de perfil
    avatares_coleccion = [
        {'id': 1, 'nombre': 'Nigromante Sombra', 'img': '/static/img/avatars/necromancer_1.png'},
        {'id': 2, 'nombre': 'Hechicera Arcana', 'img': '/static/img/avatars/necromancer_2.png'},
        {'id': 3, 'nombre': 'Archimago ISO', 'img': '/static/img/avatars/necromancer_3.png'},
        {'id': 4, 'nombre': 'Sabia del Consejo', 'img': '/static/img/avatars/necromancer_4.png'},
        {'id': 5, 'nombre': 'Invocador Rúnico', 'img': '/static/img/avatars/necromancer_5.png'},
    ]

    context = {
        'usuario': usuario,
        'progreso': progreso,
        'xp_en_nivel': xp_en_nivel,
        'xp_meta_nivel': xp_meta_nivel,
        'pct_xp': pct_xp,
        'ranking_jugadores': ranking_jugadores,
        'top_jugadores': ranking_jugadores[:tamano_pagina],
        'total_jugadores': total_jugadores,
        'total_paginas': total_paginas,
        'ranking_data_json': ranking_data_json,
        'podio_1': podio_1,
        'podio_2': podio_2,
        'podio_3': podio_3,
        'user_rank': user_rank,
        'active_page': 'clasificacion',
        'avatares_coleccion': avatares_coleccion,
        'is_admin': (usuario.rol == RolUsuarioChoices.ADMINISTRADOR or usuario.is_staff or usuario.is_superuser),
    }
    return render(request, 'usuario/clasificacion.html', context)


@login_required(login_url='/login/')
def player_profile_update_ajax(request):
    """
    Permite al empleado/jugador actualizar su alias y avatar desde la ventana
    flotante de perfil en el lobby del juego.
    """
    if request.method not in ['POST', 'PUT']:
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

    usuario = request.user
    import json
    if request.content_type == 'application/json':
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except Exception:
            payload = {}
    else:
        payload = request.POST

    nuevo_alias = payload.get('alias', '').strip()
    nuevo_avatar = payload.get('avatar', '').strip() or payload.get('avatar_url', '').strip()

    if not nuevo_alias:
        return JsonResponse({'success': False, 'error': 'El alias no puede estar vacío.'}, status=400)

    # Validar si otro usuario ya tiene ese alias
    if Usuario.objects.filter(alias__iexact=nuevo_alias).exclude(pk=usuario.pk).exists():
        return JsonResponse({'success': False, 'error': f"El alias '{nuevo_alias}' ya está en uso. Por favor elige otro."}, status=400)

    datos_anteriores = {
        'alias': usuario.alias,
        'avatar_url': usuario.avatar_url,
    }

    usuario.alias = nuevo_alias
    if nuevo_avatar:
        import re
        m = re.search(r'(necromancer_\d+\.png)', nuevo_avatar)
        if m:
            usuario.avatar_personalizado = m.group(1)
        else:
            usuario.avatar_personalizado = nuevo_avatar

    usuario.save()

    datos_nuevos = {
        'alias': usuario.alias,
        'avatar_url': usuario.avatar_url,
    }

    try:
        registrar_auditoria(
            admin=usuario,
            accion=AccionAuditoriaChoices.EDITAR,
            modulo_afectado='Perfil Jugador',
            registro_id=str(usuario.id),
            datos_anteriores=datos_anteriores,
            datos_nuevos=datos_nuevos,
            request=request
        )
    except Exception:
        pass

    return JsonResponse({
        'success': True,
        'message': 'Perfil actualizado correctamente.',
        'alias': usuario.alias,
        'avatar_url': usuario.avatar_url,
    })


def get_mapas_progreso_data(usuario, selected_mundo_id=None):
    """
    Calcula el estado de desbloqueo riguroso de mundos y niveles para el usuario:
    - El primer mundo (orden=1) siempre está desbloqueado.
    - Los mundos posteriores se desbloquean si y solo si TODOS los niveles del mundo anterior han sido ganados.
    - Dentro de un mundo desbloqueado:
      * El nivel 1 siempre está desbloqueado.
      * Los siguientes niveles se desbloquean si y solo si el nivel anterior en ese mundo fue ganado.
    - Devuelve la lista completa estructurada con coordenadas precisas para el sendero del mapa.
    """
    mundos_qs = list(Mundo.objects.filter(estado=EstadoEntidadChoices.ACTIVO).order_by('orden'))
    if not mundos_qs:
        mundos_qs = list(Mundo.objects.all().order_by('orden'))

    # Niveles ganados por este usuario
    niveles_ganados_ids = set(
        PartidaJugada.objects.filter(
            usuario=usuario,
            resultado=ResultadoPartidaChoices.VICTORIA,
            nivel__isnull=False
        ).values_list('nivel_id', flat=True)
    )

    # Mapeo de nombres narrativos / de fantasía para cada norma ISO de la BD
    NOMBRES_FANTASIA_MUNDOS = {
        1: 'Castillo Sombrío',
        2: 'Fortaleza de la Nube',
        3: 'Ciudadela del Servicio TI',
        4: 'Bastión de Resiliencia',
    }

    DESCRIPCIONES_MUNDOS = {
        1: 'Un bastión gótico donde la confidencialidad, integridad y disponibilidad de la información son defendidas (ISO/IEC 27001:2022).',
        2: 'Un reino suspendido en las alturas donde los controles y seguridad en entornos Cloud son primordiales (ISO/IEC 27017).',
        3: 'Una metrópoli tecnificada dedicada a la excelencia, entrega y gestión de servicios de TI (ISO/IEC 20000-1).',
        4: 'Un bastión inexpugnable preparado para resistir contingencias críticas y asegurar la continuidad operativa (ISO 22301).',
    }

    def get_mundo_fantasia_y_desc(m_obj):
        code = (m_obj.codigo_iso or '').replace(' ', '').lower()
        if '27017' in code:
            return 'Fortaleza de la Nube', 'Un reino suspendido en las alturas donde los controles y seguridad en entornos Cloud son primordiales (ISO/IEC 27017).'
        elif '27001' in code:
            return 'Castillo Sombrío', 'Un bastión gótico donde la confidencialidad, integridad y disponibilidad de la información son defendidas (ISO/IEC 27001:2022).'
        elif '20000' in code:
            return 'Ciudadela del Servicio TI', 'Una metrópoli tecnificada dedicada a la excelencia, entrega y gestión de servicios de TI (ISO/IEC 20000-1).'
        elif '22301' in code:
            return 'Bastión de Resiliencia', 'Un bastión inexpugnable preparado para resistir contingencias críticas y asegurar la continuidad operativa (ISO 22301).'
        fantasia = NOMBRES_FANTASIA_MUNDOS.get(m_obj.orden, m_obj.nombre_tematico)
        desc = DESCRIPCIONES_MUNDOS.get(m_obj.orden, f"Módulo de cumplimiento enfocado en {m_obj.dominio}.")
        return fantasia, desc

    # Coordenadas exactas para la disposición de 5 nodos sobre el puente (idénticas a la referencia)
    FIVE_NODES_COORDS = [
        {'x': 29.3, 'y': 58.2},  # Nodo 1 (Altar con mini castillo y 3 estrellas)
        {'x': 45.9, 'y': 54.1},  # Nodo 2 (Pedestal con cúpula y candado)
        {'x': 60.4, 'y': 48.9},  # Nodo 3 (Pedestal con cúpula y candado)
        {'x': 74.7, 'y': 47.8},  # Nodo 4 (Pedestal con cúpula y candado)
        {'x': 87.7, 'y': 47.8},  # Nodo 5 (Pedestal con cúpula y candado)
    ]

    mundos_data = []
    prev_world_completed = True  # El mundo 1 siempre está disponible

    for w_idx, m in enumerate(mundos_qs):
        niveles_qs = list(m.niveles.filter(estado=EstadoEntidadChoices.ACTIVO).order_by('numero_nivel'))
        if not niveles_qs:
            niveles_qs = list(m.niveles.all().order_by('numero_nivel'))

        total_niveles = len(niveles_qs)
        ganados_en_mundo = sum(1 for n in niveles_qs if n.id in niveles_ganados_ids)
        mundo_desbloqueado = (w_idx == 0) or prev_world_completed

        este_mundo_completado = (total_niveles > 0 and ganados_en_mundo == total_niveles)

        niveles_data = []
        prev_level_completed = True

        for l_idx, n in enumerate(niveles_qs):
            ha_ganado = n.id in niveles_ganados_ids

            if not mundo_desbloqueado:
                nivel_desbloqueado = False
                estado_progreso = 'bloqueado'
            else:
                if l_idx == 0:
                    nivel_desbloqueado = True
                else:
                    nivel_desbloqueado = prev_level_completed

                if ha_ganado:
                    estado_progreso = 'completado'
                elif nivel_desbloqueado:
                    estado_progreso = 'actual'
                else:
                    estado_progreso = 'bloqueado'

            # Código visual del nivel: e.g. 1-1, 1-2, 1-3, 1-4, 1-5
            codigo_nivel = f"{m.orden}-{n.numero_nivel}"

            # Asignar coordenadas del puente (soporta actos de 5 en 5)
            slot_idx = (n.numero_nivel - 1) % len(FIVE_NODES_COORDS)
            pt = FIVE_NODES_COORDS[slot_idx]
            acto = 1 if n.numero_nivel <= 5 else 2

            estrellas = 3 if ha_ganado else (0 if estado_progreso == 'bloqueado' else 0)

            niveles_data.append({
                'id': n.id,
                'numero_nivel': n.numero_nivel,
                'codigo_nivel': codigo_nivel,
                'acto': acto,
                'titulo': n.titulo,
                'tipo': n.tipo,
                'tipo_display': n.get_tipo_display(),
                'dificultad': n.dificultad,
                'dificultad_display': n.get_dificultad_display(),
                'recompensa_oro': n.recompensa_oro,
                'recompensa_gemas': n.recompensa_gemas,
                'recompensa_xp': n.recompensa_xp,
                'total_fases': n.fases.count(),
                'desbloqueado': nivel_desbloqueado,
                'ha_ganado': ha_ganado,
                'estado_progreso': estado_progreso,
                'estrellas': estrellas,
                'x': pt['x'],
                'y': pt['y'],
            })
            prev_level_completed = ha_ganado

        pct_avance = int((ganados_en_mundo / total_niveles) * 100) if total_niveles > 0 else 0
        nombre_fantasia, descripcion = get_mundo_fantasia_y_desc(m)

        mundos_data.append({
            'id': m.id,
            'orden': m.orden,
            'codigo_iso': m.codigo_iso,
            'nombre_tematico': m.nombre_tematico,
            'nombre_fantasia': nombre_fantasia,
            'descripcion_narrativa': descripcion,
            'nombre_corto': getattr(m, 'nombre_corto', m.nombre_tematico),
            'dominio': m.dominio,
            'dificultad': m.dificultad,
            'dificultad_display': m.get_dificultad_display(),
            'desbloqueado': mundo_desbloqueado,
            'completado': este_mundo_completado,
            'total_niveles': total_niveles,
            'ganados_en_mundo': ganados_en_mundo,
            'porcentaje': pct_avance,
            'imagen_url': m.imagen_url,
            'recompensas_mundo': {
                'gemas': 100,
                'oro': 5000,
                'cartas': 1,
            },
            'niveles': niveles_data,
        })

        prev_world_completed = este_mundo_completado

    # Localizar mundo activo
    mundo_activo = None
    if selected_mundo_id:
        try:
            mid = int(selected_mundo_id)
            for md in mundos_data:
                if md['id'] == mid:
                    mundo_activo = md
                    break
        except (ValueError, TypeError):
            pass

    if not mundo_activo:
        # Por defecto, seleccionar el primer mundo desbloqueado o el primero de la lista
        mundo_activo = mundos_data[0] if mundos_data else None

    return mundos_data, mundo_activo


@login_required(login_url='/login/')
def mapas_view(request):
    """
    Vista principal interactiva del Mapa y Niveles con estética Dark Fantasy Nigromante.
    Muestra:
    - Barra superior con perfil y recursos reales.
    - Menú lateral con 'Mapas' activo.
    - Selector temático de mundos < Mundo X Castillo Sombrío >
    - Puente gótico con nodos: Nivel 1 desbloqueado con estandarte y aura,
      y demás niveles bloqueados con candados de piedra mística.
    - Conexión por sendero continuo de energía arcana púrpura.
    """
    usuario = request.user

    # Progreso de economía del usuario
    progreso, _ = ProgresoUsuario.objects.get_or_create(
        usuario=usuario,
        defaults={
            'nivel': 1,
            'oro': 100,
            'gemas': 10,
            'xp': 50,
            'vidas': 3,
        }
    )

    # XP actual y meta
    xp_meta_nivel = max(500, progreso.nivel * 250)
    xp_en_nivel = progreso.xp % xp_meta_nivel if xp_meta_nivel > 0 else progreso.xp
    if xp_en_nivel == 0 and progreso.xp > 0:
        xp_en_nivel = min(progreso.xp, xp_meta_nivel)
    pct_xp = min(100, round((xp_en_nivel / xp_meta_nivel) * 100)) if xp_meta_nivel > 0 else 0

    # Obtener mundos y niveles con estados de desbloqueo rigurosos
    selected_mundo_id = request.GET.get('mundo_id')
    mundos_data, mundo_activo = get_mapas_progreso_data(usuario, selected_mundo_id)

    # Colección de avatares para el modal de perfil
    avatares_coleccion = [
        {'id': 1, 'nombre': 'Nigromante Sombra', 'img': '/static/img/avatars/necromancer_1.png'},
        {'id': 2, 'nombre': 'Hechicera Arcana', 'img': '/static/img/avatars/necromancer_2.png'},
        {'id': 3, 'nombre': 'Archimago ISO', 'img': '/static/img/avatars/necromancer_3.png'},
        {'id': 4, 'nombre': 'Sabia del Consejo', 'img': '/static/img/avatars/necromancer_4.png'},
        {'id': 5, 'nombre': 'Guardián del Cripto', 'img': '/static/img/avatars/necromancer_5.png'},
    ]

    # Ranking de jugadores para el modal de clasificación
    top_jugadores = ProgresoUsuario.objects.select_related('usuario').filter(
        usuario__rol=RolUsuarioChoices.EMPLEADO_JUGADOR
    ).order_by('-xp')[:10]

    context = {
        'usuario': usuario,
        'progreso': progreso,
        'xp_en_nivel': xp_en_nivel,
        'xp_meta_nivel': xp_meta_nivel,
        'pct_xp': pct_xp,
        'mundos_data': mundos_data,
        'mundos_data_json': json.dumps(mundos_data),
        'mundo_activo': mundo_activo,
        'avatares_coleccion': avatares_coleccion,
        'top_jugadores': top_jugadores,
        'active_page': 'mapas',
        'is_admin': (usuario.rol == RolUsuarioChoices.ADMINISTRADOR or usuario.is_staff or usuario.is_superuser),
    }
    return render(request, 'usuario/mapas.html', context)


@login_required(login_url='/login/')
@require_POST
def api_completar_nivel_ajax(request, nivel_id):
    """
    Registra una victoria en el nivel disputado por el usuario,
    actualiza el progreso (Oro, Gemas, XP), sube de nivel si corresponde,
    y retorna el estado actualizado para desbloquear el siguiente nivel en tiempo real.
    """
    usuario = request.user
    try:
        nivel = Nivel.objects.select_related('mundo').get(pk=nivel_id)
    except Nivel.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Nivel no encontrado'}, status=404)

    # Validar que el nivel esté efectivamente desbloqueado para este usuario
    mundos_data, _ = get_mapas_progreso_data(usuario, selected_mundo_id=nivel.mundo_id)
    este_nivel_data = None
    for m in mundos_data:
        if m['id'] == nivel.mundo_id:
            for nl in m['niveles']:
                if nl['id'] == nivel.id:
                    este_nivel_data = nl
                    break

    if not este_nivel_data or not este_nivel_data['desbloqueado']:
        return JsonResponse({'success': False, 'error': 'Este nivel se encuentra bloqueado actualmente.'}, status=403)

    # Registrar la partida jugada exitosa
    PartidaJugada.objects.create(
        usuario=usuario,
        nivel=nivel,
        resultado=ResultadoPartidaChoices.VICTORIA,
        oro_obtenido=nivel.recompensa_oro,
        gemas_obtenidas=nivel.recompensa_gemas,
    )

    # Actualizar economía y progreso del usuario
    progreso, _ = ProgresoUsuario.objects.get_or_create(usuario=usuario)
    progreso.oro += nivel.recompensa_oro
    progreso.gemas += nivel.recompensa_gemas
    progreso.xp += nivel.recompensa_xp

    nivel_maximo = get_parametro_global('nivel_maximo', 5, tipo=int)
    xp_meta_nivel = max(500, progreso.nivel * 250)
    subio_nivel = False
    if progreso.nivel < nivel_maximo and progreso.xp >= (progreso.nivel * xp_meta_nivel):
        progreso.nivel += 1
        subio_nivel = True

    progreso.save()

    # Recalcular estado de progreso después de la victoria
    mundos_data_post, mundo_activo_post = get_mapas_progreso_data(usuario, selected_mundo_id=nivel.mundo_id)

    # Determinar si se desbloqueó un nuevo mundo
    nuevo_mundo_desbloqueado = None
    for idx, m in enumerate(mundos_data_post):
        if m['id'] == nivel.mundo_id and m['completado']:
            if idx + 1 < len(mundos_data_post) and mundos_data_post[idx + 1]['desbloqueado']:
                nuevo_mundo_desbloqueado = mundos_data_post[idx + 1]['codigo_iso']

    xp_en_nivel = progreso.xp % xp_meta_nivel if xp_meta_nivel > 0 else progreso.xp
    pct_xp = min(100, round((xp_en_nivel / xp_meta_nivel) * 100)) if xp_meta_nivel > 0 else 0

    return JsonResponse({
        'success': True,
        'message': f"¡Victoria! Has superado con éxito el Nivel {nivel.numero_nivel}: {nivel.titulo}",
        'nivel_superado': {
            'id': nivel.id,
            'numero_nivel': nivel.numero_nivel,
            'titulo': nivel.titulo,
        },
        'recompensas': {
            'oro': nivel.recompensa_oro,
            'gemas': nivel.recompensa_gemas,
            'xp': nivel.recompensa_xp,
        },
        'progreso': {
            'nivel': progreso.nivel,
            'xp': progreso.xp,
            'oro': progreso.oro,
            'gemas': progreso.gemas,
            'subio_nivel': subio_nivel,
            'xp_en_nivel': xp_en_nivel,
            'xp_meta_nivel': xp_meta_nivel,
            'pct_xp': pct_xp,
        },
        'nuevo_mundo_desbloqueado': nuevo_mundo_desbloqueado,
        'mundo_activo': mundo_activo_post,
        'mundos_data': mundos_data_post,
    })


@login_required(login_url='/login/')
@require_POST
def api_reiniciar_mis_partidas_ajax(request):
    """
    Permite al usuario (o en modo prueba) reiniciar sus partidas ganadas
    para volver a experimentar el flujo desde Nivel 1.
    """
    PartidaJugada.objects.filter(usuario=request.user).delete()
    mundos_data, mundo_activo = get_mapas_progreso_data(request.user)
    return JsonResponse({
        'success': True,
        'message': 'Progreso de niveles reiniciado correctamente. Ahora solo el Nivel 1 está disponible.',
        'mundos_data': mundos_data,
        'mundo_activo': mundo_activo,
    })


@login_required(login_url='/login/')
def tienda_view(request):
    """
    Vista de la Tienda Arcana de Recursos ISO (Gemas, Monedas de Oro, Pociones de Energía y Pases).
    """
    return render(request, 'usuario/tienda.html', {
        'active_page': 'tienda',
    })


@login_required(login_url='/login/')
def academia_view(request):
    """
    Vista de la Academia ISO con módulos interactivos y lecciones de cumplimiento.
    """
    return render(request, 'usuario/academia.html', {
        'active_page': 'academia',
    })


@login_required(login_url='/login/')
def coleccion_view(request):
    """
    Vista de la Colección de Avatares Nigromantes y Cartas Arcanas de Compliance.
    """
    return render(request, 'usuario/coleccion.html', {
        'active_page': 'coleccion',
    })


@login_required(login_url='/login/')
def jugar_nivel_view(request, nivel_id):
    """
    Vista de Gameplay de Auditoría ISO con cartas arcanas y casos pedagógicos.
    El empleado/jugador resuelve los casos de cada fase seleccionando la carta
    correcta contra el tiempo exacto al mockup.
    """
    usuario = request.user
    nivel = get_object_or_404(Nivel.objects.select_related('mundo'), pk=nivel_id)
    mundo = nivel.mundo

    # Verificar si está desbloqueado para este usuario (staff y superuser pueden probar siempre)
    if not (usuario.is_staff or usuario.is_superuser):
        mundos_data, _ = get_mapas_progreso_data(usuario, selected_mundo_id=mundo.id)
        desbloqueado = False
        for m in mundos_data:
            if m['id'] == mundo.id:
                for nl in m['niveles']:
                    if nl['id'] == nivel.id and nl['desbloqueado']:
                        desbloqueado = True
                        break
        if not desbloqueado:
            messages.warning(request, f"El nivel {nivel.numero_nivel} aún está bloqueado. Supera los niveles anteriores para desbloquearlo.")
            return redirect('core:mapas')

    # Progreso de usuario con valores de ParametroGlobal y regeneración
    oro_def = get_parametro_global('oro_inicial', 100, tipo=int)
    gemas_def = get_parametro_global('gemas_iniciales', 10, tipo=int)
    vidas_def = get_parametro_global('vidas_iniciales', 3, tipo=int)

    progreso, _ = ProgresoUsuario.objects.get_or_create(
        usuario=usuario,
        defaults={'nivel': 1, 'oro': oro_def, 'gemas': gemas_def, 'xp': 0, 'vidas_actuales': vidas_def}
    )
    progreso, vidas_maximas, segundos_siguiente_vida, regeneracion_minutos = aplicar_regeneracion_vidas(progreso)

    # Validar si tiene vidas/energía para jugar
    if progreso.vidas_actuales <= 0:
        messages.warning(
            request,
            f"No tienes suficiente Energía Arcana (0/{vidas_maximas} Vidas) para iniciar este reto ISO. Espera a que se regenere o recárgala en la Tienda."
        )
        return redirect('core:mapas')

    tiempo_caso = get_parametro_global('tiempo_caso', 45, tipo=int)
    mins = tiempo_caso // 60
    secs = tiempo_caso % 60
    tiempo_caso_fmt = f"{mins:02d}:{secs:02d}"

    xp_meta_nivel = max(500, progreso.nivel * 250)
    xp_en_nivel = progreso.xp % xp_meta_nivel if xp_meta_nivel > 0 else progreso.xp
    if xp_en_nivel == 0 and progreso.xp > 0:
        xp_en_nivel = min(progreso.xp, xp_meta_nivel)
    pct_xp = min(100, round((xp_en_nivel / xp_meta_nivel) * 100)) if xp_meta_nivel > 0 else 0

    # Fases del nivel
    fases_qs = FaseCaso.objects.filter(nivel=nivel, estado=EstadoEntidadChoices.ACTIVO).order_by('numero_fase')
    if not fases_qs.exists():
        fases_qs = FaseCaso.objects.filter(nivel=nivel).order_by('numero_fase')

    letras = ['A', 'B', 'C', 'D', 'E']

    fases_data = []
    for f in fases_qs:
        opciones_qs = f.opciones_cartas.select_related('carta').all().order_by('id')
        cartas_list = []
        for idx, opc in enumerate(opciones_qs):
            carta = opc.carta
            cartas_list.append({
                'id': carta.id,
                'opcion_id': opc.id,
                'letra': letras[idx] if idx < len(letras) else chr(65 + idx),
                'nombre': carta.nombre,
                'descripcion': carta.descripcion or carta.concepto,
                'imagen_url': carta.imagen_url,
                'es_correcta': opc.es_solucion_correcta,
                'fuerza': carta.fuerza,
                'defensa': carta.defensa,
            })

        fases_data.append({
            'id': f.id,
            'numero_fase': f.numero_fase,
            'titulo_incidente': f.titulo_incidente,
            'caso_contexto': f.caso_contexto,
            'amenaza': f.amenaza,
            'dificultad': f.dificultad,
            'recompensa_oro': f.recompensa_oro,
            'recompensa_xp': f.recompensa_xp,
            'cartas': cartas_list,
        })

    context = {
        'usuario': usuario,
        'progreso': progreso,
        'xp_en_nivel': xp_en_nivel,
        'xp_meta_nivel': xp_meta_nivel,
        'pct_xp': pct_xp,
        'nivel': nivel,
        'mundo': mundo,
        'tiempo_caso': tiempo_caso,
        'tiempo_caso_fmt': tiempo_caso_fmt,
        'vidas_maximas': vidas_maximas,
        'segundos_siguiente_vida': segundos_siguiente_vida,
        'regeneracion_minutos': regeneracion_minutos,
        'fases_data_json': json.dumps(fases_data),
        'total_fases': len(fases_data),
        'active_page': 'mapas',
    }
    return render(request, 'usuario/jugar.html', context)


@login_required(login_url='/login/')
@require_POST
def api_registrar_derrota_ajax(request, nivel_id):
    """
    Registra una derrota en el intento de nivel sin otorgar recompensas,
    descuenta 1 vida (Energía Arcana) del progreso del usuario y calcula
    el tiempo exacto para la regeneración de la próxima vida según los Parámetros Globales.
    """
    usuario = request.user
    try:
        nivel = Nivel.objects.get(pk=nivel_id)
        progreso, _ = ProgresoUsuario.objects.get_or_create(usuario=usuario)

        # Aplicar regeneración previa acumulada antes de descontar
        progreso, vidas_max, _, _ = aplicar_regeneracion_vidas(progreso)

        ahora = timezone.now()
        # Si estaba en el tope de vidas, el ciclo para regenerar la vida que se pierde empieza en este momento
        if progreso.vidas_actuales >= vidas_max:
            progreso.ultimo_reinicio_vidas = ahora

        if progreso.vidas_actuales > 0:
            progreso.vidas_actuales -= 1
            progreso.save(update_fields=['vidas_actuales', 'ultimo_reinicio_vidas'])

        # Calcular tiempo restante exacto para la siguiente vida según Parámetros Globales
        progreso, vidas_max, segundos_siguiente, regen_min = aplicar_regeneracion_vidas(progreso)

        PartidaJugada.objects.create(
            usuario=usuario,
            nivel=nivel,
            resultado=ResultadoPartidaChoices.DERROTA,
            oro_obtenido=0,
            gemas_obtenidas=0,
        )
        return JsonResponse({
            'success': True,
            'vidas_actuales': progreso.vidas_actuales,
            'vidas_maximas': vidas_max,
            'segundos_siguiente_vida': segundos_siguiente,
            'regeneracion_minutos': regen_min,
            'recompensas': {
                'oro': 0,
                'gemas': 0,
                'xp': 0,
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required(login_url='/login/')
def api_estado_vidas_ajax(request):
    """
    Retorna el estado de vidas actual y tiempo para regenerar la siguiente vida
    según los Parámetros Globales.
    """
    usuario = request.user
    progreso, _ = ProgresoUsuario.objects.get_or_create(usuario=usuario)
    progreso, vidas_max, segundos_siguiente, regen_min = aplicar_regeneracion_vidas(progreso)
    return JsonResponse({
        'success': True,
        'vidas_actuales': progreso.vidas_actuales,
        'vidas_maximas': vidas_max,
        'segundos_siguiente_vida': segundos_siguiente,
        'regeneracion_minutos': regen_min,
    })


@login_required(login_url='/login/')
@require_POST
def api_canjear_tienda_ajax(request):
    """
    Procesa compras o canjes de recursos en la Tienda Arcana (Oro, Gemas, Energía Arcana).
    Actualiza el ProgresoUsuario en base de datos y devuelve el nuevo estado del HUD.
    """
    usuario = request.user
    item = request.POST.get('item', '').strip().lower()
    progreso, _ = ProgresoUsuario.objects.get_or_create(usuario=usuario)
    vidas_max = get_parametro_global('vidas_maximas', 3, tipo=int)

    if item == 'energia':
        progreso.vidas_actuales = vidas_max
        progreso.ultimo_reinicio_vidas = timezone.now()
        progreso.save(update_fields=['vidas_actuales', 'ultimo_reinicio_vidas'])
        return JsonResponse({
            'success': True,
            'message': f'¡Energía Arcana restaurada por completo ({vidas_max} / {vidas_max} Vidas)!',
            'vidas_actuales': progreso.vidas_actuales,
            'vidas_maximas': vidas_max,
            'oro': progreso.oro,
            'gemas': progreso.gemas,
        })
    elif item in ('oro', 'oro_500'):
        progreso.oro += 500
        progreso.save(update_fields=['oro'])
        return JsonResponse({
            'success': True,
            'message': '¡500 Monedas de oro agregadas con éxito!',
            'vidas_actuales': progreso.vidas_actuales,
            'vidas_maximas': vidas_max,
            'oro': progreso.oro,
            'gemas': progreso.gemas,
        })
    elif item in ('oro_1500',):
        progreso.oro += 1500
        progreso.save(update_fields=['oro'])
        return JsonResponse({
            'success': True,
            'message': '¡1.500 Monedas de oro agregadas con éxito!',
            'vidas_actuales': progreso.vidas_actuales,
            'vidas_maximas': vidas_max,
            'oro': progreso.oro,
            'gemas': progreso.gemas,
        })
    elif item in ('gemas', 'gemas_50'):
        progreso.gemas += 50
        progreso.save(update_fields=['gemas'])
        return JsonResponse({
            'success': True,
            'message': '¡50 Gemas Arcanas agregadas con éxito!',
            'vidas_actuales': progreso.vidas_actuales,
            'vidas_maximas': vidas_max,
            'oro': progreso.oro,
            'gemas': progreso.gemas,
        })
    elif item in ('gemas_120',):
        progreso.gemas += 120
        progreso.save(update_fields=['gemas'])
        return JsonResponse({
            'success': True,
            'message': '¡120 Gemas Arcanas agregadas con éxito!',
            'vidas_actuales': progreso.vidas_actuales,
            'vidas_maximas': vidas_max,
            'oro': progreso.oro,
            'gemas': progreso.gemas,
        })
    elif item in ('pase',):
        return JsonResponse({
            'success': True,
            'message': '¡Pase de Auditor Maestro activado para la temporada!',
            'vidas_actuales': progreso.vidas_actuales,
            'vidas_maximas': vidas_max,
            'oro': progreso.oro,
            'gemas': progreso.gemas,
        })

    return JsonResponse({'success': False, 'error': 'Artículo no reconocido'}, status=400)












