"""
Modelos de Datos - Backend del Videojuego de Capacitación ISO y Compliance.
Define los 6 módulos arquitectónicos requeridos con Django 5.x y SQLite3.
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError
from django.utils import timezone


# ==============================================================================
# ENUMERACIONES / TEXT CHOICES
# ==============================================================================

class RolUsuarioChoices(models.TextChoices):
    ADMINISTRADOR = 'administrador', 'Administrador'
    EMPLEADO_JUGADOR = 'empleado_jugador', 'Empleado / Jugador'


class EstadoUsuarioChoices(models.TextChoices):
    ACTIVO = 'activo', 'Activo'
    INACTIVO = 'inactivo', 'Inactivo'


class EstadoEntidadChoices(models.TextChoices):
    ACTIVO = 'activo', 'Activo'
    INACTIVO = 'inactivo', 'Inactivo'


class DificultadChoices(models.TextChoices):
    FACIL = 'facil', 'Fácil'
    NORMAL = 'normal', 'Normal'
    DIFICIL = 'dificil', 'Difícil'


class TipoNivelChoices(models.TextChoices):
    NORMAL = 'normal', 'Nivel Estándar'
    JEFE = 'jefe', 'Jefe / Auditoría Crítica'


class ResultadoPartidaChoices(models.TextChoices):
    VICTORIA = 'victoria', 'Victoria'
    DERROTA = 'derrota', 'Derrota'
    ABANDONADA = 'abandonada', 'Abandonada'


class AccionAuditoriaChoices(models.TextChoices):
    CREAR = 'CREAR', 'Crear Registro'
    EDITAR = 'EDITAR', 'Modificar Registro'
    ELIMINAR = 'ELIMINAR', 'Eliminar Registro'
    CAMBIAR_CONFIG = 'CAMBIAR_CONFIG', 'Cambiar Parámetro de Configuración'
    REINICIAR_PROGRESO = 'REINICIAR_PROGRESO', 'Reiniciar Progreso de Jugador'


# ==============================================================================
# MÓDULO 1: USUARIOS Y PROGRESO
# ==============================================================================

class UsuarioManager(BaseUserManager):
    """
    Gestor de usuarios personalizado con soporte para autenticación por correo electrónico
    y conservación del alias/perfil organizacional para compliance.
    """
    def create_user(self, correo, alias, nombre_completo, password=None, **extra_fields):
        if not correo:
            raise ValueError('El correo electrónico es obligatorio.')
        if not alias:
            raise ValueError('El alias del jugador es obligatorio.')

        correo = self.normalize_email(correo).lower()
        extra_fields.setdefault('rol', RolUsuarioChoices.EMPLEADO_JUGADOR)
        extra_fields.setdefault('estado', EstadoUsuarioChoices.ACTIVO)
        extra_fields.setdefault('is_active', True)

        user = self.model(
            correo=correo,
            alias=alias.strip(),
            nombre_completo=nombre_completo.strip(),
            **extra_fields
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, alias, nombre_completo, password=None, **extra_fields):
        extra_fields.setdefault('rol', RolUsuarioChoices.ADMINISTRADOR)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('area', 'Dirección de TI / Compliance')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(correo, alias, nombre_completo, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de Usuario institucional y jugador de la plataforma de compliance.
    Extiende AbstractBaseUser y PermissionsMixin para integrarse transparentemente con Django Admin.
    """
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    nombre_completo = models.CharField(max_length=150, verbose_name="Nombre Completo")
    alias = models.CharField(max_length=50, unique=True, verbose_name="Alias / Gamertag")
    correo = models.EmailField(max_length=150, unique=True, verbose_name="Correo Electrónico")
    area = models.CharField(max_length=100, verbose_name="Área Organizacional (ej. Compliance, TI, Legal)")
    rol = models.CharField(
        max_length=30,
        choices=RolUsuarioChoices.choices,
        default=RolUsuarioChoices.EMPLEADO_JUGADOR,
        verbose_name="Rol en Plataforma"
    )
    estado = models.CharField(
        max_length=20,
        choices=EstadoUsuarioChoices.choices,
        default=EstadoUsuarioChoices.ACTIVO,
        verbose_name="Estado de Cuenta"
    )
    avatar_personalizado = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Avatar Seleccionado (Ruta o Nombre)"
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="Acceso al Panel de Administración",
        help_text="Define si el usuario puede acceder a este panel de Django."
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Usuario Activo en Autenticación"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['alias', 'nombre_completo']

    class Meta:
        db_table = 'core_usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = '1. Usuarios y Colaboradores'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nombre_completo} ({self.alias}) - {self.area} [{self.get_rol_display()}]"

    def clean(self):
        super().clean()
        if self.rol == RolUsuarioChoices.ADMINISTRADOR:
            self.is_staff = True

    @property
    def avatar_url(self):
        """
        Retorna la URL estática del avatar nigromante ilustrado correspondiente al usuario.
        Garantiza que la asignación sea exactamente fiel a los 5 personajes nigromantes proporcionados.
        Si el usuario eligió un avatar personalizado, lo prioriza.
        """
        if self.avatar_personalizado:
            av = str(self.avatar_personalizado).strip()
            if av.startswith('/'):
                return av
            if av.startswith('necromancer_'):
                return f'/static/img/avatars/{av}'
            return f'/static/img/avatars/{av}'

        mapping = {
            'juanperez': 'necromancer_1.png',
            'andresM': 'necromancer_1.png',
            'mariaLT': 'necromancer_2.png',
            'valec': 'necromancer_2.png',
            'carlosg': 'necromancer_3.png',
            'AdminCompliance': 'necromancer_3.png',
            'admin': 'necromancer_3.png',
            'AuditMaster': 'necromancer_3.png',
            'anar': 'necromancer_4.png',
            'sofiaM': 'necromancer_4.png',
            'camirojas': 'necromancer_4.png',
            'InactivaUser': 'necromancer_4.png',
            'luisf': 'necromancer_5.png',
            'diegoH': 'necromancer_5.png',
            'DataSentry': 'necromancer_5.png',
            'RiskHunter': 'necromancer_1.png',
            'CyberGuard': 'necromancer_5.png',
            'LexProtect': 'necromancer_2.png',
        }
        alias = getattr(self, 'alias', '') or ''
        if alias in mapping:
            file_name = mapping[alias]
        else:
            seed = sum(ord(c) for c in alias) + (getattr(self, 'id', 0) or 1)
            idx = (seed % 5) + 1
            file_name = f'necromancer_{idx}.png'
        return f'/static/img/avatars/{file_name}'


