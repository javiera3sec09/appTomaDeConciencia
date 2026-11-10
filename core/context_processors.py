"""
Context Processors para inyectar analítica en el admin y los datos del HUD de jugador en las vistas de juego.
"""
from .views import get_analytics_data


def admin_analytics_context(request):
    """
    Inyecta datos agregados de rendimiento, economía y jugadores cuando el usuario
    está navegando en el panel de administración (/admin/).
    """
    if request.path.startswith('/admin') and getattr(request.user, 'is_staff', False):
        try:
            return {'analytics': get_analytics_data()}
        except Exception:
            return {'analytics': {}}
    return {}


def player_hud_context(request):
    """
    Inyecta automáticamente en el contexto de todas las plantillas los datos reales del
    empleado / jugador logueado para que la parte superior (HUD) sea idéntica y reactiva:
    - usuario
    - progreso (nivel, xp, oro, gemas, vidas)
    - xp_en_nivel, xp_meta_nivel, pct_xp
    - xp_en_nivel_fmt, xp_meta_nivel_fmt
    - oro_fmt, gemas_fmt
    - energia_actual, energia_maxima
    - avatares_coleccion
    """
    user = getattr(request, 'user', None)
    if not user or not user.is_authenticated:
        return {}

    from .models import ProgresoUsuario
    from .utils import get_parametro_global, aplicar_regeneracion_vidas

    oro_inicial = get_parametro_global('oro_inicial', 100, tipo=int)
    gemas_iniciales = get_parametro_global('gemas_iniciales', 10, tipo=int)
    vidas_iniciales = get_parametro_global('vidas_iniciales', 3, tipo=int)
    vidas_maximas = get_parametro_global('vidas_maximas', 3, tipo=int)

    try:
        progreso, created = ProgresoUsuario.objects.get_or_create(
            usuario=user,
            defaults={
                'nivel': 1,
                'oro': oro_inicial,
                'gemas': gemas_iniciales,
                'xp': 0,
                'vidas_actuales': vidas_iniciales,
            }
        )
    except Exception:
        progreso = getattr(user, 'progreso', None)

    segundos_siguiente = 0
    regen_min = 5

    if progreso:
        progreso, vidas_maximas, segundos_siguiente, regen_min = aplicar_regeneracion_vidas(progreso)

    nivel = getattr(progreso, 'nivel', 1) or 1
    xp = getattr(progreso, 'xp', 0) or 0
    oro = getattr(progreso, 'oro', 0) if getattr(progreso, 'oro', None) is not None else oro_inicial
    gemas = getattr(progreso, 'gemas', 0) if getattr(progreso, 'gemas', None) is not None else gemas_iniciales
    vidas = getattr(progreso, 'vidas_actuales', vidas_iniciales)

    xp_meta_nivel = max(500, nivel * 250)
    xp_en_nivel = xp % xp_meta_nivel if xp_meta_nivel > 0 else xp
    if xp_en_nivel == 0 and xp > 0:
        xp_en_nivel = min(xp, xp_meta_nivel)
    pct_xp = min(100, round((xp_en_nivel / xp_meta_nivel) * 100)) if xp_meta_nivel > 0 else 0

    def fmt_num(n):
        try:
            return f"{int(n):,}".replace(",", ".")
        except Exception:
            return str(n)

    avatares_coleccion = [
        {'id': 1, 'nombre': 'Nigromante Sombra', 'img': '/static/img/avatars/necromancer_1.png'},
        {'id': 2, 'nombre': 'Hechicera Arcana', 'img': '/static/img/avatars/necromancer_2.png'},
        {'id': 3, 'nombre': 'Archimago ISO', 'img': '/static/img/avatars/necromancer_3.png'},
        {'id': 4, 'nombre': 'Bruja de Compliance', 'img': '/static/img/avatars/necromancer_4.png'},
        {'id': 5, 'nombre': 'Señor del Abismo', 'img': '/static/img/avatars/necromancer_5.png'},
    ]

    return {
        'usuario': user,
        'progreso': progreso,
        'xp_en_nivel': xp_en_nivel,
        'xp_meta_nivel': xp_meta_nivel,
        'pct_xp': pct_xp,
        'xp_en_nivel_fmt': fmt_num(xp_en_nivel),
        'xp_meta_nivel_fmt': fmt_num(xp_meta_nivel),
        'oro_fmt': fmt_num(oro),
        'gemas_fmt': fmt_num(gemas),
        'energia_actual': vidas,
        'energia_maxima': vidas_maximas,
        'vidas_maximas': vidas_maximas,
        'segundos_siguiente_vida': segundos_siguiente,
        'regeneracion_minutos': regen_min,
        'avatares_coleccion': avatares_coleccion,
        'mensajes_no_leidos': 1,
        'notificaciones_no_leidas': 1,
    }

