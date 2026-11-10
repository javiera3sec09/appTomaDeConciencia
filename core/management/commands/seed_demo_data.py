"""
Comando de gestión de Django: python manage.py seed_demo_data
Carga un ecosistema completo de demostración para el videojuego:
- Administrador inicial y jugadores de muestra en distintas áreas.
- Mundos ISO 27001 (Seguridad), ISO 9001 (Calidad) e ISO 37001 (Antisoborno).
- Niveles estándar y de Jefe de auditoría.
- Incidentes/fases con casos reales de compliance (Phishing, Fuga de Datos, Sobornos).
- Catálogo de cartas con controles técnicos y organizacionales.
- Baraja asignada a fases con soluciones correctas y distractores (máximo 5).
- Partidas jugadas con victorias y derrotas para alimentar la analítica.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import (
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
    DificultadChoices,
    TipoNivelChoices,
    ResultadoPartidaChoices,
    AccionAuditoriaChoices,
)


class Command(BaseCommand):
    help = 'Puebla datos completos de prueba (Mundos ISO, Cartas, Niveles, Partidas, Jugadores).'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("[*] Iniciando sembrado de datos de demostracion ISO..."))

        # 1. Crear Superusuario Administrador por defecto si no existe
        admin_user, created = Usuario.objects.get_or_create(
            correo='admin@compliance.org',
            defaults={
                'alias': 'AdminCompliance',
                'nombre_completo': 'Oficial Principal de Cumplimiento',
                'area': 'Oficina de Compliance y Riesgos',
                'rol': RolUsuarioChoices.ADMINISTRADOR,
                'estado': EstadoUsuarioChoices.ACTIVO,
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('Admin123*')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("  [+] Superusuario creado: admin@compliance.org / Admin123*"))

        # 2. Crear Jugadores de Prueba
        jugadores_data = [
            {'correo': 'carlos.m@empresa.com', 'alias': 'CyberGuard', 'nombre': 'Carlos Morales', 'area': 'Tecnología e Infraestructura', 'nivel': 4, 'xp': 1450, 'oro': 350, 'gemas': 30, 'vidas': 3},
            {'correo': 'laura.p@empresa.com', 'alias': 'LexProtect', 'nombre': 'Laura Peña', 'area': 'Asesoría Jurídica y Legal', 'nivel': 3, 'xp': 980, 'oro': 220, 'gemas': 15, 'vidas': 2},
            {'correo': 'andres.r@empresa.com', 'alias': 'RiskHunter', 'nombre': 'Andrés Restrepo', 'area': 'Gestión de Riesgos y Control Interno', 'nivel': 5, 'xp': 2300, 'oro': 600, 'gemas': 50, 'vidas': 3},
            {'correo': 'valentina.s@empresa.com', 'alias': 'DataSentry', 'nombre': 'Valentina Solís', 'area': 'Seguridad de la Información', 'nivel': 6, 'xp': 3100, 'oro': 850, 'gemas': 75, 'vidas': 3},
            {'correo': 'diego.t@empresa.com', 'alias': 'AuditMaster', 'nombre': 'Diego Torres', 'area': 'Auditoría Interna', 'nivel': 2, 'xp': 450, 'oro': 110, 'gemas': 5, 'vidas': 1},
            {'correo': 'marina.v@empresa.com', 'alias': 'InactivaUser', 'nombre': 'Marina Vega', 'area': 'Talento Humano', 'nivel': 1, 'xp': 0, 'oro': 0, 'gemas': 0, 'vidas': 3, 'estado': EstadoUsuarioChoices.INACTIVO},
        ]

        jugadores_creados = []
        for jd in jugadores_data:
            u, _ = Usuario.objects.get_or_create(
                correo=jd['correo'],
                defaults={
                    'alias': jd['alias'],
                    'nombre_completo': jd['nombre'],
                    'area': jd['area'],
                    'rol': RolUsuarioChoices.EMPLEADO_JUGADOR,
                    'estado': jd.get('estado', EstadoUsuarioChoices.ACTIVO),
                }
            )
            # Actualizar progreso
            p, _ = ProgresoUsuario.objects.get_or_create(usuario=u)
            p.nivel = jd['nivel']
            p.xp = jd['xp']
            p.oro = jd['oro']
            p.gemas = jd['gemas']
            p.vidas_actuales = jd['vidas']
            p.save()
            jugadores_creados.append(u)

        # 3. Crear los 4 Mundos ISO Oficiales
        mundo_27001, _ = Mundo.objects.update_or_create(
            orden=1,
            defaults={
                'codigo_iso': 'ISO/IEC 27001:2022',
                'nombre_tematico': 'Seguridad de la Información',
                'dominio': 'Seguridad de la Información, Ciberseguridad y Privacidad',
                'dificultad': DificultadChoices.FACIL,
                'estado': EstadoUsuarioChoices.ACTIVO,
            }
        )

        mundo_27017, _ = Mundo.objects.update_or_create(
            orden=2,
            defaults={
                'codigo_iso': 'ISO/IEC 27017',
                'nombre_tematico': 'Seguridad en la Nube',
                'dominio': 'Seguridad en Servicios Cloud (CSP y CSC)',
                'dificultad': DificultadChoices.NORMAL,
                'estado': EstadoUsuarioChoices.ACTIVO,
            }
        )

        mundo_20000, _ = Mundo.objects.update_or_create(
            orden=3,
            defaults={
                'codigo_iso': 'ISO/IEC 20000-1',
                'nombre_tematico': 'Gestión de Servicios de TI',
                'dominio': 'Gestión y Entrega de Servicios Tecnológicos (ITSM)',
                'dificultad': DificultadChoices.NORMAL,
                'estado': EstadoUsuarioChoices.ACTIVO,
            }
        )

        mundo_22301, _ = Mundo.objects.update_or_create(
            orden=4,
            defaults={
                'codigo_iso': 'ISO 22301',
                'nombre_tematico': 'Continuidad del Negocio',
                'dominio': 'Resiliencia Operativa y Planes de Continuidad',
                'dificultad': DificultadChoices.DIFICIL,
                'estado': EstadoUsuarioChoices.ACTIVO,
            }
        )

        # 4. Crear Niveles
        nivel_1, _ = Nivel.objects.get_or_create(
            mundo=mundo_27001,
            numero_nivel=1,
            defaults={
                'titulo': 'Fundamentos del Control de Acceso',
                'tipo': TipoNivelChoices.NORMAL,
                'dificultad': DificultadChoices.FACIL,
                'recompensa_oro': 50,
                'recompensa_gemas': 10,
                'recompensa_xp': 100,
            }
        )

        nivel_jefe, _ = Nivel.objects.get_or_create(
            mundo=mundo_27001,
            numero_nivel=2,
            defaults={
                'titulo': 'Auditoría Crítica de Ciberamenazas (Jefe)',
                'tipo': TipoNivelChoices.JEFE,
                'dificultad': DificultadChoices.DIFICIL,
                'recompensa_oro': 200,
                'recompensa_gemas': 40,
                'recompensa_xp': 350,
            }
        )

        nivel_cloud, _ = Nivel.objects.get_or_create(
            mundo=mundo_27017,
            numero_nivel=1,
            defaults={
                'titulo': 'Responsabilidad Compartida y Aislamiento Cloud',
                'tipo': TipoNivelChoices.NORMAL,
                'dificultad': DificultadChoices.NORMAL,
                'recompensa_oro': 80,
                'recompensa_gemas': 15,
                'recompensa_xp': 150,
            }
        )

        # 5. Crear Fases de Caso
        fase_1, _ = FaseCaso.objects.get_or_create(
            nivel=nivel_1,
            numero_fase=1,
            defaults={
                'titulo_incidente': 'Ataque de Phishing con Suplantación del Directorio',
                'caso_contexto': 'Varios empleados de tesorería recibieron un correo urgente solicitando actualizar credenciales bancarias institucionales desde un dominio falso.',
                'amenaza': 'Ingeniería Social / Spear Phishing',
                'dificultad': DificultadChoices.FACIL,
                'recompensa_oro': 15,
                'recompensa_xp': 25,
            }
        )

        fase_2, _ = FaseCaso.objects.get_or_create(
            nivel=nivel_1,
            numero_fase=2,
            defaults={
                'titulo_incidente': 'Uso indebido de Privilegios Administrativos en Base de Datos',
                'caso_contexto': 'Un desarrollador externo utilizó una cuenta genérica root para consultar registros de nómina confidenciales sin autorización.',
                'amenaza': 'Elevación de Privilegios y Fuga de Datos',
                'dificultad': DificultadChoices.NORMAL,
                'recompensa_oro': 20,
                'recompensa_xp': 30,
            }
        )

        # 6. Catálogo de Cartas
        cartas_specs = [
            ('Autenticación Multifactor (MFA)', 'ISO 27001', 'Control A.9.4.2 Acceso Seguro', 'Obliga a confirmar la identidad mediante token temporal, bloqueando phishing.', 85, 90),
            ('Capacitación Continua Antiphishing', 'ISO 27001', 'Control A.7.2.2 Concienciación', 'Entrenamiento para identificar remitentes sospechosos e hipervínculos anómalos.', 70, 75),
            ('Principio de Mínimo Privilegio (RBAC)', 'ISO 27001', 'Control A.9.1.2 Acceso a Redes', 'Limita los privilegios estrictamente a las tareas del cargo.', 90, 85),
            ('Cifrado de Datos en Tránsito y Reposo (AES-256)', 'ISO 27001', 'Control A.10.1 Criptografía', 'Protege la confidencialidad ante interceptaciones no deseadas.', 95, 95),
            ('Ignorar Alerta del Correo (Distractor)', 'Ninguna', 'Mala Práctica', 'Permite que el correo sospechoso siga en la bandeja sin reporte.', 10, 5),
            ('Debida Diligencia de Proveedores', 'ISO 37001', 'Cláusula 8.2 Debida Diligencia', 'Investigación previa de antecedentes legales y reputacionales antes de contratar.', 80, 85),
        ]

        cartas_instancias = {}
        for nom, iso, conc, desc, fue, defe in cartas_specs:
            c, _ = Carta.objects.get_or_create(
                nombre=nom,
                defaults={
                    'norma_iso': iso,
                    'concepto': conc,
                    'descripcion': desc,
                    'fuerza': fue,
                    'defensa': defe,
                }
            )
            cartas_instancias[nom] = c

        # 7. Asignar Cartas a Fase 1 (Máximo 5 cartas)
        FaseCartaOpcion.objects.get_or_create(
            fase=fase_1,
            carta=cartas_instancias['Autenticación Multifactor (MFA)'],
            defaults={'es_solucion_correcta': True}
        )
        FaseCartaOpcion.objects.get_or_create(
            fase=fase_1,
            carta=cartas_instancias['Capacitación Continua Antiphishing'],
            defaults={'es_solucion_correcta': True}
        )
        FaseCartaOpcion.objects.get_or_create(
            fase=fase_1,
            carta=cartas_instancias['Ignorar Alerta del Correo (Distractor)'],
            defaults={'es_solucion_correcta': False}
        )

        # 8. Generar Historial de Partidas para Telemetría y Analítica
        partidas_ejemplo = [
            (jugadores_creados[0], nivel_1, ResultadoPartidaChoices.VICTORIA, 50, 10),
            (jugadores_creados[0], nivel_jefe, ResultadoPartidaChoices.VICTORIA, 200, 40),
            (jugadores_creados[1], nivel_1, ResultadoPartidaChoices.VICTORIA, 50, 10),
            (jugadores_creados[1], nivel_jefe, ResultadoPartidaChoices.DERROTA, 0, 0),
            (jugadores_creados[2], nivel_cloud, ResultadoPartidaChoices.VICTORIA, 80, 15),
            (jugadores_creados[2], nivel_1, ResultadoPartidaChoices.VICTORIA, 50, 10),
            (jugadores_creados[3], nivel_1, ResultadoPartidaChoices.VICTORIA, 50, 10),
            (jugadores_creados[3], nivel_jefe, ResultadoPartidaChoices.VICTORIA, 200, 40),
            (jugadores_creados[4], nivel_1, ResultadoPartidaChoices.DERROTA, 0, 0),
            (jugadores_creados[4], nivel_1, ResultadoPartidaChoices.ABANDONADA, 0, 0),
        ]

        for u, niv, res, oro, gemas in partidas_ejemplo:
            PartidaJugada.objects.create(
                usuario=u,
                nivel=niv,
                resultado=res,
                oro_obtenido=oro,
                gemas_obtenidas=gemas,
            )

        # 9. Asiento de Auditoría Inicial
        RegistroAuditoria.objects.get_or_create(
            accion=AccionAuditoriaChoices.CAMBIAR_CONFIG,
            modulo_afectado='SistemaInicial',
            registro_id='INIT-01',
            defaults={
                'admin': admin_user,
                'datos_anteriores': None,
                'datos_nuevos': {'mensaje': 'Población inicial de entorno de capacitación ISO completada'},
                'direccion_ip': '127.0.0.1'
            }
        )

        self.stdout.write(self.style.SUCCESS("[OK] Sembrado de datos de demostracion completado con exito."))
