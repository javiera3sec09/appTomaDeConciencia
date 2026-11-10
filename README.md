# 🛡️ Panel de Administración y Backend de Videojuego ISO & Compliance

Backend de alta fidelidad desarrollado en **Django 5.x / 6.x** y **SQLite3** para la administración, balanceo pedagógico, bitácora forense de auditoría y analítica en tiempo real de un videojuego de capacitación corporativa en normas ISO (ISO/IEC 27001 Seguridad de la Información, ISO 37001 Antisoborno, ISO 9001 Calidad).

---

## 🏗️ Estructura del Proyecto

```text
appConciencia2.0/
│
├── manage.py                          # Gestor de línea de comandos de Django
├── seed.py                            # Script independiente para inicialización de parámetros globales
├── requirements.txt                   # Dependencias (Django, Pillow, asgiref)
├── db.sqlite3                         # Base de datos relacional SQLite
│
├── game_backend/                      # Configuración raíz del proyecto
│   ├── __init__.py
│   ├── settings.py                   # Configuración global, SQLite, auth custom, context processors
│   ├── urls.py                       # Enrutador principal y resolución de analítica
│   ├── wsgi.py                       # Interfaz WSGI para servidores de producción
│   └── asgi.py                       # Interfaz ASGI para eventos asíncronos
│
└── core/                              # Aplicación principal del juego y compliance
    ├── __init__.py
    ├── apps.py                       # Definición de AppConfig y registro de señales
    ├── models.py                     # Definición de los 10 modelos y choices ENUM
    ├── forms.py                      # FormSets de validación estricta (máximo 5 cartas por fase)
    ├── admin.py                      # Configuración Django Admin, inlines, acciones y auditoría inmutable
    ├── views.py                      # Consultas agregadas (Count, Sum, Avg) y endpoints JSON
    ├── urls.py                       # Enrutador de analítica (/admin/analytics/) y API (/api/metrics/summary/)
    ├── utils.py                      # Utilitarios de auditoría forense, captura de IP y serialización
    ├── signals.py                    # Señal post_save para aprovisionar automáticamente el progreso
    ├── context_processors.py         # Context processor para métricas en admin/index.html
    ├── tests.py                      # Suite de pruebas unitarias automatizadas
    │
    ├── management/
    │   └── commands/
    │       ├── init_game_params.py   # Comando: python manage.py init_game_params
    │       └── seed_demo_data.py     # Comando: python manage.py seed_demo_data
    │
    └── templates/
        └── admin/
            ├── index.html            # Dashboard ejecutivo sobreescrito con tarjetas KPI
            └── analytics_dashboard.html # Tablero integral de telemetría y desempeño ISO
```

---

## 🧩 Especificación de Módulos y Modelos

1. **Módulo 1: Usuarios y Progreso**
   - `Usuario`: Modelo de usuario personalizado que hereda de `AbstractBaseUser` y `PermissionsMixin`. Conserva alias, correo único, área organizacional (TI, Legal, Compliance, etc.), rol (`administrador`, `empleado_jugador`) y estado (`activo`, `inactivo`).
   - `ProgresoUsuario`: Relación `OneToOne` con `Usuario`. Almacena nivel, XP (`BigIntegerField`), economía de monedas de oro, gemas de compliance, vidas actuales (base 3) y marcas de tiempo de reinicio de vidas y progreso. Aprovisionado automáticamente mediante `post_save` signal.

2. **Módulo 2: Contenido (Mundos, Niveles y Fases)**
   - `Mundo`: Ecosistema de cada norma ISO (`codigo_iso`, `nombre_tematico`, `dominio`, `dificultad`, `orden`, `estado`).
   - `Nivel`: Etapas de cada mundo (`mundo`, `numero_nivel`, `titulo`, `tipo` ['normal', 'jefe'], `dificultad`, recompensas de oro, gemas y XP).
   - `FaseCaso`: Incidentes de compliance dentro del nivel (`nivel`, `numero_fase`, `titulo_incidente`, `caso_contexto`, `amenaza`, recompensas y dificultad).

3. **Módulo 3: Catálogo de Cartas y Barajas por Fase**
   - `Carta`: Salvaguardas y controles de mitigación (`norma_iso`, `concepto`, `descripcion`, `imagen`, `fuerza`, `defensa`, `estado`).
   - `FaseCartaOpcion`: Relación intermedia que vincula incidentes con cartas ofertadas al jugador e indica si es solución correcta o distractor. **Validación estricta de regla de negocio:** Máximo 5 cartas por fase en el modelo (`clean()`) y en el formset del admin (`FaseCartaOpcionInlineFormSet`).

