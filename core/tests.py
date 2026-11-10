"""
Pruebas Automatizadas (Unit Tests) del Backend del Videojuego ISO & Compliance.
Valida reglas de negocio, integridad de datos, bitácora forense y analítica agregada.
"""
from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import AdminSite
from django.core.exceptions import ValidationError
from django.utils import timezone
import json

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
    ResultadoPartidaChoices,
    AccionAuditoriaChoices,
)
from core.admin import (
    UsuarioAdmin,
    RegistroAuditoriaAdmin,
    FaseCasoAdmin,
)
from core.views import get_analytics_data, jugar_nivel_view
from core.utils import registrar_auditoria


class MockSuperUser:
    def __init__(self, user):
        self.user = user

    def has_perm(self, perm):
        return True


class ISOComplianceGameTestCase(TestCase):
    """
    Suite de pruebas integrales para los 6 módulos y requerimientos de administración.
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.site = AdminSite()

        # Admin User
        self.admin = Usuario.objects.create_superuser(
            correo='admin.test@empresa.com',
            alias='AdminTester',
            nombre_completo='Auditor Jefe',
            password='Password123*'
        )

        # Empleado / Jugador
        self.jugador = Usuario.objects.create_user(
            correo='jugador.test@empresa.com',
            alias='PlayerOne',
            nombre_completo='Colaborador Operativo',
            area='Compliance',
            password='Password123*'
        )

        # Mundo ISO
        self.mundo = Mundo.objects.create(
            orden=1,
            codigo_iso='ISO 27001',
            nombre_tematico='Seguridad de Datos',
            dominio='Ciberseguridad'
        )

        # Nivel
        self.nivel = Nivel.objects.create(
            mundo=self.mundo,
            numero_nivel=1,
            titulo='Acceso Seguro'
        )

        # Fase de Caso
        self.fase = FaseCaso.objects.create(
            nivel=self.nivel,
            numero_fase=1,
            titulo_incidente='Intento de Phishing',
            caso_contexto='Detección de correo malicioso',
            amenaza='Ingeniería Social'
        )

    def test_creacion_automatica_progreso_usuario(self):
        """Verifica que el modelo ProgresoUsuario se aprovisione automáticamente por señal."""
        self.assertTrue(hasattr(self.jugador, 'progreso'))
        progreso = self.jugador.progreso
        self.assertEqual(progreso.nivel, 1)
        self.assertEqual(progreso.xp, 0)
        self.assertEqual(progreso.vidas_actuales, 3)

    def test_regla_integridad_maximo_5_cartas_por_fase(self):
        """Verifica que no sea posible asociar más de 5 cartas a una misma fase."""
        cartas = []
        for i in range(6):
            c = Carta.objects.create(
                nombre=f"Carta Control {i+1}",
                norma_iso='ISO 27001',
                concepto=f'Control {i+1}',
                descripcion='Detalle técnico',
                fuerza=50,
                defensa=50
            )
            cartas.append(c)

        # Asignar 5 cartas exitosamente
        for i in range(5):
            opcion = FaseCartaOpcion(fase=self.fase, carta=cartas[i])
            opcion.full_clean()
            opcion.save()

        self.assertEqual(self.fase.opciones_cartas.count(), 5)

        # Intentar asignar la 6ta carta debe lanzar ValidationError
        opcion_excedente = FaseCartaOpcion(fase=self.fase, carta=cartas[5])
        with self.assertRaises(ValidationError):
            opcion_excedente.full_clean()

    def test_accion_admin_reiniciar_progreso_con_auditoria(self):
        """Verifica la acción personalizada de reinicio de progreso y su registro inmutable en auditoría."""
        # Modificar progreso previo para simular avance
        progreso = self.jugador.progreso
        progreso.nivel = 7
        progreso.xp = 4500
        progreso.oro = 1200
        progreso.gemas = 80
        progreso.vidas_actuales = 1
        progreso.save()

        # Ejecutar acción personalizada
        usuario_admin = UsuarioAdmin(Usuario, self.site)
        request = self.factory.get('/admin/core/usuario/')
        request.user = self.admin
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', {})
        setattr(request, '_messages', FallbackStorage(request))

        queryset = Usuario.objects.filter(pk=self.jugador.pk)
        usuario_admin.reiniciar_progreso_action(request, queryset)

        # Recargar y verificar progreso restablecido con valores de ParametroGlobal
        progreso.refresh_from_db()
        self.assertEqual(progreso.nivel, 1)
        self.assertEqual(progreso.xp, 0)
        self.assertEqual(progreso.oro, 100)
        self.assertEqual(progreso.gemas, 10)
        self.assertEqual(progreso.vidas_actuales, 3)
        self.assertIsNotNone(progreso.ultimo_reinicio_progreso)

        # Verificar bitácora de auditoría inmutable
        asiento = RegistroAuditoria.objects.filter(
            accion=AccionAuditoriaChoices.REINICIAR_PROGRESO,
            registro_id=str(progreso.pk)
        ).first()

        self.assertIsNotNone(asiento)
        self.assertEqual(asiento.admin, self.admin)
        self.assertEqual(asiento.modulo_afectado, 'ProgresoUsuario')
        self.assertEqual(asiento.datos_anteriores['xp'], 4500)
        self.assertEqual(asiento.datos_nuevos['xp'], 0)

    def test_inmutabilidad_registro_auditoria(self):
        """Verifica que el admin bloquee adición, edición y eliminación de registros de auditoría."""
        auditoria_admin = RegistroAuditoriaAdmin(RegistroAuditoria, self.site)
        request = self.factory.get('/admin/core/registroauditoria/')
        request.user = self.admin

        self.assertFalse(auditoria_admin.has_add_permission(request))
        self.assertFalse(auditoria_admin.has_change_permission(request))
        self.assertFalse(auditoria_admin.has_delete_permission(request))

    def test_consultas_agregadas_analitica(self):
        """Verifica el cálculo de analítica agregada (Count, Sum, Avg)."""
        # Crear partidas de prueba
        PartidaJugada.objects.create(
            usuario=self.jugador,
            nivel=self.nivel,
            resultado=ResultadoPartidaChoices.VICTORIA,
            oro_obtenido=100,
            gemas_obtenidas=20
        )
        PartidaJugada.objects.create(
            usuario=self.jugador,
            nivel=self.nivel,
            resultado=ResultadoPartidaChoices.DERROTA,
            oro_obtenido=10,
            gemas_obtenidas=0
        )

        data = get_analytics_data()
        self.assertGreaterEqual(data['total_partidas'], 2)
        self.assertGreaterEqual(data['total_victorias'], 1)
        self.assertGreaterEqual(data['total_derrotas'], 1)
        self.assertGreaterEqual(data['oro_global'], 110)
        self.assertGreaterEqual(data['gemas_globales'], 20)
        self.assertIn('tasa_victoria', data)
        self.assertIn('jugadores_activos', data)

    def test_purge_auditoria_por_tiempo(self):
        """Verifica la depuración de registros de auditoría según el rango de tiempo seleccionado."""
        import json
        import datetime
        from core.views import registroauditoria_purge_ajax

        now = timezone.now()

        # Registro de hace 10 días (< 1 mes)
        r_reciente = RegistroAuditoria.objects.create(
            admin=self.admin,
            accion=AccionAuditoriaChoices.CREAR,
            modulo_afectado='Cartas',
            registro_id='1'
        )
        RegistroAuditoria.objects.filter(pk=r_reciente.pk).update(created_at=now - datetime.timedelta(days=10))

        # Registro de hace 40 días (> 1 mes, < 2 meses)
        r_1mes = RegistroAuditoria.objects.create(
            admin=self.admin,
            accion=AccionAuditoriaChoices.EDITAR,
            modulo_afectado='Usuarios',
            registro_id='2'
        )
        RegistroAuditoria.objects.filter(pk=r_1mes.pk).update(created_at=now - datetime.timedelta(days=40))

        # Registro de hace 75 días (> 2 meses, < 3 meses)
        r_2meses = RegistroAuditoria.objects.create(
            admin=self.admin,
            accion=AccionAuditoriaChoices.ELIMINAR,
            modulo_afectado='Fases',
            registro_id='3'
        )
        RegistroAuditoria.objects.filter(pk=r_2meses.pk).update(created_at=now - datetime.timedelta(days=75))

        # Registro de hace 100 días (> 3 meses)
        r_3meses = RegistroAuditoria.objects.create(
            admin=self.admin,
            accion=AccionAuditoriaChoices.CAMBIAR_CONFIG,
            modulo_afectado='Sistema',
            registro_id='4'
        )
        RegistroAuditoria.objects.filter(pk=r_3meses.pk).update(created_at=now - datetime.timedelta(days=100))

        # 1. Probar PREVIEW para > 2 meses (60 días): deben ser r_2meses (75d) y r_3meses (100d)
        req_prev = self.factory.post(
            '/admin/core/registroauditoria/purge-ajax/',
            data=json.dumps({'tiempo': '2', 'admin_id': 'todos', 'accion': 'todas', 'preview': True}),
            content_type='application/json'
        )
        req_prev.user = self.admin
        res_prev = registroauditoria_purge_ajax(req_prev)
        self.assertEqual(res_prev.status_code, 200)
        data_prev = json.loads(res_prev.content)
        self.assertTrue(data_prev['success'])
        self.assertEqual(data_prev['count'], 2)

        # 2. Probar BORRADO para > 3 meses (90 días): solo debe borrar r_3meses (100d)
        req_del_3m = self.factory.post(
            '/admin/core/registroauditoria/purge-ajax/',
            data=json.dumps({'tiempo': '3', 'admin_id': 'todos', 'accion': 'todas', 'preview': False}),
            content_type='application/json'
        )
        req_del_3m.user = self.admin
        res_del_3m = registroauditoria_purge_ajax(req_del_3m)
        self.assertEqual(res_del_3m.status_code, 200)
        data_del_3m = json.loads(res_del_3m.content)
        self.assertEqual(data_del_3m['deleted_count'], 1)
        self.assertFalse(RegistroAuditoria.objects.filter(pk=r_3meses.pk).exists())
        self.assertTrue(RegistroAuditoria.objects.filter(pk=r_2meses.pk).exists())
        self.assertTrue(RegistroAuditoria.objects.filter(pk=r_1mes.pk).exists())
        self.assertTrue(RegistroAuditoria.objects.filter(pk=r_reciente.pk).exists())

        # 3. Probar BORRADO para > 1 mes (30 días): debe borrar r_2meses y r_1mes
        req_del_1m = self.factory.post(
            '/admin/core/registroauditoria/purge-ajax/',
            data=json.dumps({'tiempo': '1', 'admin_id': 'todos', 'accion': 'todas', 'preview': False}),
            content_type='application/json'
        )
        req_del_1m.user = self.admin
        res_del_1m = registroauditoria_purge_ajax(req_del_1m)
        data_del_1m = json.loads(res_del_1m.content)
        self.assertEqual(data_del_1m['deleted_count'], 2)
        self.assertFalse(RegistroAuditoria.objects.filter(pk=r_2meses.pk).exists())
        self.assertFalse(RegistroAuditoria.objects.filter(pk=r_1mes.pk).exists())
        self.assertTrue(RegistroAuditoria.objects.filter(pk=r_reciente.pk).exists())

    def test_cartas_en_juego_usan_misma_imagen_que_catalogo(self):
        """Verifica que en el gameplay (juego_view) las cartas usen su misma imagen del catálogo."""
        carta1 = Carta.objects.create(
            nombre="Cifrado de Base de Datos",
            norma_iso="ISO 27001",
            concepto="Seguridad Criptográfica",
            descripcion="Aplica cifrado en reposo para datos sensibles.",
            fuerza=80,
            defensa=75
        )
        carta2 = Carta.objects.create(
            nombre="Plan de Continuidad Operativa",
            norma_iso="ISO 22301",
            concepto="Resiliencia Operativa",
            descripcion="Estrategia de recuperación de servicios.",
            fuerza=85,
            defensa=90
        )
        FaseCartaOpcion.objects.create(fase=self.fase, carta=carta1, es_solucion_correcta=True)
        FaseCartaOpcion.objects.create(fase=self.fase, carta=carta2, es_solucion_correcta=False)

        self.client.force_login(self.admin)
        res = self.client.get(f'/jugar/{self.nivel.id}/')
        self.assertEqual(res.status_code, 200)

        # Extraer JSON de fases
        context_json = res.context['fases_data_json']
        fases_data = json.loads(context_json)
        self.assertEqual(len(fases_data), 1)

        cartas_fase = fases_data[0]['cartas']
        self.assertEqual(len(cartas_fase), 2)
        # La carta 1 debe tener exactamente carta1.imagen_url (no art_malware.png)
        self.assertEqual(cartas_fase[0]['imagen_url'], carta1.imagen_url)
        self.assertNotEqual(cartas_fase[0]['imagen_url'], '/static/img/cartas/art_malware.png')
        # La carta 2 debe tener exactamente carta2.imagen_url (no art_identity.png)
        self.assertEqual(cartas_fase[1]['imagen_url'], carta2.imagen_url)
        self.assertNotEqual(cartas_fase[1]['imagen_url'], '/static/img/cartas/art_identity.png')

    def test_descuento_vidas_en_derrota_y_hud_energia(self):
        """Verifica que las vidas (Energía Arcana) se descuentan al perder, se calculan los segundos de regeneración y se reflejan en el progreso."""
        self.client.force_login(self.jugador)
        progreso = self.jugador.progreso
        progreso.vidas_actuales = 3
        progreso.save()

        # Registrar derrota
        res = self.client.post(f'/api/mapas/registrar-derrota/{self.nivel.id}/')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['vidas_actuales'], 2)
        self.assertIn('segundos_siguiente_vida', data)
        self.assertGreater(data['segundos_siguiente_vida'], 0)
        self.assertEqual(data['regeneracion_minutos'], 5)

        progreso.refresh_from_db()
        self.assertEqual(progreso.vidas_actuales, 2)

    def test_regeneracion_vidas_segun_parametro_global(self):
        """Verifica que el tiempo de regeneración se rija por 'regeneracion_minutos' de ParametroGlobal y regenere vidas."""
        from datetime import timedelta
        from core.utils import aplicar_regeneracion_vidas

        # Configurar parámetro global: regeneración de 2 minutos
        ParametroGlobal.objects.update_or_create(
            clave='regeneracion_minutos',
            defaults={'categoria': 'Vidas', 'valor': '2', 'descripcion': '2 minutos de regeneración'}
        )
        ParametroGlobal.objects.update_or_create(
            clave='vidas_maximas',
            defaults={'categoria': 'Vidas', 'valor': '3', 'descripcion': '3 vidas máximas'}
        )

        progreso = self.jugador.progreso
        progreso.vidas_actuales = 1
        progreso.ultimo_reinicio_vidas = timezone.now() - timedelta(seconds=70)  # Han pasado 70s de los 120s
        progreso.save()

        # Verificar endpoint de estado de vidas
        self.client.force_login(self.jugador)
        res = self.client.get('/api/usuario/estado-vidas/')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['vidas_actuales'], 1)
        self.assertEqual(data['regeneracion_minutos'], 2)
        # Deben quedar aproximadamente 120 - 70 = 50 segundos
        self.assertTrue(45 <= data['segundos_siguiente_vida'] <= 55)

        # Simular que transcurrieron más de 2 minutos (ej. 130 segundos)
        progreso.ultimo_reinicio_vidas = timezone.now() - timedelta(seconds=130)
        progreso.save()

        progreso, max_v, seg_sig, reg_m = aplicar_regeneracion_vidas(progreso)
        self.assertEqual(progreso.vidas_actuales, 2)
        self.assertTrue(seg_sig > 0)

    def test_sincronizacion_parametros_globales(self):
        """Verifica que actualizar ParametroGlobal actualiza visible y realmente el juego."""
        from .utils import sincronizar_efecto_parametro_global
        param_vidas, _ = ParametroGlobal.objects.update_or_create(
            clave='vidas_maximas',
            defaults={'categoria': 'Vidas', 'valor': '5', 'descripcion': 'Max vidas'}
        )
        sincronizar_efecto_parametro_global(param_vidas)

        self.jugador.progreso.refresh_from_db()
        self.assertEqual(self.jugador.progreso.vidas_actuales, 5)

        # Verificar canje de tienda
        self.client.force_login(self.jugador)
        res = self.client.post('/api/tienda/canjear/', {'item': 'energia'})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['vidas_actuales'], 5)