class ProgresoUsuario(models.Model):
    """
    Progreso, economía y estado de vidas del colaborador en el juego.
    """
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='progreso',
        verbose_name="Usuario Colaborador"
    )
    nivel = models.IntegerField(default=1, verbose_name="Nivel de Jugador")
    xp = models.BigIntegerField(default=0, verbose_name="Puntos de Experiencia (XP)")
    oro = models.IntegerField(default=0, verbose_name="Monedas de Oro")
    gemas = models.IntegerField(default=0, verbose_name="Gemas de Cumplimiento")
    vidas_actuales = models.IntegerField(default=3, verbose_name="Vidas Actuales")
    ultimo_reinicio_vidas = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Último Reinicio de Vidas"
    )
    ultimo_reinicio_progreso = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Último Reinicio Administrativo de Progreso"
    )

    class Meta:
        db_table = 'core_progreso_usuario'
        verbose_name = 'Progreso de Jugador'
        verbose_name_plural = '1.1 Progresos de Jugadores'
        ordering = ['-xp', '-nivel']

    def __str__(self):
        return f"Progreso de {self.usuario.alias} (Nivel {self.nivel} | {self.xp} XP | {self.vidas_actuales} Vidas)"

    @property
    def avatar_url(self):
        return self.usuario.avatar_url if self.usuario else '/static/img/avatars/necromancer_1.png'


