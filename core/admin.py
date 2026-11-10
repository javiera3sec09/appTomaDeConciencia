"""
Configuración del Panel de Administración de Django (Django Admin).
Implementa Acciones Personalizadas de Reinicio con Auditoría Forense,
Inlines con validación estricta (máximo 5 cartas por fase) y Bitácora Inmutable.
"""
from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Count, Q

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
    RolUsuarioChoices,
    EstadoUsuarioChoices,
    AccionAuditoriaChoices,
    DificultadChoices,
    EstadoEntidadChoices,
)
from .forms import (
    FaseCartaOpcionInlineFormSet,
    CartaForm,
    NORMA_ISO_CHOICES,
    FaseCasoForm,
    AMENAZAS_SUGERIDAS,
)
from .utils import (
    get_client_ip,
    registrar_auditoria,
    serialize_instance,
    resequenciar_ids_usuarios,
    get_parametro_global,
    sincronizar_efecto_parametro_global,
)


# ==============================================================================
# INLINES
# ==============================================================================

class ProgresoUsuarioInline(admin.StackedInline):
    """
    Permite visualizar y ajustar el progreso del usuario directamente en la ficha del Usuario.
    """
    model = ProgresoUsuario
    can_delete = False
    verbose_name = "Estado de Progreso y Economía de Juego"
    verbose_name_plural = "Estado de Progreso y Economía de Juego"
    readonly_fields = ('ultimo_reinicio_vidas', 'ultimo_reinicio_progreso')
    extra = 0


class FaseCartaOpcionInline(admin.TabularInline):
    """
    Gestión de opciones de cartas asociadas a una Fase de Caso.
    Restricción de Integridad: Máximo 5 cartas por fase, validado con FormSet.
    """
    model = FaseCartaOpcion
    formset = FaseCartaOpcionInlineFormSet
    extra = 1
    max_num = 5
    autocomplete_fields = ['carta']
    fields = ('carta', 'es_solucion_correcta')
    verbose_name = "Carta Ofertada para la Fase"
    verbose_name_plural = "Baraja de Opciones para la Fase (Máximo 5 cartas)"

    def get_help_text(self):
        return "Regla de Negocio: Se permite un máximo de 5 cartas por fase para garantizar balance de juego."


class FaseCasoInline(admin.StackedInline):
    """
    Inline para definir Fases de Casos directamente desde la edición de un Nivel.
    """
    model = FaseCaso
    extra = 1
    fields = (
        ('numero_fase', 'titulo_incidente', 'amenaza'),
        'caso_contexto',
        ('dificultad', 'recompensa_oro', 'recompensa_xp', 'estado')
    )
    show_change_link = True
    verbose_name = "Fase de Caso del Nivel"
    verbose_name_plural = "Fases de Casos Contenidas en este Nivel"


