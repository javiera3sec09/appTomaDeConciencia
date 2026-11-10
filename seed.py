"""
Script de Inicialización y Población de Parámetros Globales (Data Seed).
Ejecución: python seed.py
"""
import os
import sys

# Configurar entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game_backend.settings')

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

try:
    import django
    django.setup()
except ImportError as exc:
    print(f"Error al inicializar Django: {exc}")
    sys.exit(1)

from django.core.management import call_command
from core.models import ParametroGlobal


def main():
    print("=" * 70)
    print("[*] INICIALIZACION DE PARAMETROS GLOBALES - VIDEOJUEGO ISO & COMPLIANCE")
    print("=" * 70)

    # Invocar los comandos de gestión
    call_command('init_game_params')
    call_command('init_mundos_iso')

    print("\nVerificacion de parametros almacenados en base de datos SQLite:")
    for p in ParametroGlobal.objects.all().order_by('categoria', 'clave'):
        print(f"  - [{p.categoria}] {p.clave}: {p.valor} ({p.descripcion})")

    print("\n[OK] Proceso completado con exito.")


if __name__ == '__main__':
    main()