# ==============================================================================
# MÓDULO 2: CONTENIDO (MUNDOS, NIVELES Y FASES)
# ==============================================================================

class Mundo(models.Model):
    """
    Representa un ecosistema o norma de cumplimiento ISO (ej. ISO 27001 Seguridad, ISO 9001 Calidad).
    """
    orden = models.IntegerField(verbose_name="Orden de Despliegue en Mapa")
    codigo_iso = models.CharField(max_length=50, verbose_name="Código de Norma ISO (ej. ISO 27001)")
    nombre_tematico = models.CharField(max_length=100, verbose_name="Nombre Temático del Mundo")
    dominio = models.CharField(max_length=100, verbose_name="Dominio Temático / Área de Seguridad")
    dificultad = models.CharField(
        max_length=20,
        choices=DificultadChoices.choices,
        default=DificultadChoices.NORMAL,
        verbose_name="Nivel de Dificultad"
    )
    estado = models.CharField(
        max_length=20,
        choices=EstadoEntidadChoices.choices,
        default=EstadoEntidadChoices.ACTIVO,
        verbose_name="Estado de Publicación"
    )

    class Meta:
        db_table = 'core_mundo'
        verbose_name = 'Mundo ISO'
        verbose_name_plural = '2. Mundos ISO'
        ordering = ['orden']

    def __str__(self):
        return f"Mundo {self.orden}: {self.codigo_iso} - {self.nombre_tematico}"

    @property
    def imagen_url(self):
        """
        Retorna la imagen temática del Mundo ISO.
        """
        code = (self.codigo_iso or '').replace(' ', '').lower()
        if '27017' in code:
            return '/static/img/mundos/mundo_iso27017.png'
        elif '27001' in code:
            return '/static/img/mundos/mundo_iso27001.png'
        elif '20000' in code:
            return '/static/img/mundos/mundo_iso20000.png'
        elif '22301' in code:
            return '/static/img/mundos/mundo_iso22301.png'
        elif '37301' in code or '37001' in code:
            return '/static/img/mundos/mundo_iso37301.png'
        elif '9001' in code:
            return '/static/img/mundos/mundo_iso9001.png'
        elif '14001' in code:
            return '/static/img/mundos/mundo_iso14001.png'
        return '/static/img/mundos/mundo_iso27001.png'

    @property
    def nombre_corto(self):
        """
        Retorna el nombre temático resumido para las tarjetas superiores.
        """
        code = (self.codigo_iso or '').replace(' ', '').lower()
        if '27017' in code:
            return 'Seguridad Cloud'
        elif '27001' in code:
            return 'Ciberseguridad'
        elif '20000' in code:
            return 'Servicios TI'
        elif '22301' in code:
            return 'Continuidad'
        elif '37301' in code or '37001' in code:
            return 'Ética y Cumplimiento'
        elif '9001' in code:
            return 'Calidad'
        elif '14001' in code:
            return 'Planeta Sostenible'
        return self.nombre_tematico

    @property
    def descripcion_tematica(self):
        """
        Retorna la descripción narrativa del mundo ISO para el banner destacado.
        """
        code = (self.codigo_iso or '').replace(' ', '').lower()
        if '27017' in code:
            return 'Asegura los controles de seguridad para la provisión y uso de servicios de computación en la nube.'
        elif '27001' in code:
            return 'Protege la confidencialidad, integridad y disponibilidad de la información según ISO/IEC 27001:2022.'
        elif '20000' in code:
            return 'Optimiza el diseño, entrega, soporte y gestión integral de los servicios de TI (ITSM).'
        elif '22301' in code:
            return 'Garantiza la resiliencia operativa y rápida recuperación ante contingencias críticas del negocio.'
        elif '37301' in code or '37001' in code:
            return 'Garantiza las conductas éticas, transparencia y prevención de actos ilícitos en la organización.'
        elif '9001' in code:
            return 'Optimiza la calidad de los procesos organizacionales y la excelencia operativa continua.'
        elif '14001' in code:
            return 'Fomenta la sostenibilidad ambiental, gestión ecológica de recursos y reducción de huella de carbono.'
        return f"Módulo de capacitación en {self.nombre_tematico} enfocado en {self.dominio}."

    @property
    def icono_class(self):
        """
        Icono representativo de cada norma ISO para las tarjetas del selector superior.
        """
        code = (self.codigo_iso or '').replace(' ', '').lower()
        if '27017' in code:
            return 'bi bi-cloud-check'
        elif '27001' in code:
            return 'bi bi-shield-check'
        elif '20000' in code:
            return 'bi bi-hdd-network'
        elif '22301' in code:
            return 'bi bi-life-preserver'
        elif '37301' in code or '37001' in code:
            return 'bi bi-shield-check'
        elif '9001' in code:
            return 'bi bi-patch-check'
        elif '14001' in code:
            return 'bi bi-globe-americas'
        return 'bi bi-cpu'

    @property
    def avatar_guardia_url(self):
        """
        Avatar ilustrado del nigromante guardián para el hero banner de este mundo.
        """
        avatars = [
            '/static/img/avatars/necromancer_3.png',
            '/static/img/avatars/necromancer_2.png',
            '/static/img/avatars/necromancer_1.png',
            '/static/img/avatars/necromancer_4.png',
            '/static/img/avatars/necromancer_5.png',
        ]
        idx = ((self.orden or 1) - 1) % len(avatars)
        return avatars[idx]


