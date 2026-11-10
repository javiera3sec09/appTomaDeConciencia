"""
Comando de gestión de Django: python manage.py init_game_params
Carga o actualiza los parámetros globales por defecto del videojuego ISO & Compliance.
"""
from django.core.management.base import BaseCommand
from core.models import ParametroGlobal


PARAMETROS_DEFECTO = [
    {
        'categoria': 'Vidas',
        'clave': 'vidas_iniciales',
        'valor': '3',
        'descripcion': 'Cantidad de vidas por partida.'
    },
    {
        'categoria': 'Vidas',
        'clave': 'vidas_maximas',
        'valor': '3',
        'descripcion': 'Límite máximo de vidas acumulables por regeneración periódica.'
    },
    {
        'categoria': 'Vidas',
        'clave': 'regeneracion_minutos',
        'valor': '5',
        'descripcion': 'Tiempo de regeneración de vidas (min).'
    },
    {
        'categoria': 'Jerarquía',
        'clave': 'nivel_maximo',
        'valor': '5',
        'descripcion': 'Nivel máximo alcanzable.'
    },
    {
        'categoria': 'Jerarquía',
        'clave': 'niveles_por_mundo',
        'valor': '5',
        'descripcion': 'Cantidad estándar de niveles por cada norma o mundo ISO.'
    },
    {
        'categoria': 'Economía',
        'clave': 'oro_inicial',
        'valor': '100',
        'descripcion': 'Oro inicial del jugador.'
    },
    {
        'categoria': 'Economía',
        'clave': 'gemas_iniciales',
        'valor': '10',
        'descripcion': 'Gemas iniciales del jugador.'
    },
    {
        'categoria': 'Seguridad',
        'clave': 'tiempo_sesion',
        'valor': '30',
        'descripcion': 'Tiempo de sesión (min).'
    },
    {
        'categoria': 'Seguridad',
        'clave': 'tiempo_caso',
        'valor': '45',
        'descripcion': 'Tiempo límite para resolver cada caso o fase (segundos).'
    },
    {
        'categoria': 'Logros',
        'clave': 'logros_activos',
        'valor': 'true',
        'descripcion': 'Habilita el sistema de logros.'
    },
]


class Command(BaseCommand):
    help = 'Puebla los Parámetros Globales por defecto del videojuego de capacitación ISO.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Iniciando carga de Parámetros Globales..."))
        creados = 0
        actualizados = 0

        from core.utils import sincronizar_efecto_parametro_global
        for item in PARAMETROS_DEFECTO:
            obj, created = ParametroGlobal.objects.update_or_create(
                clave=item['clave'],
                defaults={
                    'categoria': item['categoria'],
                    'valor': item['valor'],
                    'descripcion': item['descripcion'],
                }
            )
            sincronizar_efecto_parametro_global(obj)
            if created:
                creados += 1
                self.stdout.write(self.style.SUCCESS(f"  [+] Creado: {item['clave']} = {item['valor']} ({item['categoria']})"))
            else:
                actualizados += 1
                self.stdout.write(self.style.WARNING(f"  [*] Actualizado: {item['clave']} = {item['valor']} ({item['categoria']})"))

        self.stdout.write(self.style.SUCCESS(
            f"\nFinalizado exitosamente: {creados} parámetros creados, {actualizados} actualizados."
        ))