# ==============================================================================
# ADMIN MÓDULO 1: USUARIOS Y PROGRESO
# ==============================================================================

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    """
    Administración de Usuarios y Colaboradores.
    Incluye acción administrativa de Reinicio de Progreso con registro en auditoría.
    """
    list_display = (
        'alias',
        'nombre_completo',
        'correo',
        'area',
        'badge_rol',
        'badge_estado',
        'get_nivel',
        'get_xp',
        'is_staff',
        'created_at',
    )
    list_filter = ('rol', 'estado', 'area', 'is_staff', 'created_at')
    search_fields = ('alias', 'nombre_completo', 'correo', 'area')
    ordering = ('-created_at',)
    inlines = [ProgresoUsuarioInline]
    actions = ['reiniciar_progreso_action', 'activar_usuarios_action', 'desactivar_usuarios_action', 'eliminar_usuarios_action']

    fieldsets = (
        ('Credenciales e Identidad Institucional', {
            'fields': (('correo', 'alias'), ('nombre_completo', 'area'))
        }),
        ('Roles y Privilegios', {
            'fields': (('rol', 'estado'), ('is_staff', 'is_superuser'))
        }),
        ('Fechas de Auditoría', {
            'fields': (('created_at', 'updated_at'),),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    @admin.display(description="Rol")
    def badge_rol(self, obj):
        color = "#1d4ed8" if obj.rol == RolUsuarioChoices.ADMINISTRADOR else "#047857"
        return format_html(
            '<span style="background:{}; color:#fff; padding:3px 8px; border-radius:12px; font-weight:600; font-size:11px;">{}</span>',
            color,
            obj.get_rol_display()
        )

    @admin.display(description="Estado")
    def badge_estado(self, obj):
        color = "#16a34a" if obj.estado == EstadoUsuarioChoices.ACTIVO else "#dc2626"
        return format_html(
            '<span style="background:{}; color:#fff; padding:3px 8px; border-radius:12px; font-weight:600; font-size:11px;">{}</span>',
            color,
            obj.get_estado_display()
        )

    @admin.display(description="Nivel Actual")
    def get_nivel(self, obj):
        return getattr(getattr(obj, 'progreso', None), 'nivel', '-')

    @admin.display(description="XP")
    def get_xp(self, obj):
        return getattr(getattr(obj, 'progreso', None), 'xp', '-')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        total = Usuario.objects.count()
        activos = Usuario.objects.filter(estado=EstadoUsuarioChoices.ACTIVO).count()
        inactivos = Usuario.objects.filter(estado=EstadoUsuarioChoices.INACTIVO).count()
        administradores = Usuario.objects.filter(rol=RolUsuarioChoices.ADMINISTRADOR).count()
        jugadores = Usuario.objects.filter(rol=RolUsuarioChoices.EMPLEADO_JUGADOR).count()

        extra_context.update({
            'kpi_total_usuarios': total,
            'kpi_usuarios_activos': activos,
            'kpi_usuarios_inactivos': inactivos,
            'kpi_total_administradores': administradores,
            'kpi_total_jugadores': jugadores,
            'pct_activos': round((activos / total * 100), 1) if total > 0 else 0.0,
            'pct_inactivos': round((inactivos / total * 100), 1) if total > 0 else 0.0,
            'pct_admin': round((administradores / total * 100), 1) if total > 0 else 0.0,
            'pct_jugadores': round((jugadores / total * 100), 1) if total > 0 else 0.0,
            'roles_choices': RolUsuarioChoices.choices,
            'estados_choices': EstadoUsuarioChoices.choices,
            'areas_list': list(Usuario.objects.values_list('area', flat=True).distinct()),
        })
        return super().changelist_view(request, extra_context=extra_context)

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        resequenciar_ids_usuarios()

    def delete_queryset(self, request, queryset):
        super().delete_queryset(request, queryset)
        resequenciar_ids_usuarios()

    @admin.action(description="🗑️ Eliminar usuarios seleccionados y resecuenciar IDs (1, 2, 3...)")
    def eliminar_usuarios_action(self, request, queryset):
        ip = get_client_ip(request)
        queryset_valid = queryset.exclude(pk=request.user.pk)
        eliminados = 0
        for u in queryset_valid:
            registrar_auditoria(
                admin=request.user,
                accion=AccionAuditoriaChoices.ELIMINAR,
                modulo_afectado='Usuario',
                registro_id=str(u.pk),
                datos_anteriores=serialize_instance(u),
                datos_nuevos=None,
                ip=ip
            )
            u.delete()
            eliminados += 1
        resequenciar_ids_usuarios()
        self.message_user(request, f"Se eliminaron {eliminados} usuarios y se reorganizaron los IDs consecutivamente (1, 2, 3...).")

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        La URL de edición clásica de Django no existe en este sistema.
        Toda la edición de usuarios se gestiona desde el panel lateral AJAX.
        """
        from django.http import Http404
        raise Http404("Esta URL no existe. Utilice el panel lateral para editar usuarios.")

    def get_urls(self):
        """
        Elimina la URL `/admin/core/usuario/<id>/change/` del registro de Django admin.
        Al no existir la ruta, cualquier acceso directo devuelve 404.
        """
        urls = super().get_urls()
        # Filtrar cualquier patrón cuyo nombre contenga 'change' pero no 'changelist'
        filtered_urls = [
            u for u in urls
            if not (
                getattr(u, 'name', None)
                and 'change' in u.name
                and 'changelist' not in u.name
            )
        ]
        return filtered_urls

    # --------------------------------------------------------------------------
    # ACCIÓN PERSONALIZADA: REINICIAR PROGRESO CON AUDITORÍA
    # --------------------------------------------------------------------------
    @admin.action(description="⚠️ Reiniciar Progreso de Jugador (Nivel y XP a 0) con Auditoría")
    def reiniciar_progreso_action(self, request, queryset):
        """
        Reinicia a 0 el nivel, XP, oro y gemas del jugador, y regenera vidas a 3.
        Genera registro formal e inmutable en RegistroAuditoria.
        """
        reiniciados_count = 0
        ip = get_client_ip(request)
        ahora = timezone.now()

        for usuario in queryset:
            # Obtener o asegurar la existencia de ProgresoUsuario
            progreso, created = ProgresoUsuario.objects.get_or_create(usuario=usuario)

            # Capturar snapshot de datos anteriores
            datos_anteriores = {
                'usuario_alias': usuario.alias,
                'usuario_correo': usuario.correo,
                'nivel': progreso.nivel,
                'xp': progreso.xp,
                'oro': progreso.oro,
                'gemas': progreso.gemas,
                'vidas_actuales': progreso.vidas_actuales,
                'ultimo_reinicio_progreso': str(progreso.ultimo_reinicio_progreso),
            }

            # Aplicar reinicio con valores de ParametroGlobal
            oro_def = get_parametro_global('oro_inicial', 100, tipo=int)
            gemas_def = get_parametro_global('gemas_iniciales', 10, tipo=int)
            vidas_def = get_parametro_global('vidas_iniciales', 3, tipo=int)

            progreso.nivel = 1
            progreso.xp = 0
            progreso.oro = oro_def
            progreso.gemas = gemas_def
            progreso.vidas_actuales = vidas_def
            progreso.ultimo_reinicio_progreso = ahora
            progreso.save()

            datos_nuevos = {
                'usuario_alias': usuario.alias,
                'usuario_correo': usuario.correo,
                'nivel': 1,
                'xp': 0,
                'oro': oro_def,
                'gemas': gemas_def,
                'vidas_actuales': vidas_def,
                'ultimo_reinicio_progreso': ahora.isoformat(),
            }

            # Registro forense inmutable
            registrar_auditoria(
                admin=request.user,
                accion=AccionAuditoriaChoices.REINICIAR_PROGRESO,
                modulo_afectado='ProgresoUsuario',
                registro_id=str(progreso.pk),
                datos_anteriores=datos_anteriores,
                datos_nuevos=datos_nuevos,
                ip=ip
            )
            reiniciados_count += 1

        self.message_user(
            request,
            f"Se ha reiniciado exitosamente el progreso de {reiniciados_count} jugador(es). "
            f"Se generaron los asientos correspondientes en la bitácora de auditoría.",
            messages.SUCCESS
        )

    @admin.action(description="Marcar seleccionados como Activos")
    def activar_usuarios_action(self, request, queryset):
        updated = queryset.update(estado=EstadoUsuarioChoices.ACTIVO, is_active=True)
        self.message_user(request, f"{updated} usuario(s) marcados como activos.", messages.INFO)

    @admin.action(description="Marcar seleccionados como Inactivos")
    def desactivar_usuarios_action(self, request, queryset):
        updated = queryset.update(estado=EstadoUsuarioChoices.INACTIVO, is_active=False)
        self.message_user(request, f"{updated} usuario(s) marcados como inactivos.", messages.WARNING)


@admin.register(ProgresoUsuario)
class ProgresoUsuarioAdmin(admin.ModelAdmin):
    """
    Administración específica de la tabla de progreso de jugadores.
    Presenta la vista enriquecida ISO QUEST con KPIs, filtros, tabla y modales interactivos.
    """
    change_list_template = "admin/core/progresousuario/change_list.html"
    list_display = (
        'usuario',
        'nivel',
        'xp',
        'oro',
        'gemas',
        'vidas_actuales',
        'ultimo_reinicio_vidas',
        'ultimo_reinicio_progreso',
    )
    list_filter = ('nivel', 'vidas_actuales')
    search_fields = ('usuario__alias', 'usuario__nombre_completo', 'usuario__correo')
    ordering = ('-ultimo_reinicio_vidas',)
    list_per_page = 10
    actions = ['reiniciar_progreso_desde_progreso_action']

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        from django.db.models import Avg, Sum, Count, Min, Max
        
        total = ProgresoUsuario.objects.count()
        activos = ProgresoUsuario.objects.filter(usuario__estado=EstadoUsuarioChoices.ACTIVO).count()
        agg = ProgresoUsuario.objects.aggregate(
            avg_nivel=Avg('nivel'),
            min_nivel=Min('nivel'),
            max_nivel=Max('nivel'),
            sum_oro=Sum('oro'),
            avg_oro=Avg('oro'),
            sum_gemas=Sum('gemas'),
            avg_gemas=Avg('gemas')
        )
        
        kpi_total = total
        kpi_nivel = round(agg['avg_nivel'], 1) if agg['avg_nivel'] is not None else 1.0
        kpi_oro = agg['sum_oro'] or 0
        kpi_gemas = agg['sum_gemas'] or 0
        kpi_oro_promedio = round(agg['avg_oro']) if agg['avg_oro'] is not None else 0
        kpi_gemas_promedio = round(agg['avg_gemas']) if agg['avg_gemas'] is not None else 0
        min_nivel = agg['min_nivel'] or 1
        max_nivel = agg['max_nivel'] or 1

        extra_context.update({
            'kpi_total_jugadores': f"{kpi_total:,}",
            'kpi_nivel_promedio': kpi_nivel,
            'kpi_oro_total': f"{kpi_oro:,}",
            'kpi_gemas_totales': f"{kpi_gemas:,}",
            'kpi_sub_jugadores': f"{activos} activos en plataforma",
            'kpi_sub_nivel': f"Rango nivel {min_nivel} - {max_nivel}",
            'kpi_sub_oro': f"Promedio: {kpi_oro_promedio:,} por jugador",
            'kpi_sub_gemas': f"Promedio: {kpi_gemas_promedio:,} por jugador",
            'roles_choices': RolUsuarioChoices.choices,
            'estados_choices': EstadoUsuarioChoices.choices,
            'total_jugadores_display': total,
        })
        return super().changelist_view(request, extra_context=extra_context)

    @admin.action(description="⚠️ Reiniciar progreso de los registros seleccionados")
    def reiniciar_progreso_desde_progreso_action(self, request, queryset):
        ip = get_client_ip(request)
        ahora = timezone.now()
        count = 0
        oro_def = get_parametro_global('oro_inicial', 100, tipo=int)
        gemas_def = get_parametro_global('gemas_iniciales', 10, tipo=int)
        vidas_def = get_parametro_global('vidas_iniciales', 3, tipo=int)
        for progreso in queryset:
            datos_anteriores = serialize_instance(progreso)
            progreso.nivel = 1
            progreso.xp = 0
            progreso.oro = oro_def
            progreso.gemas = gemas_def
            progreso.vidas_actuales = vidas_def
            progreso.ultimo_reinicio_progreso = ahora
            progreso.save()
            datos_nuevos = serialize_instance(progreso)

            registrar_auditoria(
                admin=request.user,
                accion=AccionAuditoriaChoices.REINICIAR_PROGRESO,
                modulo_afectado='ProgresoUsuario',
                registro_id=str(progreso.pk),
                datos_anteriores=datos_anteriores,
                datos_nuevos=datos_nuevos,
                ip=ip
            )
            count += 1
        self.message_user(request, f"{count} perfil(es) de progreso reiniciados con auditoría.", messages.SUCCESS)


# ==============================================================================
# ADMIN MÓDULO 2: MUNDOS, NIVELES Y FASES
# ==============================================================================

@admin.register(Mundo)
class MundoAdmin(admin.ModelAdmin):
    """
    Administración de Mundos ISO (ISO 27001, ISO 9001, etc.).
    Vista personalizada Dark SaaS / ISO QUEST con KPIs, filtros y modales interactivos.
    """
    change_list_template = "admin/core/mundo/change_list.html"
    list_display = (
        'orden',
        'codigo_iso',
        'nombre_tematico',
        'dominio',
        'dificultad',
        'estado',
        'total_niveles',
    )
    list_filter = ('dificultad', 'estado', 'dominio')
    search_fields = ('codigo_iso', 'nombre_tematico', 'dominio')
    ordering = ('orden',)
    list_per_page = 10

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_niveles_count=Count('niveles'))

    @admin.display(description="Total Niveles")
    def total_niveles(self, obj):
        return getattr(obj, '_niveles_count', 0)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        from core.models import EstadoEntidadChoices, DificultadChoices
        
        total_mundos = Mundo.objects.count()
        activos = Mundo.objects.filter(estado=EstadoEntidadChoices.ACTIVO).count()
        dominios = list(Mundo.objects.values_list('dominio', flat=True).distinct())

        pct_activos = round((activos / total_mundos * 100)) if total_mundos > 0 else 0

        extra_context.update({
            'kpi_total_mundos': total_mundos,
            'kpi_mundos_activos': activos,
            'pct_activos': pct_activos,
            'kpi_dominio_principal': dominios[0] if dominios else 'General',
            'kpi_dominio_sub': 'Mundos Oficiales',
            'kpi_dificultad_promedio': 'Equilibrada',
            'dominios_list': dominios,
            'dificultades_choices': DificultadChoices.choices,
            'estados_choices': EstadoEntidadChoices.choices,
        })
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Nivel)
class NivelAdmin(admin.ModelAdmin):
    """
    Administración de Niveles con vista personalizada Dark SaaS / ISO QUEST,
    selector horizontal de mundos activos, hero banner con estadísticas y modales interactivos.
    """
    change_list_template = "admin/core/nivel/change_list.html"
    list_display = (
        'numero_nivel',
        'titulo',
        'mundo',
        'tipo',
        'dificultad',
        'recompensa_oro',
        'recompensa_xp',
        'estado',
        'total_fases',
    )
    list_filter = ('mundo', 'tipo', 'dificultad', 'estado')
    search_fields = ('titulo', 'mundo__codigo_iso', 'mundo__nombre_tematico')
    ordering = ('mundo', 'numero_nivel')
    inlines = [FaseCasoInline]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_fases_count=Count('fases'))

    @admin.display(description="Fases")
    def total_fases(self, obj):
        return getattr(obj, '_fases_count', 0)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        from core.models import Mundo, TipoNivelChoices, DificultadChoices, EstadoEntidadChoices
        from django.db.models import Sum, Count
        import json

        mundos_activos = list(Mundo.objects.filter(estado=EstadoEntidadChoices.ACTIVO).order_by('orden'))
        all_mundos = list(Mundo.objects.all().order_by('orden'))

        selected_mundo_id = request.GET.get('mundo_id')
        selected_mundo = None
        if selected_mundo_id and str(selected_mundo_id).isdigit():
            selected_mundo = Mundo.objects.filter(pk=int(selected_mundo_id)).first()
        if not selected_mundo:
            selected_mundo = mundos_activos[0] if mundos_activos else (all_mundos[0] if all_mundos else None)

        mundos_data = []
        target_mundos = mundos_activos if mundos_activos else all_mundos
        for m in target_mundos:
            agg = m.niveles.aggregate(
                total_xp=Sum('recompensa_xp'),
                total_oro=Sum('recompensa_oro'),
                total_gemas=Sum('recompensa_gemas'),
                total_niveles=Count('id')
            )
            mundos_data.append({
                'id': m.id,
                'orden': m.orden,
                'codigo_iso': m.codigo_iso,
                'nombre_tematico': m.nombre_tematico,
                'nombre_corto': m.nombre_corto,
                'descripcion': m.descripcion_tematica,
                'avatar_url': m.avatar_guardia_url,
                'icono_class': m.icono_class,
                'estado': m.estado,
                'is_active': m.estado == EstadoEntidadChoices.ACTIVO,
                'total_niveles': agg['total_niveles'] or 0,
                'total_xp': agg['total_xp'] or 0,
                'total_oro': agg['total_oro'] or 0,
                'total_gemas': agg['total_gemas'] or 0,
            })

        sel_data = next((item for item in mundos_data if selected_mundo and item['id'] == selected_mundo.id), None)
        if not sel_data and selected_mundo:
            agg = selected_mundo.niveles.aggregate(
                total_xp=Sum('recompensa_xp'),
                total_oro=Sum('recompensa_oro'),
                total_gemas=Sum('recompensa_gemas'),
                total_niveles=Count('id')
            )
            sel_data = {
                'id': selected_mundo.id,
                'orden': selected_mundo.orden,
                'codigo_iso': selected_mundo.codigo_iso,
                'nombre_tematico': selected_mundo.nombre_tematico,
                'nombre_corto': selected_mundo.nombre_corto,
                'descripcion': selected_mundo.descripcion_tematica,
                'avatar_url': selected_mundo.avatar_guardia_url,
                'icono_class': selected_mundo.icono_class,
                'estado': selected_mundo.estado,
                'is_active': selected_mundo.estado == EstadoEntidadChoices.ACTIVO,
                'total_niveles': agg['total_niveles'] or 0,
                'total_xp': agg['total_xp'] or 0,
                'total_oro': agg['total_oro'] or 0,
                'total_gemas': agg['total_gemas'] or 0,
            }

        niveles_qs = Nivel.objects.filter(mundo=selected_mundo).order_by('numero_nivel') if selected_mundo else Nivel.objects.none()

        extra_context.update({
            'mundos_activos': target_mundos,
            'all_mundos': all_mundos,
            'mundos_data': mundos_data,
            'mundos_data_json': json.dumps(mundos_data),
            'selected_mundo': selected_mundo,
            'selected_mundo_data': sel_data,
            'niveles_list': list(niveles_qs),
            'tipos_choices': TipoNivelChoices.choices,
            'dificultades_choices': DificultadChoices.choices,
            'estados_choices': EstadoEntidadChoices.choices,
        })
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(FaseCaso)
class FaseCasoAdmin(admin.ModelAdmin):
    """
    Administración de Fases de Casos con vista Dark SaaS / ISO QUEST,
    editor con Vista Previa holográfica en tiempo real, selector de Mundo y Nivel,
    e Inline de Cartas (Máximo 5 cartas por fase).
    """
    form = FaseCasoForm
    change_list_template = "admin/core/fasecaso/change_list.html"
    change_form_template = "admin/core/fasecaso/change_form.html"
    list_display = (
        'numero_fase',
        'titulo_incidente',
        'nivel',
        'amenaza',
        'dificultad',
        'cartas_asignadas_count',
        'estado',
    )
    list_filter = ('dificultad', 'estado', 'nivel__mundo')
    search_fields = ('titulo_incidente', 'amenaza', 'caso_contexto')
    inlines = [FaseCartaOpcionInline]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_cartas_count=Count('opciones_cartas'))

    @admin.display(description="Cartas Asignadas (Max 5)")
    def cartas_asignadas_count(self, obj):
        count = getattr(obj, '_cartas_count', 0)
        color = "#16a34a" if count <= 5 else "#dc2626"
        return format_html(
            '<span style="color:{}; font-weight:bold;">{}/5 Cartas</span>',
            color,
            count
        )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        import json

        # Normalizar parámetros de filtro por mundo para evitar redirección de Django (IncorrectLookupParameters)
        mundo_param = (
            request.GET.get('mundo')
            or request.GET.get('mundo_id')
            or request.GET.get('nivel__mundo__id__exact')
        )

        q = request.GET.copy()
        if 'mundo' in q:
            del q['mundo']
        if 'mundo_id' in q:
            del q['mundo_id']

        selected_mundo = None
        if mundo_param and str(mundo_param).strip().isdigit():
            try:
                selected_mundo = Mundo.objects.filter(pk=int(mundo_param)).first()
            except (ValueError, TypeError):
                selected_mundo = None

        if selected_mundo:
            q['nivel__mundo__id__exact'] = str(selected_mundo.id)

        request.GET = q

        mundos_qs = Mundo.objects.filter(estado=EstadoEntidadChoices.ACTIVO).order_by('orden')
        if not mundos_qs.exists():
            mundos_qs = Mundo.objects.all().order_by('orden')

        fases_qs = FaseCaso.objects.select_related('nivel', 'nivel__mundo').order_by(
            'nivel__mundo__orden', 'nivel__numero_nivel', 'numero_fase'
        )

        if selected_mundo:
            fases_qs = fases_qs.filter(nivel__mundo=selected_mundo)

        fases_list = list(fases_qs)
        mundos_list = list(mundos_qs)

        total_fases = len(fases_list) if selected_mundo else FaseCaso.objects.count()
        fases_activas = sum(1 for f in fases_list if f.estado == EstadoEntidadChoices.ACTIVO)
        pct_activas = round((fases_activas / total_fases * 100), 1) if total_fases > 0 else 100.0
        total_niveles = selected_mundo.niveles.count() if selected_mundo else Nivel.objects.count()
        total_mundos = 1 if selected_mundo else mundos_qs.count()

        extra_context.update({
            'kpi_total_fases': total_fases,
            'kpi_fases_activas': fases_activas,
            'kpi_pct_activas': pct_activas,
            'kpi_total_niveles': total_niveles,
            'kpi_total_mundos': total_mundos,
            'mundos_list': mundos_list,
            'selected_mundo': selected_mundo,
            'fases_list': fases_list,
            'dificultades_choices': DificultadChoices.choices,
            'estados_choices': EstadoEntidadChoices.choices,
        })
        return super().changelist_view(request, extra_context=extra_context)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        import json

        fase_obj = None
        if object_id:
            try:
                fase_obj = FaseCaso.objects.select_related('nivel', 'nivel__mundo').get(pk=object_id)
            except FaseCaso.DoesNotExist:
                fase_obj = None

        mundos_qs = Mundo.objects.all().order_by('orden')
        niveles_qs = Nivel.objects.select_related('mundo').all().order_by('mundo__orden', 'numero_nivel')

        # Determinar Nivel y Mundo seleccionados por defecto
        selected_nivel = None
        if fase_obj:
            selected_nivel = fase_obj.nivel
        else:
            nivel_id_param = request.GET.get('nivel')
            if nivel_id_param:
                try:
                    selected_nivel = Nivel.objects.get(pk=int(nivel_id_param))
                except (Nivel.DoesNotExist, ValueError):
                    selected_nivel = niveles_qs.first()
            else:
                selected_nivel = niveles_qs.first()

        selected_mundo = selected_nivel.mundo if selected_nivel else mundos_qs.first()

        # Generar diccionario serializado para JavaScript interactivo
        mundos_data = []
        for m in mundos_qs:
            mundos_data.append({
                'id': m.id,
                'codigo_iso': m.codigo_iso,
                'nombre_tematico': m.nombre_tematico,
                'dominio': m.dominio,
                'imagen_url': m.imagen_url,
                'descripcion_tematica': m.descripcion_tematica,
            })

        niveles_data = []
        for n in niveles_qs:
            niveles_data.append({
                'id': n.id,
                'mundo_id': n.mundo_id,
                'numero_nivel': n.numero_nivel,
                'titulo': n.titulo,
                'dificultad': n.get_dificultad_display(),
                'recompensa_oro': n.recompensa_oro,
                'recompensa_xp': n.recompensa_xp,
            })

        extra_context.update({
            'fase_obj': fase_obj,
            'is_edit': object_id is not None,
            'mundos_list': list(mundos_qs),
            'niveles_list': list(niveles_qs),
            'selected_mundo': selected_mundo,
            'selected_nivel': selected_nivel,
            'mundos_json': json.dumps(mundos_data),
            'niveles_json': json.dumps(niveles_data),
            'amenazas_sugeridas': AMENAZAS_SUGERIDAS,
            'dificultad_choices': DificultadChoices.choices,
            'estados_choices': EstadoEntidadChoices.choices,
        })
        return super().changeform_view(request, object_id=object_id, form_url=form_url, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        """
        Guarda la fase de caso registrando auditoría forense inmutable.
        """
        datos_anteriores = {}
        if change and obj.pk:
            try:
                antiguo = FaseCaso.objects.get(pk=obj.pk)
                datos_anteriores = serialize_instance(antiguo)
            except FaseCaso.DoesNotExist:
                pass

        super().save_model(request, obj, form, change)
        datos_nuevos = serialize_instance(obj)

        registrar_auditoria(
            admin=request.user,
            accion=AccionAuditoriaChoices.EDITAR if change else AccionAuditoriaChoices.CREAR,
            modulo_afectado='FaseCaso',
            registro_id=str(obj.pk),
            datos_anteriores=datos_anteriores,
            datos_nuevos=datos_nuevos,
            request=request
        )

    def delete_model(self, request, obj):
        """
        Elimina la fase de caso registrando auditoría forense inmutable.
        """
        obj_pk = str(obj.pk)
        datos_anteriores = serialize_instance(obj)
        super().delete_model(request, obj)

        registrar_auditoria(
            admin=request.user,
            accion=AccionAuditoriaChoices.ELIMINAR,
            modulo_afectado='FaseCaso',
            registro_id=obj_pk,
            datos_anteriores=datos_anteriores,
            datos_nuevos={},
            request=request
        )


# ==============================================================================
# ADMIN MÓDULO 3: CARTAS Y BARAJAS
# ==============================================================================

@admin.register(Carta)
class CartaAdmin(admin.ModelAdmin):
    """
    Catálogo de cartas de salvaguarda y controles ISO con vista Dark SaaS / ISO QUEST,
    métricas de poder de baraja, visualización en cuadrícula interactiva y editor visual con Vista Previa.
    """
    form = CartaForm
    change_list_template = "admin/core/carta/change_list.html"
    change_form_template = "admin/core/carta/change_form.html"
    list_display = (
        'nombre',
        'norma_iso',
        'concepto',
        'fuerza',
        'defensa',
        'estado',
    )
    list_filter = ('norma_iso', 'estado')
    search_fields = ('nombre', 'norma_iso', 'concepto', 'descripcion')
    ordering = ('id',)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        from core.models import EstadoEntidadChoices
        from django.db.models import Avg

        total = Carta.objects.count()
        activas = Carta.objects.filter(estado=EstadoEntidadChoices.ACTIVO).count()
        normas = list(Carta.objects.values_list('norma_iso', flat=True).distinct().order_by('norma_iso'))
        normas_count = len(normas)
        agg_fuerza = Carta.objects.aggregate(avg=Avg('fuerza'))['avg']
        fuerza_promedio = round(agg_fuerza) if agg_fuerza is not None else 0
        pct_activas = round((activas / total * 100), 1) if total > 0 else 0.0

        cartas_list = list(Carta.objects.all().order_by('id'))

        extra_context.update({
            'kpi_total_cartas': total,
            'kpi_cartas_activas': activas,
            'kpi_pct_activas': pct_activas,
            'kpi_normas_count': normas_count,
            'kpi_fuerza_promedio': fuerza_promedio,
            'normas_list': normas,
            'estados_choices': EstadoEntidadChoices.choices,
            'cartas_list': cartas_list,
        })
        return super().changelist_view(request, extra_context=extra_context)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        from core.models import EstadoEntidadChoices

        carta_obj = None
        if object_id:
            try:
                carta_obj = Carta.objects.get(pk=object_id)
            except Carta.DoesNotExist:
                carta_obj = None

        extra_context.update({
            'normas_choices': NORMA_ISO_CHOICES,
            'estados_choices': EstadoEntidadChoices.choices,
            'carta_obj': carta_obj,
            'is_edit': object_id is not None,
        })
        return super().changeform_view(request, object_id=object_id, form_url=form_url, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        """
        Guarda la carta registrando auditoría forense inmutable.
        """
        datos_anteriores = {}
        if change and obj.pk:
            try:
                antiguo = Carta.objects.get(pk=obj.pk)
                datos_anteriores = serialize_instance(antiguo)
            except Carta.DoesNotExist:
                pass

        super().save_model(request, obj, form, change)
        datos_nuevos = serialize_instance(obj)

        registrar_auditoria(
            admin=request.user,
            accion=AccionAuditoriaChoices.EDITAR if change else AccionAuditoriaChoices.CREAR,
            modulo_afectado='Carta',
            registro_id=str(obj.pk),
            datos_anteriores=datos_anteriores,
            datos_nuevos=datos_nuevos,
            request=request
        )

    def delete_model(self, request, obj):
        """
        Elimina la carta registrando auditoría forense inmutable.
        """
        obj_pk = str(obj.pk)
        datos_anteriores = serialize_instance(obj)
        super().delete_model(request, obj)

        registrar_auditoria(
            admin=request.user,
            accion=AccionAuditoriaChoices.ELIMINAR,
            modulo_afectado='Carta',
            registro_id=obj_pk,
            datos_anteriores=datos_anteriores,
            datos_nuevos={},
            request=request
        )


@admin.register(FaseCartaOpcion)
class FaseCartaOpcionAdmin(admin.ModelAdmin):
    """
    Gestión interactiva y visual de barajas/opciones de cartas asignadas a cada fase de caso.
    Permite filtrar en cascada por Mundo -> Nivel -> Fase, y gestionar hasta 5 cartas activas.
    """
    change_list_template = "admin/core/fasecartaopcion/change_list.html"
    list_display = ('fase', 'carta', 'es_solucion_correcta')
    list_filter = ('es_solucion_correcta', 'fase__nivel__mundo')
    search_fields = ('fase__titulo_incidente', 'carta__nombre')
    autocomplete_fields = ['fase', 'carta']

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        import json

        mundos_qs = list(Mundo.objects.all().order_by('orden'))

        # Parámetros seleccionados
        mundo_id_param = request.GET.get('mundo_id')
        nivel_id_param = request.GET.get('nivel_id')
        fase_id_param = request.GET.get('fase_id')

        selected_mundo = None
        if mundo_id_param and str(mundo_id_param).isdigit():
            selected_mundo = Mundo.objects.filter(pk=int(mundo_id_param)).first()
        if not selected_mundo and mundos_qs:
            selected_mundo = mundos_qs[0]

        # Niveles del mundo seleccionado
        niveles_qs = []
        selected_nivel = None
        if selected_mundo:
            niveles_qs = list(Nivel.objects.filter(mundo=selected_mundo).order_by('numero_nivel'))
            if nivel_id_param and str(nivel_id_param).isdigit():
                selected_nivel = Nivel.objects.filter(pk=int(nivel_id_param), mundo=selected_mundo).first()
            if not selected_nivel and niveles_qs:
                # Priorizar nivel que tenga fases si es posible
                nivel_con_fases = next((n for n in niveles_qs if n.fases.exists()), None)
                selected_nivel = nivel_con_fases or niveles_qs[0]

        # Fases del nivel seleccionado
        fases_qs = []
        selected_fase = None
        if selected_nivel:
            fases_qs = list(FaseCaso.objects.filter(nivel=selected_nivel).order_by('numero_fase'))
            if fase_id_param and str(fase_id_param).isdigit():
                selected_fase = FaseCaso.objects.filter(pk=int(fase_id_param), nivel=selected_nivel).first()
            if not selected_fase and fases_qs:
                selected_fase = fases_qs[0]

        # Cartas asignadas a la fase seleccionada
        cartas_asignadas = []
        cartas_asignadas_data = []
        if selected_fase:
            cartas_asignadas = list(
                FaseCartaOpcion.objects.filter(fase=selected_fase)
                .select_related('carta')
                .order_by('id')
            )
            for op in cartas_asignadas:
                cartas_asignadas_data.append({
                    'carta_id': op.carta.id,
                    'nombre': op.carta.nombre,
                    'norma_iso': op.carta.norma_iso,
                    'concepto': op.carta.concepto,
                    'descripcion': op.carta.descripcion,
                    'imagen_url': op.carta.imagen_url,
                    'fuerza': op.carta.fuerza,
                    'defensa': op.carta.defensa,
                    'es_solucion_correcta': op.es_solucion_correcta,
                })

        # Catálogo de cartas activas con información de uso en fases
        cartas_activas_qs = (
            Carta.objects.filter(estado=EstadoEntidadChoices.ACTIVO)
            .prefetch_related('usada_en_fases__fase__nivel__mundo')
            .order_by('norma_iso', 'nombre')
        )
        cartas_activas_data = []
        for c in cartas_activas_qs:
            usos = [
                {
                    'fase_id': op.fase_id,
                    'mundo_codigo': op.fase.nivel.mundo.codigo_iso,
                    'nivel_numero': op.fase.nivel.numero_nivel,
                    'fase_numero': op.fase.numero_fase,
                    'fase_titulo': op.fase.titulo_incidente,
                }
                for op in c.usada_en_fases.all()
            ]
            cartas_activas_data.append({
                'id': c.id,
                'nombre': c.nombre,
                'norma_iso': c.norma_iso,
                'concepto': c.concepto,
                'descripcion': c.descripcion,
                'imagen_url': c.imagen_url,
                'fuerza': c.fuerza,
                'defensa': c.defensa,
                'estado': c.estado,
                'usos': usos,
                'usos_count': len(usos),
            })

        # Serialización de mundos, niveles y fases para reactividad instantánea JS
        jerarquia = []
        for m in mundos_qs:
            m_niveles = []
            for n in m.niveles.all().order_by('numero_nivel'):
                n_fases = [
                    {
                        'id': f.id,
                        'numero_fase': f.numero_fase,
                        'titulo_incidente': f.titulo_incidente,
                        'amenaza': f.amenaza,
                        'dificultad': f.dificultad,
                        'cartas_count': f.opciones_cartas.count(),
                    }
                    for f in n.fases.all().order_by('numero_fase')
                ]
                m_niveles.append({
                    'id': n.id,
                    'numero_nivel': n.numero_nivel,
                    'titulo': n.titulo,
                    'dificultad': n.dificultad,
                    'dificultad_display': n.get_dificultad_display(),
                    'fases': n_fases,
                })
            jerarquia.append({
                'id': m.id,
                'codigo_iso': m.codigo_iso,
                'nombre_tematico': m.nombre_tematico,
                'niveles': m_niveles,
            })

        extra_context.update({
            'mundos_list': mundos_qs,
            'selected_mundo': selected_mundo,
            'niveles_list': niveles_qs,
            'selected_nivel': selected_nivel,
            'fases_list': fases_qs,
            'selected_fase': selected_fase,
            'cartas_asignadas': cartas_asignadas,
            'cartas_asignadas_count': len(cartas_asignadas),
            'cartas_asignadas_json': json.dumps(cartas_asignadas_data),
            'cartas_activas': cartas_activas_qs,
            'cartas_activas_json': json.dumps(cartas_activas_data),
            'jerarquia_json': json.dumps(jerarquia),
        })

        return super().changelist_view(request, extra_context=extra_context)


# ==============================================================================
# ADMIN MÓDULO 4: ANALÍTICA Y RENDIMIENTO
# ==============================================================================

@admin.register(PartidaJugada)
class PartidaJugadaAdmin(admin.ModelAdmin):
    """
    Bitácora de partidas jugadas con analítica y telemetría de rendimiento Dark SaaS / ISO QUEST.
    """
    change_list_template = "admin/core/partidajugada/change_list.html"
    list_display = (
        'usuario',
        'nivel',
        'badge_resultado',
        'oro_obtenido',
        'gemas_obtenidas',
        'fecha_partida',
    )
    list_filter = ('resultado', 'fecha_partida', 'nivel__mundo')
    search_fields = ('usuario__alias', 'usuario__correo', 'nivel__titulo')
    date_hierarchy = 'fecha_partida'
    ordering = ('-fecha_partida',)

    @admin.display(description="Resultado")
    def badge_resultado(self, obj):
        colors = {
            'victoria': '#16a34a',
            'derrota': '#dc2626',
            'abandonada': '#d97706',
        }
        color = colors.get(obj.resultado, '#6b7280')
        return format_html(
            '<span style="background:{}; color:#fff; padding:3px 10px; border-radius:12px; font-weight:700; font-size:11px;">{}</span>',
            color,
            obj.get_resultado_display().upper()
        )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        import json
        import datetime
        from django.core.paginator import Paginator
        from django.db.models import Sum, Q

        usuario_id = request.GET.get('usuario')
        mundo_id = request.GET.get('mundo')
        nivel_id = request.GET.get('nivel')
        dias_param = request.GET.get('dias', '30')

        qs = PartidaJugada.objects.select_related('usuario', 'nivel', 'nivel__mundo').all().order_by('-fecha_partida')

        if usuario_id:
            qs = qs.filter(usuario_id=usuario_id)
        if mundo_id:
            qs = qs.filter(nivel__mundo_id=mundo_id)
        if nivel_id:
            qs = qs.filter(nivel_id=nivel_id)

        now = timezone.now()
        if dias_param == '7':
            qs = qs.filter(fecha_partida__gte=now - datetime.timedelta(days=7))
        elif dias_param == '1':
            qs = qs.filter(fecha_partida__gte=now - datetime.timedelta(days=1))
        elif dias_param == '30':
            qs = qs.filter(fecha_partida__gte=now - datetime.timedelta(days=30))

        # Métricas calculadas en base a datos reales de la base de datos
        total_db = qs.count()
        kpi_total = f"{total_db:,}"
        vics = qs.filter(resultado='victoria').count()
        derts = qs.filter(resultado='derrota').count()
        abands = qs.filter(resultado='abandonada').count()
        tasa = round((vics / total_db * 100), 1) if total_db > 0 else 0.0
        oro_sum = qs.aggregate(s=Sum('oro_obtenido'))['s'] or 0
        gemas_sum = qs.aggregate(s=Sum('gemas_obtenidas'))['s'] or 0
        kpi_oro = f"{oro_sum:,}"
        kpi_gemas = f"{gemas_sum:,}"
        oro_prom = round(oro_sum / total_db) if total_db > 0 else 0
        gemas_prom = round(gemas_sum / total_db) if total_db > 0 else 0

        # Donut progress proporcional real (perímetro 238.76)
        dash_len = round((tasa / 100.0) * 238.76, 1)
        donut_dash_array = f"{dash_len} 239"

        # Tendencia semanal real (últimas 4 semanas S1 a S4)
        c4 = qs.filter(fecha_partida__gte=now - datetime.timedelta(days=7)).count()
        c3 = qs.filter(fecha_partida__gte=now - datetime.timedelta(days=14), fecha_partida__lt=now - datetime.timedelta(days=7)).count()
        c2 = qs.filter(fecha_partida__gte=now - datetime.timedelta(days=21), fecha_partida__lt=now - datetime.timedelta(days=14)).count()
        c1 = qs.filter(fecha_partida__gte=now - datetime.timedelta(days=28), fecha_partida__lt=now - datetime.timedelta(days=21)).count()

        max_c = max(c1, c2, c3, c4, 1)
        y1 = 75 - round((c1 / max_c) * 50)
        y2 = 75 - round((c2 / max_c) * 50)
        y3 = 75 - round((c3 / max_c) * 50)
        y4 = 75 - round((c4 / max_c) * 50)

        trend_path = f"M10,{y1} Q60,{(y1+y2)//2} 105,{y2} T200,{y3} T310,{y4}"
        trend_area = f"M10,{y1} Q60,{(y1+y2)//2} 105,{y2} T200,{y3} T310,{y4} L310,85 L10,85 Z"

        top_nivel = qs.values('nivel__numero_nivel', 'nivel__titulo').annotate(c=Count('id')).order_by('-c').first()
        if top_nivel and total_db > 0:
            top_num = top_nivel['nivel__numero_nivel'] or 1
            top_tit = top_nivel['nivel__titulo'] or "General"
            top_pct = f"{round((top_nivel['c'] / total_db) * 100)}%"
            top_count = top_nivel['c']
        else:
            top_num = 1
            top_tit = "Sin partidas"
            top_pct = "0%"
            top_count = 0

        # Paginación
        paginator = Paginator(qs, 10)
        page_number = request.GET.get('page', 1)
        partidas_page = paginator.get_page(page_number)

        usuarios_list = list(Usuario.objects.all().order_by('alias'))
        mundos_list = list(Mundo.objects.all().order_by('orden'))
        niveles_list = list(Nivel.objects.all().order_by('mundo__orden', 'numero_nivel'))
        niveles_data = [{'id': n.id, 'mundo_id': n.mundo_id, 'numero_nivel': n.numero_nivel, 'titulo': n.titulo} for n in niveles_list]

        extra_context.update({
            'kpi_total_partidas': kpi_total,
            'kpi_tasa_victoria': tasa,
            'kpi_oro_total': kpi_oro,
            'kpi_gemas_totales': kpi_gemas,
            'kpi_sub_total': f"{vics}V / {derts}D / {abands}A",
            'kpi_sub_tasa': f"{vics} de {total_db} victorias",
            'kpi_sub_oro': f"Prom: +{oro_prom} por partida",
            'kpi_sub_gemas': f"Prom: +{gemas_prom} por partida",
            'kpi_victorias': vics,
            'kpi_derrotas': derts,
            'kpi_abandonadas': abands,
            'donut_dash_array': donut_dash_array,
            'trend_path': trend_path,
            'trend_area': trend_area,
            'y1': y1,
            'y2': y2,
            'y3': y3,
            'y4': y4,
            'weekly_c1': c1,
            'weekly_c2': c2,
            'weekly_c3': c3,
            'weekly_c4': c4,
            'top_nivel_numero': top_num,
            'top_nivel_titulo': top_tit,
            'top_nivel_pct': top_pct,
            'top_nivel_count': top_count,
            'partidas_page': partidas_page,
            'total_partidas_display': total_db,
            'usuarios_list': usuarios_list,
            'mundos_list': mundos_list,
            'niveles_list': niveles_list,
            'niveles_json': json.dumps(niveles_data),
            'selected_usuario': usuario_id or '',
            'selected_mundo': mundo_id or '',
            'selected_nivel': nivel_id or '',
            'selected_dias': dias_param or '30',
        })
        return super().changelist_view(request, extra_context=extra_context)


# ==============================================================================
# ADMIN MÓDULO 5: AUDITORÍA INMUTABLE (SOLO LECTURA)
# ==============================================================================

@admin.register(RegistroAuditoria)
class RegistroAuditoriaAdmin(admin.ModelAdmin):
    """
    Registro Forense e Inmutable de Auditoría.
    Se bloquean estrictamente los permisos de creación, modificación y eliminación
    (has_add_permission=False, has_change_permission=False, has_delete_permission=False).
    """
    change_list_template = "admin/core/registroauditoria/change_list.html"
    list_display = (
        'created_at',
        'admin',
        'badge_accion',
        'modulo_afectado',
        'registro_id',
        'direccion_ip',
    )
    list_filter = ('accion', 'modulo_afectado', 'created_at')
    search_fields = (
        'modulo_afectado',
        'registro_id',
        'direccion_ip',
        'admin__alias',
        'admin__correo',
    )
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    # Campos de solo lectura
    readonly_fields = (
        'created_at',
        'admin',
        'accion',
        'modulo_afectado',
        'registro_id',
        'datos_anteriores',
        'datos_nuevos',
        'direccion_ip',
    )

    # --------------------------------------------------------------------------
    # RESTRICCIÓN DE SEGURIDAD: INMUTABILIDAD ESTRICTA
    # --------------------------------------------------------------------------
    def has_add_permission(self, request):
        """Bloquea la adición manual desde el panel."""
        return False

    def has_change_permission(self, request, obj=None):
        """Bloquea la edición o modificación de registros existentes."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Bloquea la eliminación de registros de la bitácora."""
        return False

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        import json
        import datetime
        from django.core.paginator import Paginator

        rango_param = request.GET.get('rango', '30')
        usuario_param = request.GET.get('usuario', '')
        modulo_param = request.GET.get('modulo', '')
        accion_param = request.GET.get('accion', '')

        qs = RegistroAuditoria.objects.select_related('admin').all().order_by('-created_at')

        # Filtro de rango de fechas
        now = timezone.now()
        if rango_param == 'hoy':
            inicio_hoy = now.replace(hour=0, minute=0, second=0, microsecond=0)
            qs = qs.filter(created_at__gte=inicio_hoy)
        elif rango_param == '7':
            qs = qs.filter(created_at__gte=now - datetime.timedelta(days=7))
        elif rango_param == '30':
            qs = qs.filter(created_at__gte=now - datetime.timedelta(days=30))
        # 'todo' no filtra por fecha

        # Filtro de usuario
        if usuario_param and usuario_param != 'todos' and str(usuario_param).isdigit():
            qs = qs.filter(admin_id=int(usuario_param))

        # Filtro de módulo
        if modulo_param and modulo_param != 'todos':
            qs = qs.filter(modulo_afectado__icontains=modulo_param)

        # Filtro de acción
        if accion_param and accion_param != 'todas':
            qs = qs.filter(accion=accion_param)

        # Paginación (8 registros por página)
        paginator = Paginator(qs, 8)
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        # Usuarios administradores para el filtro
        usuarios_list = list(
            Usuario.objects.filter(is_staff=True).order_by('alias')
        )
        if not usuarios_list:
            usuarios_list = list(Usuario.objects.all().order_by('alias')[:10])

        # Módulos disponibles
        modulos_disponibles = [
            {'valor': 'Cartas', 'nombre': 'Cartas'},
            {'valor': 'Usuarios', 'nombre': 'Usuarios'},
            {'valor': 'Fases', 'nombre': 'Fases'},
            {'valor': 'Niveles', 'nombre': 'Niveles'},
            {'valor': 'Mundos', 'nombre': 'Mundos'},
            {'valor': 'Barajas', 'nombre': 'Barajas'},
            {'valor': 'Sistema', 'nombre': 'Sistema'},
            {'valor': 'Progreso', 'nombre': 'Progreso'},
        ]

        # Acciones disponibles
        acciones_disponibles = [
            {'valor': 'EDITAR', 'nombre': 'EDITAR'},
            {'valor': 'ELIMINAR', 'nombre': 'ELIMINAR'},
            {'valor': 'CAMBIAR_CONFIG', 'nombre': 'CAMBIAR_CONFIG'},
            {'valor': 'REINICIAR_PROGRESO', 'nombre': 'REINICIAR_PROGRESO'},
            {'valor': 'CREAR', 'nombre': 'CREAR'},
        ]

        # Registro seleccionado por defecto (el primero de la página actual)
        selected_registro = page_obj.object_list[0] if len(page_obj.object_list) > 0 else None

        # Serialización de registros de la página para interactividad
        registros_json = []
        for r in page_obj.object_list:
            registros_json.append({
                'id': r.id,
                'created_at_formatted': r.created_at.strftime('%d/%m/%Y - %H:%M'),
                'created_at_full': r.created_at.strftime('%d/%m/%Y - %H:%M:%S'),
                'admin_alias': r.admin_alias,
                'admin_avatar_url': r.admin_avatar_url,
                'accion': r.accion,
                'accion_display': r.get_accion_display(),
                'modulo_display': r.modulo_display,
                'registro_codigo': r.registro_codigo,
                'direccion_ip': r.direccion_ip or '127.0.0.1',
                'datos_anteriores': r.datos_anteriores or {},
                'datos_nuevos': r.datos_nuevos or {},
            })

        extra_context.update({
            'page_obj': page_obj,
            'total_registros': paginator.count,
            'selected_registro': selected_registro,
            'registros_json': json.dumps(registros_json),
            'usuarios_list': usuarios_list,
            'modulos_disponibles': modulos_disponibles,
            'acciones_disponibles': acciones_disponibles,
            'selected_rango': rango_param,
            'selected_usuario': usuario_param,
            'selected_modulo': modulo_param,
            'selected_accion': accion_param,
        })
        return super().changelist_view(request, extra_context=extra_context)

    @admin.display(description="Acción")
    def badge_accion(self, obj):
        colors = {
            AccionAuditoriaChoices.REINICIAR_PROGRESO: '#dc2626',
            AccionAuditoriaChoices.CAMBIAR_CONFIG: '#d97706',
            AccionAuditoriaChoices.EDITAR: '#2563eb',
            AccionAuditoriaChoices.ELIMINAR: '#991b1b',
        }
        color = colors.get(obj.accion, '#374151')
        return format_html(
            '<span style="background:{}; color:#fff; padding:3px 8px; border-radius:10px; font-weight:600; font-size:11px;">{}</span>',
            color,
            obj.get_accion_display()
        )


# ==============================================================================
# ADMIN MÓDULO 6: PARÁMETROS GLOBALES
# ==============================================================================

@admin.register(ParametroGlobal)
class ParametroGlobalAdmin(admin.ModelAdmin):
    """
    Administración de Variables Globales de Balance y Economía.
    Cada cambio es registrado automáticamente en RegistroAuditoria.
    """
    change_list_template = "admin/core/parametroglobal/change_list.html"
    list_display = ('categoria', 'clave', 'valor', 'descripcion', 'updated_at')
    list_filter = ('categoria',)
    search_fields = ('clave', 'descripcion', 'categoria')
    ordering = ('categoria', 'clave')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        all_params = ParametroGlobal.objects.all().order_by('id')
        extra_context['parametros_lista'] = all_params
        extra_context['vidas_count'] = ParametroGlobal.objects.filter(categoria__iexact='Vidas').count()
        extra_context['jerarquia_count'] = ParametroGlobal.objects.filter(
            Q(categoria__iexact='Jerarquia') | Q(categoria__iexact='Jerarquía')
        ).count()
        extra_context['economia_count'] = ParametroGlobal.objects.filter(
            Q(categoria__iexact='Economia') | Q(categoria__iexact='Economía')
        ).count()
        extra_context['seguridad_count'] = ParametroGlobal.objects.filter(categoria__iexact='Seguridad').count()
        extra_context['logros_count'] = ParametroGlobal.objects.filter(categoria__iexact='Logros').count()
        extra_context['total_params'] = all_params.count()
        return super().changelist_view(request, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        """
        Sobrescribe el guardado para auditar cambios de configuración en la bitácora.
        """
        datos_anteriores = None
        if change:
            try:
                antiguo = ParametroGlobal.objects.get(pk=obj.pk)
                datos_anteriores = serialize_instance(antiguo)
            except ParametroGlobal.DoesNotExist:
                pass

        super().save_model(request, obj, form, change)

        # Sincronizar efectos reales e inmediatos en el juego
        sincronizar_efecto_parametro_global(obj)

        datos_nuevos = serialize_instance(obj)
        registrar_auditoria(
            admin=request.user,
            accion=AccionAuditoriaChoices.CAMBIAR_CONFIG,
            modulo_afectado='ParametroGlobal',
            registro_id=str(obj.pk),
            datos_anteriores=datos_anteriores,
            datos_nuevos=datos_nuevos,
            request=request
        )

    def delete_model(self, request, obj):
        """
        Audita la eliminación de un parámetro global.
        """
        datos_anteriores = serialize_instance(obj)
        obj_pk = str(obj.pk)
        super().delete_model(request, obj)

        registrar_auditoria(
            admin=request.user,
            accion=AccionAuditoriaChoices.ELIMINAR,
            modulo_afectado='ParametroGlobal',
            registro_id=obj_pk,
            datos_anteriores=datos_anteriores,
            datos_nuevos=None,
            request=request
        )