class Nivel(models.Model):
    """
    Etapa dentro de un Mundo ISO. Puede ser estándar o enfrentamiento con Jefe/Auditoría crítica.
    """
    mundo = models.ForeignKey(
        Mundo,
        on_delete=models.CASCADE,
        related_name='niveles',
        verbose_name="Mundo Perteneciente"
    )
    numero_nivel = models.IntegerField(verbose_name="Número de Nivel")
    titulo = models.CharField(max_length=120, verbose_name="Título del Nivel")
    tipo = models.CharField(
        max_length=20,
        choices=TipoNivelChoices.choices,
        default=TipoNivelChoices.NORMAL,
        verbose_name="Tipo de Nivel"
    )
    dificultad = models.CharField(
        max_length=20,
        choices=DificultadChoices.choices,
        default=DificultadChoices.NORMAL,
        verbose_name="Dificultad"
    )
    recompensa_oro = models.IntegerField(default=50, verbose_name="Recompensa en Oro")
    recompensa_gemas = models.IntegerField(default=10, verbose_name="Recompensa en Gemas")
    recompensa_xp = models.IntegerField(default=100, verbose_name="Recompensa en XP")
    estado = models.CharField(
        max_length=20,
        choices=EstadoEntidadChoices.choices,
        default=EstadoEntidadChoices.ACTIVO,
        verbose_name="Estado de Activación"
    )

    class Meta:
        db_table = 'core_nivel'
        verbose_name = 'Nivel'
        verbose_name_plural = '2.1 Niveles'
        ordering = ['mundo', 'numero_nivel']
        unique_together = ('mundo', 'numero_nivel')

    def __str__(self):
        return f"[{self.mundo.codigo_iso}] Nivel {self.numero_nivel}: {self.titulo} ({self.get_tipo_display()})"


