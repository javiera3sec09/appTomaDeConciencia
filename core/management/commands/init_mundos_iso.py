"""
Comando de gestión de Django: python manage.py init_mundos_iso
Configura exactamente 5 niveles por cada mundo activo, con exactamente 3 fases por nivel,
y 4 barajas/cartas por fase (1 correcta y 3 distractores), siguiendo el formato de entidades mitológicas
y rigor técnico de normas ISO (ISO 27001, ISO 27017, ISO 20000-1 e ISO 22301).
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import (
    Mundo,
    Nivel,
    FaseCaso,
    Carta,
    FaseCartaOpcion,
    DificultadChoices,
    TipoNivelChoices,
    EstadoEntidadChoices,
)
from core.data_mundos_fases import MUNDOS_CONFIG


class Command(BaseCommand):
    help = 'Inicializa exactamente 5 niveles por mundo activo con 3 fases y sus barajas de cartas.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("[*] Configurando Mundos ISO Activos con 5 niveles, 3 fases por nivel y 4 cartas por fase...")

        # 1. Configurar y sincronizar cada mundo oficial según MUNDOS_CONFIG
        for m_conf in MUNDOS_CONFIG:
            mundo, _ = Mundo.objects.update_or_create(
                orden=m_conf['orden'],
                defaults={
                    'codigo_iso': m_conf['codigo_iso'],
                    'nombre_tematico': m_conf['nombre_tematico'],
                    'dominio': m_conf['dominio'],
                    'dificultad': m_conf.get('dificultad', DificultadChoices.NORMAL),
                    'estado': EstadoEntidadChoices.ACTIVO,
                }
            )
            self.stdout.write(f"\n  [+] Procesando Mundo {mundo.orden}: {mundo.codigo_iso} - {mundo.nombre_tematico}")

            # Eliminar niveles excedentes (> 5) si existían
            niveles_excedentes = mundo.niveles.filter(numero_nivel__gt=5)
            if niveles_excedentes.exists():
                count_del = niveles_excedentes.count()
                niveles_excedentes.delete()
                self.stdout.write(f"      [-] Eliminados {count_del} niveles excedentes (> 5) de Mundo {mundo.orden}.")

            # 2. Configurar exactamente 5 niveles
            for n_conf in m_conf['niveles']:
                nivel, _ = Nivel.objects.update_or_create(
                    mundo=mundo,
                    numero_nivel=n_conf['numero_nivel'],
                    defaults={
                        'titulo': n_conf['titulo'],
                        'tipo': n_conf.get('tipo', TipoNivelChoices.NORMAL),
                        'dificultad': n_conf.get('dificultad', DificultadChoices.NORMAL),
                        'recompensa_oro': n_conf.get('recompensa_oro', 50 * n_conf['numero_nivel']),
                        'recompensa_gemas': n_conf.get('recompensa_gemas', 10 * n_conf['numero_nivel']),
                        'recompensa_xp': n_conf.get('recompensa_xp', 100 * n_conf['numero_nivel']),
                        'estado': EstadoEntidadChoices.ACTIVO,
                    }
                )

                # Eliminar fases excedentes (> 3) si existían
                fases_excedentes = nivel.fases.filter(numero_fase__gt=3)
                if fases_excedentes.exists():
                    fases_excedentes.delete()

                # 3. Configurar exactamente 3 fases por nivel
                for f_conf in n_conf['fases']:
                    fase, _ = FaseCaso.objects.update_or_create(
                        nivel=nivel,
                        numero_fase=f_conf['numero_fase'],
                        defaults={
                            'titulo_incidente': f_conf['titulo_incidente'],
                            'caso_contexto': f_conf['caso_contexto'],
                            'amenaza': f_conf['amenaza'],
                            'dificultad': f_conf.get('dificultad', DificultadChoices.NORMAL),
                            'recompensa_oro': 15 * f_conf['numero_fase'],
                            'recompensa_xp': 25 * f_conf['numero_fase'],
                            'estado': EstadoEntidadChoices.ACTIVO,
                        }
                    )

                    # 4. Configurar las 4 opciones de baraja/carta para la fase
                    # Limpiar opciones anteriores de esta fase para garantizar exactamente 4 cartas
                    FaseCartaOpcion.objects.filter(fase=fase).delete()

                    for op_conf in f_conf['opciones']:
                        # Crear o actualizar carta en el catálogo global
                        carta, _ = Carta.objects.update_or_create(
                            nombre=op_conf['nombre'],
                            defaults={
                                'norma_iso': mundo.codigo_iso,
                                'concepto': op_conf['concepto'],
                                'descripcion': op_conf['descripcion'],
                                'fuerza': op_conf.get('fuerza', 85),
                                'defensa': op_conf.get('defensa', 85),
                                'estado': EstadoEntidadChoices.ACTIVO,
                            }
                        )

                        # Asociar carta a la fase
                        FaseCartaOpcion.objects.create(
                            fase=fase,
                            carta=carta,
                            es_solucion_correcta=op_conf['es_correcta'],
                        )

                self.stdout.write(f"      [OK] Nivel {nivel.numero_nivel}: {nivel.titulo} -> 3 Fases y Barajas creadas.")

        # 5. Para cualquier otro mundo activo en el sistema, asegurar 5 niveles y 3 fases
        otros_mundos_activos = Mundo.objects.filter(estado=EstadoEntidadChoices.ACTIVO).exclude(orden__in=[m['orden'] for m in MUNDOS_CONFIG])
        for om in otros_mundos_activos:
            self.stdout.write(f"\n  [+] Ajustando mundo activo adicional: {om.codigo_iso} (ID {om.id})")
            # Ajustar niveles a máx 5
            om.niveles.filter(numero_nivel__gt=5).delete()
            for n_num in range(1, 6):
                niv, _ = Nivel.objects.get_or_create(
                    mundo=om,
                    numero_nivel=n_num,
                    defaults={
                        'titulo': f'Nivel {n_num} - {om.nombre_tematico}',
                        'tipo': TipoNivelChoices.JEFE if n_num == 5 else TipoNivelChoices.NORMAL,
                        'dificultad': DificultadChoices.NORMAL,
                        'estado': EstadoEntidadChoices.ACTIVO,
                    }
                )
                niv.fases.filter(numero_fase__gt=3).delete()
                for f_num in range(1, 4):
                    fase, _ = FaseCaso.objects.get_or_create(
                        nivel=niv,
                        numero_fase=f_num,
                        defaults={
                            'titulo_incidente': f'Caso {f_num} - Nivel {n_num} ({om.codigo_iso})',
                            'caso_contexto': f'Escenario / Caso para {om.codigo_iso}. ¿A qué entidad mitológica debes recurrir?',
                            'amenaza': 'Incumplimiento normativo y riesgo operativo',
                            'dificultad': DificultadChoices.NORMAL,
                            'estado': EstadoEntidadChoices.ACTIVO,
                        }
                    )

        self.stdout.write(self.style.SUCCESS("\n[OK] ¡Todos los mundos activos quedaron configurados exitosamente!"))
        for m in Mundo.objects.filter(estado=EstadoEntidadChoices.ACTIVO).order_by('orden'):
            total_niv = m.niveles.count()
            total_fas = FaseCaso.objects.filter(nivel__mundo=m).count()
            total_bar = FaseCartaOpcion.objects.filter(fase__nivel__mundo=m).count()
            self.stdout.write(f"  - Mundo {m.orden} ({m.codigo_iso}): {total_niv} niveles | {total_fas} fases | {total_bar} cartas asignadas en barajas.")