4. **Módulo 4: Analítica y Rendimiento**
   - `PartidaJugada`: Registro de partidas de los colaboradores (`usuario`, `nivel`, `resultado` ['victoria', 'derrota', 'abandonada'], oro y gemas obtenidos, `fecha_partida`).

5. **Módulo 5: Auditoría Inmutable (Forense)**
   - `RegistroAuditoria`: Bitácora inalterable de acciones administrativas (`admin`, `accion`, `modulo_afectado`, `registro_id`, `datos_anteriores` en JSON, `datos_nuevos` en JSON, `direccion_ip`, `created_at`).
   - **Inmutabilidad en Django Admin:** `has_add_permission`, `has_change_permission` y `has_delete_permission` deshabilitados estrictamente (`False`). Todos los campos en `readonly_fields`.

6. **Módulo 6: Parámetros Globales**
   - `ParametroGlobal`: Variables de balanceo del juego y economía (`categoria`, `clave` única, `valor`, `descripcion`, `updated_at`). Los cambios y eliminaciones en el panel generan automáticamente registros de auditoría (`CAMBIAR_CONFIG` / `ELIMINAR`).

---

## 🚀 Puesta en Marcha Rápida

### 1. Instalación de dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar Migraciones
```bash
python manage.py migrate
```

### 3. Cargar Parámetros Globales Obligatorios
Puedes inicializarlos mediante el script raíz o el comando de gestión de Django:
```bash
# Opción A (Script independiente):
python seed.py

# Opción B (Comando Django):
python manage.py init_game_params
```
Parámetros inicializados automáticamente:
- `vidas_iniciales` = 3
- `vidas_maximas` = 3
- `regeneracion_minutos` = 5
- `fases_por_nivel_estandar` = 5
- `niveles_por_mundo_estandar` = 10
- `monedas_defecto` = 50
- `gemas_defecto` = 10
- `xp_defecto` = 100

### 4. (Opcional) Cargar Entorno Completo de Demostración
Para poblar mundos ISO reales (ISO 27001, ISO 37001, ISO 9001), barajas de cartas, fases con incidentes de phishing/fuga de datos, usuarios de prueba y partidas históricas:
```bash
python manage.py seed_demo_data
```
> **Credenciales del Superadministrador de Demostración:**
> - **Correo:** `admin@compliance.org`
> - **Contraseña:** `Admin123*`

### 5. Iniciar el Servidor de Desarrollo
```bash
python manage.py runserver
```

---

## 🎯 Acceso a Paneles y Rutas Clave

- **Panel de Administración con Dashboard Ejecutivo integrado:**  
  URL: `http://127.0.0.1:8000/admin/`  
  *Muestra de forma nativa tarjetas KPI con total de partidas, porcentaje de victorias vs derrotas con barra visual, oro y gemas en circulación, y jugadores activos vs inactivos calculados mediante agregaciones ORM (`Count`, `Sum`).*

- **Tablero Dedicado de Analítica y Telemetría ISO:**  
  URL: `http://127.0.0.1:8000/admin/analytics/`  
  *Incluye desglose por Norma ISO (ISO 27001, 37001, 9001), distribución por departamentos organizacionales, cuadro de honor con Top 5 jugadores por XP y bitácora forense reciente.*

- **Endpoint de Métricas en Formato JSON:**  
  URL: `http://127.0.0.1:8000/api/metrics/summary/`  
  *Para integración con dashboards externos, BI o motores de videojuegos como Unity/Unreal/Godot.*

---

## 🧪 Pruebas Unitarias Automatizadas

El proyecto incluye pruebas automatizadas exhaustivas que verifican:
- Señal de aprovisionamiento automático de `ProgresoUsuario`.
- Regla de negocio de máximo 5 cartas por fase (`ValidationError`).
- Acción personalizada de reinicio de progreso y generación de asiento inmutable en `RegistroAuditoria`.
- Inmutabilidad estricta del modelo `RegistroAuditoria` en el admin.
- Consultas agregadas de analítica global.

Ejecución de tests:
```bash
python manage.py test core
```