class FaseCaso(models.Model):
    """
    Incidente o caso específico planteado al jugador dentro de un Nivel.
    """
    nivel = models.ForeignKey(
        Nivel,
        on_delete=models.CASCADE,
        related_name='fases',
        verbose_name="Nivel Asociado"
    )
    numero_fase = models.IntegerField(verbose_name="Número de Fase / Incidente")
    titulo_incidente = models.CharField(max_length=150, verbose_name="Título del Incidente")
    caso_contexto = models.TextField(
        help_text="Contexto de la situación para el jugador",
        verbose_name="Contexto / Situación de Cumplimiento"
    )
    amenaza = models.CharField(
        max_length=100,
        verbose_name="Amenaza Identificada (ej. Fuga de datos, Phishing)"
    )
    dificultad = models.CharField(
        max_length=20,
        choices=DificultadChoices.choices,
        default=DificultadChoices.NORMAL,
        verbose_name="Dificultad de la Fase"
    )
    recompensa_oro = models.IntegerField(default=10, verbose_name="Recompensa Oro")
    recompensa_xp = models.IntegerField(default=20, verbose_name="Recompensa XP")
    estado = models.CharField(
        max_length=20,
        choices=EstadoEntidadChoices.choices,
        default=EstadoEntidadChoices.ACTIVO,
        verbose_name="Estado de la Fase"
    )

    class Meta:
        db_table = 'core_fase_caso'
        verbose_name = 'Fase de Caso / Incidente'
        verbose_name_plural = '2.2 Fases de Casos'
        ordering = ['nivel', 'numero_fase']
        unique_together = ('nivel', 'numero_fase')

    def __str__(self):
        return f"{self.nivel.titulo} - Fase {self.numero_fase}: {self.titulo_incidente}"


# ==============================================================================
# MÓDULO 3: CATÁLOGO DE CARTAS Y BARAJAS POR FASE
# ==============================================================================

class Carta(models.Model):
    """
    Carta de control o salvaguarda ISO que el jugador utiliza para mitigar incidentes.
    """
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Carta")
    norma_iso = models.CharField(max_length=50, verbose_name="Norma ISO de Referencia")
    concepto = models.CharField(max_length=150, verbose_name="Concepto / Control ISO")
    descripcion = models.TextField(verbose_name="Descripción Técnica / Pedagógica")
    imagen = models.ImageField(
        upload_to='cartas/',
        null=True,
        blank=True,
        verbose_name="Arte / Imagen de la Carta"
    )
    fuerza = models.IntegerField(verbose_name="Puntos de Mitigación / Fuerza")
    defensa = models.IntegerField(verbose_name="Puntos de Cumplimiento / Defensa")
    estado = models.CharField(
        max_length=20,
        choices=EstadoEntidadChoices.choices,
        default=EstadoEntidadChoices.ACTIVO,
        verbose_name="Estado del Catálogo"
    )

    class Meta:
        db_table = 'core_carta'
        verbose_name = 'Carta de Control ISO'
        verbose_name_plural = '3. Catálogo de Cartas'
        ordering = ['norma_iso', 'nombre']

    def __str__(self):
        return f"{self.nombre} [{self.norma_iso}] (Fuerza: {self.fuerza} | Defensa: {self.defensa})"

    @property
    def imagen_url(self):
        """
        Retorna la URL de la imagen de la carta o un fallback temático según la norma/nombre.
        """
        if self.imagen:
            try:
                return self.imagen.url
            except Exception:
                pass
        nombre_lower = (self.nombre or '').lower()
        norma_lower = (self.norma_iso or '').lower()
        if 'phishing' in nombre_lower or 'hacker' in nombre_lower or 'amenaza' in nombre_lower:
            return '/static/img/incidentes/hacker_cyber.png'
        elif 'cloud' in nombre_lower or 'nube' in nombre_lower or '27017' in norma_lower:
            return '/static/img/cartas/carta_datos.png'
        elif 'servicio' in nombre_lower or 'itsm' in nombre_lower or '20000' in norma_lower:
            return '/static/img/cartas/carta_calidad.png'
        elif 'actualizaci' in nombre_lower or 'acceso' in nombre_lower or 'sistema' in nombre_lower:
            return '/static/img/cartas/carta_accesos.png'
        elif 'firewall' in nombre_lower or 'ciberseguridad' in nombre_lower or '27001' in norma_lower:
            return '/static/img/cartas/carta_ciberseguridad.png'
        elif 'continuidad' in nombre_lower or '22301' in norma_lower:
            return '/static/img/cartas/carta_continuidad.png'
        elif 'dato' in nombre_lower or '27701' in norma_lower:
            return '/static/img/cartas/carta_datos.png'
        elif 'calidad' in nombre_lower or '9001' in norma_lower:
            return '/static/img/cartas/carta_calidad.png'
        return '/static/img/cartas/carta_ciberseguridad.png'



class FaseCartaOpcion(models.Model):
    """
    Relación de opciones de cartas disponibles para resolver un caso/incidente.
    Regla de integridad del negocio: Máximo 5 cartas por fase.
    """
    fase = models.ForeignKey(
        FaseCaso,
        on_delete=models.CASCADE,
        related_name='opciones_cartas',
        verbose_name="Fase del Caso"
    )
    carta = models.ForeignKey(
        Carta,
        on_delete=models.CASCADE,
        related_name='usada_en_fases',
        verbose_name="Carta Ofertada"
    )
    es_solucion_correcta = models.BooleanField(
        default=False,
        verbose_name="¿Es Solución Correcta / Control Efectivo?"
    )

    class Meta:
        db_table = 'core_fase_carta_opcion'
        verbose_name = 'Opción de Carta en Fase'
        verbose_name_plural = '3.1 Cartas Asignadas por Fase'
        unique_together = ('fase', 'carta')

    def __str__(self):
        correcta_txt = "CORRECTA" if self.es_solucion_correcta else "INCORRECTA / DISTRACTOR"
        return f"{self.fase.titulo_incidente} -> {self.carta.nombre} [{correcta_txt}]"

    def clean(self):
        super().clean()
        if hasattr(self, 'fase') and self.fase_id:
            qs = FaseCartaOpcion.objects.filter(fase_id=self.fase_id)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.count() >= 5:
                raise ValidationError(
                    f"Violación de regla de negocio: La fase '{self.fase}' ya cuenta con 5 cartas asignadas. "
                    "El límite máximo permitido por diseño del juego es de 5 cartas por fase."
                )


# ==============================================================================
# MÓDULO 4: ANALÍTICA Y RENDIMIENTO
# ==============================================================================

class PartidaJugada(models.Model):
    """
    Registro histórico de cada intento de resolución de nivel por los colaboradores.
    """
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='partidas',
        verbose_name="Colaborador / Jugador"
    )
    nivel = models.ForeignKey(
        Nivel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='partidas',
        verbose_name="Nivel Disputado"
    )
    resultado = models.CharField(
        max_length=20,
        choices=ResultadoPartidaChoices.choices,
        verbose_name="Resultado de la Partida"
    )
    oro_obtenido = models.IntegerField(default=0, verbose_name="Oro Obtenido")
    gemas_obtenidas = models.IntegerField(default=0, verbose_name="Gemas Obtenidas")
    fecha_partida = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha y Hora de la Partida"
    )

    class Meta:
        db_table = 'core_partida_jugada'
        verbose_name = 'Partida Jugada'
        verbose_name_plural = '4. Analítica y Rendimiento'
        ordering = ['-fecha_partida']

    def __str__(self):
        nivel_str = self.nivel.titulo if self.nivel else "Nivel eliminado"
        return f"{self.usuario.alias} - {nivel_str} - {self.get_resultado_display()} ({self.fecha_partida.strftime('%Y-%m-%d %H:%M')})"


# ==============================================================================
# MÓDULO 5: AUDITORÍA INMUTABLE
# ==============================================================================

class RegistroAuditoria(models.Model):
    """
    Bitácora forense e inmutable de acciones administrativas y eventos críticos.
    Solo lectura en el panel de Django para garantizar trazabilidad estricta de compliance.
    """
    admin = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='acciones_auditoria',
        verbose_name="Administrador Responsable"
    )
    accion = models.CharField(
        max_length=50,
        choices=AccionAuditoriaChoices.choices,
        verbose_name="Acción Ejecutada"
    )
    modulo_afectado = models.CharField(max_length=50, verbose_name="Módulo Afectado")
    registro_id = models.CharField(max_length=50, verbose_name="ID del Registro Afectado")
    datos_anteriores = models.JSONField(
        null=True,
        blank=True,
        verbose_name="Snapshot Datos Anteriores"
    )
    datos_nuevos = models.JSONField(
        null=True,
        blank=True,
        verbose_name="Snapshot Datos Nuevos"
    )
    direccion_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="Dirección IP de Origen"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Marca de Tiempo (Timestamp)"
    )

    class Meta:
        db_table = 'core_registro_auditoria'
        verbose_name = 'Registro de Auditoría'
        verbose_name_plural = '5. Bitácora de Auditoría Inmutable'
        ordering = ['-created_at']

    def __str__(self):
        admin_nom = self.admin.alias if self.admin else "Sistema / Anónimo"
        return f"[{self.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {admin_nom} -> {self.get_accion_display()} ({self.modulo_afectado} #{self.registro_id})"

    @property
    def modulo_display(self):
        mapa = {
            'Carta': 'Cartas',
            'Cartas': 'Cartas',
            'Usuario': 'Usuarios',
            'Usuarios': 'Usuarios',
            'FaseCaso': 'Fases',
            'Fases': 'Fases',
            'Nivel': 'Niveles',
            'Niveles': 'Niveles',
            'Mundo': 'Mundos',
            'Mundos': 'Mundos',
            'ParametroGlobal': 'Sistema',
            'Sistema': 'Sistema',
            'ProgresoUsuario': 'Progreso',
            'Progreso': 'Progreso',
            'FaseCartaOpcion': 'Barajas',
            'Barajas': 'Barajas',
        }
        return mapa.get(self.modulo_afectado, self.modulo_afectado)

    @property
    def registro_codigo(self):
        prefix_map = {
            'Carta': 'C', 'Cartas': 'C',
            'Usuario': 'U', 'Usuarios': 'U',
            'FaseCaso': 'F', 'Fases': 'F',
            'Nivel': 'N', 'Niveles': 'N',
            'Mundo': 'M', 'Mundos': 'M',
            'ParametroGlobal': 'CFG', 'Sistema': 'CFG',
            'ProgresoUsuario': 'P', 'Progreso': 'P',
            'FaseCartaOpcion': 'B', 'Barajas': 'B',
        }
        prefix = prefix_map.get(self.modulo_afectado, 'REG')
        try:
            val = int(self.registro_id)
            return f"{prefix}-{val:04d}"
        except (ValueError, TypeError):
            return f"{prefix}-{self.registro_id}"

    @property
    def admin_alias(self):
        if self.admin:
            return self.admin.alias
        return 'admin'

    @property
    def admin_avatar_url(self):
        if self.admin:
            return self.admin.avatar_url
        return '/static/img/avatars/necromancer_1.png'


# ==============================================================================
# MÓDULO 6: PARÁMETROS GLOBALES
# ==============================================================================

class ParametroGlobal(models.Model):
    """
    Variables globales de balanceo de juego, economía y mecánicas ISO.
    """
    categoria = models.CharField(
        max_length=50,
        verbose_name="Categoría (ej. Vidas, Jerarquía, Economía)"
    )
    clave = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Clave Única de Configuración"
    )
    valor = models.CharField(max_length=50, verbose_name="Valor del Parámetro")
    descripcion = models.CharField(max_length=255, verbose_name="Descripción / Efecto en Mecánica")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Modificación")

    class Meta:
        db_table = 'core_parametro_global'
        verbose_name = 'Parámetro Global'
        verbose_name_plural = '6. Parámetros Globales'
        ordering = ['categoria', 'clave']

    def __str__(self):
        return f"[{self.categoria}] {self.clave} = {self.valor}"
