"""
Estructura oficial de Mundos, Niveles, Fases y Barajas (Cartas/Opciones).
Define exactamente 5 niveles por cada mundo activo, con exactamente 3 fases por nivel,
y 4 barajas/cartas por fase (1 correcta y 3 distractores), siguiendo el formato de entidades mitológicas
y rigor técnico de normas ISO (ISO 27001, ISO 27017, ISO 20000-1 e ISO 22301).
"""

MUNDOS_CONFIG = [
    {
        'orden': 1,
        'codigo_iso': 'ISO/IEC 27001:2022',
        'nombre_tematico': 'Seguridad de la Información',
        'dominio': 'Seguridad de la Información, Ciberseguridad y Privacidad',
        'dificultad': 'facil',
        'niveles': [
            {
                'numero_nivel': 1,
                'titulo': 'Fundamentos del SGSI y Políticas de Seguridad',
                'tipo': 'normal',
                'dificultad': 'facil',
                'recompensa_oro': 50,
                'recompensa_gemas': 10,
                'recompensa_xp': 100,
                'fases': [
                    {
                        'numero_fase': 1,
                        'titulo_incidente': 'Caso de Uso 1: Política de Seguridad y Compromiso de la Dirección',
                        'amenaza': 'Falta de Gobernanza y Desconocimiento de Obligaciones de Seguridad',
                        'dificultad': 'facil',
                        'caso_contexto': (
                            'Escenario / Caso: La organización no cuenta con un marco formal aprobado para proteger '
                            'sus activos críticos y el equipo directivo desconoce sus obligaciones de gobernanza. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La norma ISO/IEC 27001:2022 (Cláusula 5.2) establece que la alta '
                            'dirección debe establecer una política de seguridad de la información que provea '
                            'orientación, compromiso y gobernanza sobre los activos de la organización.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Archimago de las Políticas del SGSI',
                                'concepto': 'Cláusula 5.2 Política de Seguridad',
                                'descripcion': 'Establece directrices formales aprobadas por la alta dirección.',
                                'es_correcta': True,
                                'fuerza': 85,
                                'defensa': 90,
                            },
                            {
                                'nombre': 'Minotauro de las Claves Simétricas',
                                'concepto': 'Control Criptográfico Básico',
                                'descripcion': 'Entidad centrada únicamente en cifrado mecánico sin gobernanza.',
                                'es_correcta': False,
                                'fuerza': 60,
                                'defensa': 55,
                            },
                            {
                                'nombre': 'Nigromante de la Fuga de Correos',
                                'concepto': 'Amenaza Disruptiva de Mensajería',
                                'descripcion': 'Ente que explota canales no cifrados de comunicación.',
                                'es_correcta': False,
                                'fuerza': 65,
                                'defensa': 50,
                            },
                            {
                                'nombre': 'Golem del Servidor de Archivos',
                                'concepto': 'Almacenamiento Local de Datos',
                                'descripcion': 'Guardián pasivo de discos sin visión de cumplimiento directivo.',
                                'es_correcta': False,
                                'fuerza': 58,
                                'defensa': 62,
                            },
                        ],
                    },
                    {
                        'numero_fase': 2,
                        'titulo_incidente': 'Caso de Uso 2: Clasificación y Etiquetado de Activos',
                        'amenaza': 'Exposición de Datos Confidenciales sin Identificación de Riesgo',
                        'dificultad': 'facil',
                        'caso_contexto': (
                            'Escenario / Caso: Documentos con nóminas y contratos confidenciales circulan sin marcas '
                            'de seguridad en carpetas compartidas abiertas a todos los colaboradores. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: El Control A.5.12 de ISO/IEC 27001:2022 exige clasificar la información '
                            'según sus necesidades de protección legal, criticidad y sensibilidad frente a divulgaciones no autorizadas.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Centinela de la Clasificación de Activos',
                                'concepto': 'Control A.5.12 Clasificación de Información',
                                'descripcion': 'Etiqueta y segrega la información según su valor y confidencialidad.',
                                'es_correcta': True,
                                'fuerza': 88,
                                'defensa': 91,
                            },
                            {
                                'nombre': 'Vigía de los Sitios Espejo',
                                'concepto': 'Redundancia Física de Servidores',
                                'descripcion': 'Duplica datos sin discriminar su nivel de confidencialidad.',
                                'es_correcta': False,
                                'fuerza': 62,
                                'defensa': 60,
                            },
                            {
                                'nombre': 'Espectro del Almacén Huérfano',
                                'concepto': 'Riesgo de Datos Abandonados',
                                'descripcion': 'Presencia que deambula entre archivos residuales sin clasificar.',
                                'es_correcta': False,
                                'fuerza': 55,
                                'defensa': 50,
                            },
                            {
                                'nombre': 'Invocador de Copias Fantasma',
                                'concepto': 'Duplicación Descontrolada de Archivos',
                                'descripcion': 'Crea réplicas sin control de etiquetado de seguridad.',
                                'es_correcta': False,
                                'fuerza': 58,
                                'defensa': 52,
                            },
                        ],
                    },
                    {
                        'numero_fase': 3,
                        'titulo_incidente': 'Caso de Uso 3: Cultura y Concientización Contra la Ingeniería Social',
                        'amenaza': 'Phishing y Manipulación Psicológica de Empleados',
                        'dificultad': 'facil',
                        'caso_contexto': (
                            'Escenario / Caso: Empleados de reciente ingreso caen de manera recurrente en correos fraudulentos '
                            'que solicitan credenciales corporativas por falta de entrenamiento continuo. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: El Control A.6.3 de ISO/IEC 27001:2022 establece la concienciación, '
                            'educación y capacitación obligatoria en seguridad para prevenir brechas por engaños o ingeniería social.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Oráculo de Concientización y Cultura de Seguridad',
                                'concepto': 'Control A.6.3 Concientización en Seguridad',
                                'descripcion': 'Instruye la mente de los colaboradores para detectar engaños digitales.',
                                'es_correcta': True,
                                'fuerza': 86,
                                'defensa': 89,
                            },
                            {
                                'nombre': 'Caballero del Cortafuegos Perimetral',
                                'concepto': 'Filtrado de Paquetes en Red',
                                'descripcion': 'Bloquea puertos de red pero es ciego ante engaños al factor humano.',
                                'es_correcta': False,
                                'fuerza': 70,
                                'defensa': 65,
                            },
                            {
                                'nombre': 'Cíclope del Puerto 80',
                                'concepto': 'Inspección de Tráfico HTTP Básico',
                                'descripcion': 'Monitorea tráfico web sin capacidad pedagógica sobre usuarios.',
                                'es_correcta': False,
                                'fuerza': 58,
                                'defensa': 55,
                            },
                            {
                                'nombre': 'Guardián del Cifrado Asimétrico',
                                'concepto': 'Criptografía de Llave Pública',
                                'descripcion': 'Protege el canal matemático pero no el juicio del usuario engañado.',
                                'es_correcta': False,
                                'fuerza': 64,
                                'defensa': 62,
                            },
                        ],
                    },
                ],
            },
            {
                'numero_nivel': 2,
                'titulo': 'Control de Accesos y Autenticación Fuerte',
                'tipo': 'normal',
                'dificultad': 'facil',
                'recompensa_oro': 75,
                'recompensa_gemas': 15,
                'recompensa_xp': 150,
                'fases': [
                    {
                        'numero_fase': 1,
                        'titulo_incidente': 'Caso de Uso 1: Principio de Menor Privilegio (RBAC)',
                        'amenaza': 'Privilegios Excesivos y Escalada no Autorizada',
                        'dificultad': 'facil',
                        'caso_contexto': (
                            'Escenario / Caso: Analistas de soporte júnior tienen permisos de superusuario en la base '
                            'de datos de producción, pudiendo modificar registros maestros sin restricción. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: El Control A.8.2 de ISO/IEC 27001:2022 exige otorgar accesos '
                            'estrictamente basados en el principio de menor privilegio y la necesidad de saber/operar.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Guardián del Menor Privilegio y RBAC',
                                'concepto': 'Control A.8.2 Derechos de Acceso Privilegiados',
                                'descripcion': 'Restringe los privilegios estrictamente a lo requerido para el rol.',
                                'es_correcta': True,
                                'fuerza': 90,
                                'defensa': 92,
                            },
                            {
                                'nombre': 'Basilisco de la Fibra Óptica',
                                'concepto': 'Transmisión Física de Datos',
                                'descripcion': 'Acelera el paso de bits sin discernir niveles de autorización.',
                                'es_correcta': False,
                                'fuerza': 60,
                                'defensa': 54,
                            },
                            {
                                'nombre': 'Titán del Balanceo de Carga',
                                'concepto': 'Distribución de Peticiones Web',
                                'descripcion': 'Reparte solicitudes entre servidores sin validar roles de usuario.',
                                'es_correcta': False,
                                'fuerza': 65,
                                'defensa': 60,
                            },
                            {
                                'nombre': 'Centinela del DNS Dinámico',
                                'concepto': 'Resolución de Nombres de Dominio',
                                'descripcion': 'Asigna direcciones IP a nombres sin evaluar permisos internos.',
                                'es_correcta': False,
                                'fuerza': 55,
                                'defensa': 58,
                            },
                        ],
                    },
                    {
                        'numero_fase': 2,
                        'titulo_incidente': 'Caso de Uso 2: Autenticación Multifactor (MFA)',
                        'amenaza': 'Robo de Contraseñas y Acceso Remoto Ilegítimo',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: El acceso remoto a la red interna corporativa se realiza con solo '
                            'usuario y contraseña estática, exponiendo la organización a ataques de fuerza bruta. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: El Control A.8.5 de ISO/IEC 27001:2022 requiere métodos de autenticación '
                            'segura como MFA (algo que sabes, algo que tienes, algo que eres) para accesos a sistemas críticos.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Custodio de la Autenticación Multifactor (MFA)',
                                'concepto': 'Control A.8.5 Autenticación Segura',
                                'descripcion': 'Exige múltiples factores independientes para validar la identidad.',
                                'es_correcta': True,
                                'fuerza': 91,
                                'defensa': 93,
                            },
                            {
                                'nombre': 'Cazador de Búferes Desbordados',
                                'concepto': 'Detección de Exploits de Memoria',
                                'descripcion': 'Monitorea fallos en binarios pero no valida credenciales de red.',
                                'es_correcta': False,
                                'fuerza': 68,
                                'defensa': 62,
                            },
                            {
                                'nombre': 'Dragón de la Tasa de Transferencia',
                                'concepto': 'Ancho de Banda de Red',
                                'descripcion': 'Monitorea volumen de descarga sin autenticar al usuario remoto.',
                                'es_correcta': False,
                                'fuerza': 62,
                                'defensa': 56,
                            },
                            {
                                'nombre': 'Centurión de la Memoria Swap',
                                'concepto': 'Gestión de Paginación de SO',
                                'descripcion': 'Controla memoria virtual de servidores sin relación con accesos VPN.',
                                'es_correcta': False,
                                'fuerza': 58,
                                'defensa': 55,
                            },
                        ],
                    },
                    {
                        'numero_fase': 3,
                        'titulo_incidente': 'Caso de Uso 3: Revocación Inmediata de Cuentas de Ex-empleados',
                        'amenaza': 'Accesos Huérfanos y Sabotaje Interno post-desvinculación',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Un administrador de sistemas que renunció hace dos semanas aún conserva '
                            'sus credenciales activas en los servidores clave por falta de coordinación con RRHH. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: El Control A.5.18 de ISO/IEC 27001:2022 estipula que los derechos '
                            'de acceso a los activos deben modificarse o revocarse inmediatamente al terminar la relación laboral.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Ejecutor de la Baja y Revocación de Accesos',
                                'concepto': 'Control A.5.18 Derechos de Acceso al Cese',
                                'descripcion': 'Corta inmediatamente los accesos lógicos y físicos de usuarios desvinculados.',
                                'es_correcta': True,
                                'fuerza': 89,
                                'defensa': 90,
                            },
                            {
                                'nombre': 'Arquitecto de Microservicios',
                                'concepto': 'Diseño de Aplicaciones Distribuidas',
                                'descripcion': 'Estructura APIs sin gestionar el ciclo de vida de colaboradores.',
                                'es_correcta': False,
                                'fuerza': 64,
                                'defensa': 60,
                            },
                            {
                                'nombre': 'Centinela del Disco Espejo',
                                'concepto': 'Arreglo RAID de Almacenamiento',
                                'descripcion': 'Protege contra fallas de disco duro físico pero no contra accesos indebidos.',
                                'es_correcta': False,
                                'fuerza': 60,
                                'defensa': 62,
                            },
                            {
                                'nombre': 'Sacerdote de la Latencia Cero',
                                'concepto': 'Optimización de Paquetes en Red',
                                'descripcion': 'Minimiza retrasos de red sin intervenir en permisos de cuentas.',
                                'es_correcta': False,
                                'fuerza': 58,
                                'defensa': 54,
                            },
                        ],
                    },
                ],
            },
            {
                'numero_nivel': 3,
                'titulo': 'Criptografía y Seguridad Operativa',
                'tipo': 'normal',
                'dificultad': 'normal',
                'recompensa_oro': 100,
                'recompensa_gemas': 20,
                'recompensa_xp': 200,
                'fases': [
                    {
                        'numero_fase': 1,
                        'titulo_incidente': 'Caso de Uso 1: Cifrado en Reposo y en Tránsito',
                        'amenaza': 'Intercepción de Datos en Red (Eavesdropping) y Fuga en Discos',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Datos bancarios confidenciales viajan en texto claro entre la web y '
                            'el servidor de pagos, y las bases de datos no cuentan con cifrado en sus discos físicos. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: El Control A.8.24 de ISO/IEC 27001:2022 requiere el uso efectivo '
                            'de criptografía para salvaguardar la confidencialidad e integridad de la información en tránsito y reposo.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Archimago del Cifrado de Extremo a Extremo',
                                'concepto': 'Control A.8.24 Uso de Criptografía',
                                'descripcion': 'Transforma datos legibles en código indescifrable en red y reposo.',
                                'es_correcta': True,
                                'fuerza': 92,
                                'defensa': 94,
                            },
                            {
                                'nombre': 'Centinela de los Enlaces Satelitales',
                                'concepto': 'Conectividad Remota Satelital',
                                'descripcion': 'Emite señales a larga distancia sin cifrado intrínseco.',
                                'es_correcta': False,
                                'fuerza': 65,
                                'defensa': 60,
                            },
                            {
                                'nombre': 'Herrero del Protocolo FTP',
                                'concepto': 'Transferencia Antigua en Texto Plano',
                                'descripcion': 'Transfiere archivos sin ninguna capa de seguridad criptográfica.',
                                'es_correcta': False,
                                'fuerza': 50,
                                'defensa': 45,
                            },
                            {
                                'nombre': 'Monje de la Tarjeta Madre',
                                'concepto': 'Arquitectura de Hardware Interno',
                                'descripcion': 'Coordina buses de hardware sin gestionar llaves criptográficas.',
                                'es_correcta': False,
                                'fuerza': 60,
                                'defensa': 58,
                            },
                        ],
                    },
                    {
                        'numero_fase': 2,
                        'titulo_incidente': 'Caso de Uso 2: Gestión del Ciclo de Vida de Llaves Criptográficas',
                        'amenaza': 'Compromiso de Llaves Privadas y Suplantación Criptográfica',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Las llaves privadas SSL y llaves de firmado digital están almacenadas '
                            'en un bloc de notas compartido y nunca han sido rotadas en los últimos 4 años. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: El Control A.8.24 de ISO/IEC 27001:2022 exige una estricta política '
                            'de gestión de llaves que regule su generación, distribución, almacenamiento seguro, rotación y revocación.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Guardián del Ciclo de Vida de Llaves Criptográficas',
                                'concepto': 'Control A.8.24 Gestión de Claves',
                                'descripcion': 'Custodia la generación, custodia segura y rotación periódica de llaves.',
                                'es_correcta': True,
                                'fuerza': 93,
                                'defensa': 91,
                            },
                            {
                                'nombre': 'Minotauro de las Rutas BGP',
                                'concepto': 'Enrutamiento Global de Internet',
                                'descripcion': 'Propaga prefijos de red sin gestionar certificados digitales.',
                                'es_correcta': False,
                                'fuerza': 67,
                                'defensa': 61,
                            },
                            {
                                'nombre': 'Vigía de la Tasa de Refresco',
                                'concepto': 'Frecuencia de Monitores Gráficos',
                                'descripcion': 'Controla hercios de pantalla sin conocimiento criptográfico.',
                                'es_correcta': False,
                                'fuerza': 52,
                                'defensa': 50,
                            },
                            {
                                'nombre': 'Oráculo del Proxy Reverso',
                                'concepto': 'Intermediario de Peticiones HTTP',
                                'descripcion': 'Reenvía paquetes sin gestionar bóvedas seguras de llaves.',
                                'es_correcta': False,
                                'fuerza': 66,
                                'defensa': 63,
                            },
                        ],
                    },
                    {
                        'numero_fase': 3,
                        'titulo_incidente': 'Caso de Uso 3: Segregación y Aislamiento de Redes Corporativas',
                        'amenaza': 'Movimiento Lateral de Atacantes entre Dispositivos y Servidores',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Las computadoras de visitantes, cámaras de seguridad y servidores '
                            'transaccionales conviven en la misma subred sin VLANs ni reglas de filtrado interno. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: El Control A.8.22 de ISO/IEC 27001:2022 establece la necesidad de '
                            'segregar las redes de información en dominios de seguridad para impedir movimientos laterales no autorizados.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Protector de la Segregación de Redes',
                                'concepto': 'Control A.8.22 Segregación de Redes',
                                'descripcion': 'Divide la infraestructura en zonas aisladas con control estricto de tráfico.',
                                'es_correcta': True,
                                'fuerza': 90,
                                'defensa': 92,
                            },
                            {
                                'nombre': 'Caballero del Cable Coaxial',
                                'concepto': 'Medio Físico de Transmisión Antiguo',
                                'descripcion': 'Conecta terminales en topología de bus compartida sin segmentación.',
                                'es_correcta': False,
                                'fuerza': 56,
                                'defensa': 52,
                            },
                            {
                                'nombre': 'Centinela del Puerto HDMI',
                                'concepto': 'Salida de Video Digital',
                                'descripcion': 'Muestra imágenes en monitores sin relación con firewalls ni VLANs.',
                                'es_correcta': False,
                                'fuerza': 50,
                                'defensa': 50,
                            },
                            {
                                'nombre': 'Espectro del Búfer Serial',
                                'concepto': 'Memoria Temporal de Comunicación',
                                'descripcion': 'Retiene bytes en conexiones COM sin segmentar dominios de red.',
                                'es_correcta': False,
                                'fuerza': 57,
                                'defensa': 55,
                            },
                        ],
                    },
                ],
            },
            {
                'numero_nivel': 4,
                'titulo': 'Gestión de Vulnerabilidades e Incidentes',
                'tipo': 'normal',
                'dificultad': 'normal',
                'recompensa_oro': 125,
                'recompensa_gemas': 25,
                'recompensa_xp': 250,
                'fases': [
                    {
                        'numero_fase': 1,
                        'titulo_incidente': 'Caso de Uso 1: Detección y Notificación Oportuna de Incidentes',
                        'amenaza': 'Retraso en la Respuesta y Agravamiento de Brechas de Seguridad',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Se detectó un acceso sospechoso con extracción masiva de datos en la '
                            'madrugada, pero los analistas no saben a quién reportar ni cómo escalar el incidente. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: El Control A.5.24 de ISO/IEC 27001:2022 requiere planificar y preparar '
                            'la gestión de incidentes con roles, responsabilidades y canales de escalamiento inmediatos.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Comandante de Respuesta a Incidentes de Seguridad',
                                'concepto': 'Control A.5.24 Gestión de Incidentes',
                                'descripcion': 'Coordina la detección, reporte, contención y erradicación de amenazas.',
                                'es_correcta': True,
                                'fuerza': 91,
                                'defensa': 90,
                            },
                            {
                                'nombre': 'Centinela del Rendimiento Gráfico',
                                'concepto': 'Métricas de Fotogramas por Segundo',
                                'descripcion': 'Monitorea renderizado 3D sin protocolos de contención de brechas.',
                                'es_correcta': False,
                                'fuerza': 58,
                                'defensa': 54,
                            },
                            {
                                'nombre': 'Vigía de la Fuente de Alimentación',
                                'concepto': 'Monitoreo Eléctrico de Hardware',
                                'descripcion': 'Verifica voltaje de watts sin capacidad de respuesta cibernética.',
                                'es_correcta': False,
                                'fuerza': 60,
                                'defensa': 61,
                            },
                            {
                                'nombre': 'Cazador de Paquetes Perdidos',
                                'concepto': 'Telemetría Básica de Conexión',
                                'descripcion': 'Identifica caídas de ping sin analizar naturaleza del ciberataque.',
                                'es_correcta': False,
                                'fuerza': 63,
                                'defensa': 59,
                            },
                        ],
                    },
                    {
                        'numero_fase': 2,
                        'titulo_incidente': 'Caso de Uso 2: Gestión de Vulnerabilidades y Parches Críticos',
                        'amenaza': 'Explotación de Fallas Conocidas y Falta de Actualización',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Se publicó una vulnerabilidad crítica con código exploit disponible '
                            'que afecta a los servidores web expuestos, y no existe un protocolo de parcheo prioritario. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: El Control A.8.8 de ISO/IEC 27001:2022 exige obtener información '
                            'oportuna sobre vulnerabilidades técnicas, evaluar su exposición y aplicar parches correctivos.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Cazador de Vulnerabilidades y Gestión de Parches',
                                'concepto': 'Control A.8.8 Gestión de Vulnerabilidades Técnicas',
                                'descripcion': 'Detecta fallas en sistemas y despliega actualizaciones correctivas urgentes.',
                                'es_correcta': True,
                                'fuerza': 92,
                                'defensa': 93,
                            },
                            {
                                'nombre': 'Titán de la Replicación Asíncrona',
                                'concepto': 'Copia Diferida de Bases de Datos',
                                'descripcion': 'Duplica bases de datos manteniendo intactas las mismas vulnerabilidades.',
                                'es_correcta': False,
                                'fuerza': 67,
                                'defensa': 64,
                            },
                            {
                                'nombre': 'Custodio de las Fuentes Tipográficas',
                                'concepto': 'Recursos Visuales del Sistema',
                                'descripcion': 'Gestiona fuentes de texto sin relación con la seguridad del kernel.',
                                'es_correcta': False,
                                'fuerza': 50,
                                'defensa': 48,
                            },
                            {
                                'nombre': 'Oráculo de la Tarjeta Gráfica',
                                'concepto': 'Aceleración de Video por Hardware',
                                'descripcion': 'Procesa texturas visuales sin capacidad de remediación de software.',
                                'es_correcta': False,
                                'fuerza': 61,
                                'defensa': 57,
                            },
                        ],
                    },
                    {
                        'numero_fase': 3,
                        'titulo_incidente': 'Caso de Uso 3: Cadena de Custodia y Preservación Forense',
                        'amenaza': 'Contaminación de Evidencia Digital y Pérdida de Trazabilidad Legal',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Un atacante comprometió un servidor central y los técnicos reiniciaron '
                            'el equipo, borrando la memoria RAM y alterando marcas de tiempo indispensables para la justicia. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: El Control A.5.28 de ISO/IEC 27001:2022 establece directrices para '
                            'identificar, recolectar, adquirir y preservar evidencia digital garantizando su admisibilidad forense.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Custodio de la Evidencia Forense y Cadena de Custodia',
                                'concepto': 'Control A.5.28 Recolección de Evidencias',
                                'descripcion': 'Preserva la memoria volátil y garantiza la integridad probatoria del incidente.',
                                'es_correcta': True,
                                'fuerza': 93,
                                'defensa': 95,
                            },
                            {
                                'nombre': 'Minotauro del Teclado Mecánico',
                                'concepto': 'Periférico de Entrada',
                                'descripcion': 'Registra pulsaciones físicas sin preservar imágenes forenses de disco.',
                                'es_correcta': False,
                                'fuerza': 55,
                                'defensa': 50,
                            },
                            {
                                'nombre': 'Vigía de la Compresión ZIP',
                                'concepto': 'Empaquetado de Archivos',
                                'descripcion': 'Comprime documentos pero no garantiza la inmutabilidad pericial.',
                                'es_correcta': False,
                                'fuerza': 60,
                                'defensa': 58,
                            },
                            {
                                'nombre': 'Arquitecto de Fuentes CSS',
                                'concepto': 'Hojas de Estilo en Cascada',
                                'descripcion': 'Define colores y fuentes en pantalla sin conocimiento forense.',
                                'es_correcta': False,
                                'fuerza': 48,
                                'defensa': 46,
                            },
                        ],
                    },
                ],
            },
            {
                'numero_nivel': 5,
                'titulo': 'Auditoría Crítica de Ciberseguridad (Jefe)',
                'tipo': 'jefe',
                'dificultad': 'dificil',
                'recompensa_oro': 200,
                'recompensa_gemas': 50,
                'recompensa_xp': 400,
                'fases': [
                    {
                        'numero_fase': 1,
                        'titulo_incidente': 'Caso de Uso 1: Tratamiento de No Conformidades Mayores',
                        'amenaza': 'Suspensión de la Certificación y Reincidencia de Brechas',
                        'dificultad': 'dificil',
                        'caso_contexto': (
                            'Escenario / Caso: El auditor externo descubre que durante el año no se realizaron auditorías '
                            'internas y múltiples controles de seguridad carecen de evidencia de ejecución. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 10.1 de ISO/IEC 27001:2022 requiere reaccionar ante '
                            'no conformidades, evaluar la necesidad de acciones para eliminar sus causas y evitar su repetición.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Gran Juez de No Conformidades y Acciones Correctivas',
                                'concepto': 'Cláusula 10.1 No Conformidad y Acción Correctiva',
                                'descripcion': 'Analiza causas raíces y ejecuta planes formales de corrección vinculante.',
                                'es_correcta': True,
                                'fuerza': 95,
                                'defensa': 96,
                            },
                            {
                                'nombre': 'Vigía de los Puntos de Restauración',
                                'concepto': 'Snapshots del Sistema Operativo',
                                'descripcion': 'Restaura el estado del sistema pero no resuelve la causa raíz de auditoría.',
                                'es_correcta': False,
                                'fuerza': 68,
                                'defensa': 65,
                            },
                            {
                                'nombre': 'Centinela del Scroll de Pantalla',
                                'concepto': 'Interacción de Navegación',
                                'descripcion': 'Controla desplazamiento de páginas web sin impacto en compliance.',
                                'es_correcta': False,
                                'fuerza': 50,
                                'defensa': 49,
                            },
                            {
                                'nombre': 'Dragón de las Líneas de Código',
                                'concepto': 'Métrica de Volumen de Programación',
                                'descripcion': 'Cuenta líneas de software sin validar cumplimiento de cláusulas ISO.',
                                'es_correcta': False,
                                'fuerza': 64,
                                'defensa': 62,
                            },
                        ],
                    },
                    {
                        'numero_fase': 2,
                        'titulo_incidente': 'Caso de Uso 2: Revisión por la Dirección del SGSI',
                        'amenaza': 'Desalineación Estratégica y Falta de Presupuesto en Ciberseguridad',
                        'dificultad': 'dificil',
                        'caso_contexto': (
                            'Escenario / Caso: La alta gerencia desconoce el estado de los controles de seguridad y '
                            'no se han presentado informes periódicos de riesgos ni resultados de auditoría previa. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 9.3 de ISO/IEC 27001:2022 exige que la alta dirección '
                            'revise el SGSI a intervalos planificados para asegurar su idoneidad, adecuación y eficacia continua.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Heraldo de la Revisión por la Dirección',
                                'concepto': 'Cláusula 9.3 Revisión por la Dirección',
                                'descripcion': 'Presenta el estado del SGSI al comité ejecutivo para asegurar recursos y rumbo.',
                                'es_correcta': True,
                                'fuerza': 94,
                                'defensa': 95,
                            },
                            {
                                'nombre': 'Caballero del Firmware de Impresoras',
                                'concepto': 'Software Embebido de Impresión',
                                'descripcion': 'Actualiza microcódigo de periféricos sin alcance en decisiones directivas.',
                                'es_correcta': False,
                                'fuerza': 58,
                                'defensa': 55,
                            },
                            {
                                'nombre': 'Espectro del Código Fuente',
                                'concepto': 'Repositorio de Desarrollo de Software',
                                'descripcion': 'Almacena scripts sin estructurar reportes ejecutivos para la dirección.',
                                'es_correcta': False,
                                'fuerza': 65,
                                'defensa': 60,
                            },
                            {
                                'nombre': 'Cazador de Píxeles Muertos',
                                'concepto': 'Diagnóstico de Paneles LCD',
                                'descripcion': 'Inspecciona pantallas de computadoras sin relación con la gobernanza.',
                                'es_correcta': False,
                                'fuerza': 49,
                                'defensa': 47,
                            },
                        ],
                    },
                    {
                        'numero_fase': 3,
                        'titulo_incidente': 'Caso de Uso 3: Evaluación de Eficacia y Mejora Continua',
                        'amenaza': 'Obsolescencia del SGSI y Pérdida de Eficacia en el Tiempo',
                        'dificultad': 'dificil',
                        'caso_contexto': (
                            'Escenario / Caso: Los controles se ejecutan por inercia pero la organización no cuenta '
                            'con indicadores clave (KPI) ni métricas para demostrar su grado de protección real. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: Las Cláusulas 9.1 y 10.2 de ISO/IEC 27001:2022 estipulan el monitoreo, '
                            'medición, análisis y evaluación constante para impulsar la mejora continua del SGSI.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Oráculo de la Medición de Eficacia y Mejora Continua',
                                'concepto': 'Cláusulas 9.1 y 10.2 Monitoreo y Mejora Continua',
                                'descripcion': 'Cuantifica el rendimiento del SGSI y optimiza permanentemente los controles.',
                                'es_correcta': True,
                                'fuerza': 96,
                                'defensa': 97,
                            },
                            {
                                'nombre': 'Titán de la Tasa de Muestreo',
                                'concepto': 'Captura de Audio y Señales',
                                'descripcion': 'Mide frecuencias acústicas sin evaluar métricas de cumplimiento normativo.',
                                'es_correcta': False,
                                'fuerza': 62,
                                'defensa': 60,
                            },
                            {
                                'nombre': 'Minotauro de los Controladores de Audio',
                                'concepto': 'Drivers de Tarjetas de Sonido',
                                'descripcion': 'Sincroniza parlantes sin vinculación con auditorías de seguridad.',
                                'es_correcta': False,
                                'fuerza': 54,
                                'defensa': 51,
                            },
                            {
                                'nombre': 'Guardián de la Resolución 4K',
                                'concepto': 'Definición de Imagen Ultra HD',
                                'descripcion': 'Asegura nitidez gráfica en monitores pero no mide la eficacia del SGSI.',
                                'es_correcta': False,
                                'fuerza': 57,
                                'defensa': 53,
                            },
                        ],
                    },
                ],
            },
        ],
    },
    {
        'orden': 2,
        'codigo_iso': 'ISO/IEC 27017',
        'nombre_tematico': 'Seguridad en la Nube',
        'dominio': 'Seguridad en Servicios Cloud (CSP y CSC)',
        'dificultad': 'normal',
        'niveles': [
            {
                'numero_nivel': 1,
                'titulo': 'Fundamentos de Seguridad Cloud (CSP vs CSC)',
                'tipo': 'normal',
                'dificultad': 'facil',
                'recompensa_oro': 60,
                'recompensa_gemas': 12,
                'recompensa_xp': 120,
                'fases': [
                    {
                        'numero_fase': 1,
                        'titulo_incidente': 'Caso de Uso 1: Matriz de Responsabilidad Compartida en Cloud',
                        'amenaza': 'Vacíos de Seguridad por Falta de Delimitación de Roles Cliente-Proveedor',
                        'dificultad': 'facil',
                        'caso_contexto': (
                            'Escenario / Caso: Ocurrió un fallo en el sistema operativo de una máquina virtual en IaaS '
                            'y el cliente culpa al proveedor sin entender que el parcheo del SO era su propia responsabilidad. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La norma ISO/IEC 27017 (Control CLD.6.1) establece que deben acordarse '
                            'y documentarse claramente los roles y responsabilidades compartidas entre el cliente y el proveedor de nube.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Guardián de la Responsabilidad Compartida Cloud',
                                'concepto': 'Control CLD.6.1 Roles y Responsabilidades Cloud',
                                'descripcion': 'Delimita con precisión matemática qué capas protege el proveedor y cuáles el cliente.',
                                'es_correcta': True,
                                'fuerza': 88,
                                'defensa': 91,
                            },
                            {
                                'nombre': 'Minotauro del Servidor Físico On-Premise',
                                'concepto': 'Infraestructura Tradicional Local',
                                'descripcion': 'Monitorea gabinetes locales desconociendo la elasticidad de la nube.',
                                'es_correcta': False,
                                'fuerza': 65,
                                'defensa': 60,
                            },
                            {
                                'nombre': 'Centinela del Puerto VGA',
                                'concepto': 'Conector Analógico de Video',
                                'descripcion': 'Enfocado en monitores antiguos sin alcance en arquitectura cloud.',
                                'es_correcta': False,
                                'fuerza': 52,
                                'defensa': 50,
                            },
                            {
                                'nombre': 'Vigía de la Cinta Magnética',
                                'concepto': 'Copia Física en Cinta',
                                'descripcion': 'Custodia cintas mecánicas sin gestionar contratos de nube pública.',
                                'es_correcta': False,
                                'fuerza': 58,
                                'defensa': 56,
                            },
                        ],
                    },
                    {
                        'numero_fase': 2,
                        'titulo_incidente': 'Caso de Uso 2: Segregación y Aislamiento Multi-Inquilino',
                        'amenaza': 'Contaminación Cruzada y Fuga de Datos entre Inquilinos Cloud',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Se requiere garantizar que en un entorno de cómputo en la nube compartida '
                            'ningún otro cliente vecino pueda acceder a la memoria volátil o disco de nuestras instancias. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: El Control CLD.6.3 de ISO/IEC 27017 exige la segregación lógica '
                            'y el aislamiento efectivo de entornos multi-inquilino para prevenir accesos cruzados indebidos.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Escudo del Aislamiento Multi-Inquilino',
                                'concepto': 'Control CLD.6.3 Segregación en Ambientes Virtuales',
                                'descripcion': 'Levanta barreras de hipervisor impenetrables entre diferentes inquilinos de la nube.',
                                'es_correcta': True,
                                'fuerza': 91,
                                'defensa': 93,
                            },
                            {
                                'nombre': 'Titán del Enfriamiento Líquido',
                                'concepto': 'Disipación Térmica de Servidores',
                                'descripcion': 'Enfría racks físicos sin aislar lógicamente la memoria de máquinas virtuales.',
                                'es_correcta': False,
                                'fuerza': 64,
                                'defensa': 62,
                            },
                            {
                                'nombre': 'Cazador de Clústeres Locales',
                                'concepto': 'Topología Monolítica Interna',
                                'descripcion': 'Opera sobre hardware propio sin dominar la multi-inquilinidad pública.',
                                'es_correcta': False,
                                'fuerza': 60,
                                'defensa': 58,
                            },
                            {
                                'nombre': 'Custodio del Cableado Estructurado',
                                'concepto': 'Canaletas y Patch Panels',
                                'descripcion': 'Organiza cables físicos pero es ciego ante la virtualización en la nube.',
                                'es_correcta': False,
                                'fuerza': 57,
                                'defensa': 55,
                            },
                        ],
                    },
                    {
                        'numero_fase': 3,
                        'titulo_incidente': 'Caso de Uso 3: Configuración Segura de Buckets de Almacenamiento',
                        'amenaza': 'Exposición Pública de Almacenamiento Cloud y Fuga Masiva',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Un repositorio de objetos S3 en la nube pública que contiene información '
                            'financiera de clientes quedó configurado con permisos de lectura pública a internet. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: El Control CLD.12.1 de ISO/IEC 27017 requiere la configuración segura, '
                            'restricción estricta de accesos y bloqueo por defecto de lecturas públicas en servicios de almacenamiento cloud.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Centinela de Protección de Buckets y Depósitos Cloud',
                                'concepto': 'Control CLD.12.1 Seguridad en Almacenamiento Cloud',
                                'descripcion': 'Cierra accesos públicos no autorizados y aplica políticas de cifrado forzado en buckets.',
                                'es_correcta': True,
                                'fuerza': 89,
                                'defensa': 92,
                            },
                            {
                                'nombre': 'Oráculo del Disco Duro IDE',
                                'concepto': 'Estándar Antiguo de Almacenamiento Físico',
                                'descripcion': 'Lee cilindros magnéticos locales desconociendo el almacenamiento en la nube.',
                                'es_correcta': False,
                                'fuerza': 54,
                                'defensa': 50,
                            },
                            {
                                'nombre': 'Sacerdote de la Consola Serial',
                                'concepto': 'Acceso por Cable de Diagnóstico',
                                'descripcion': 'Gestiona terminales físicas sin impacto en políticas de almacenamiento cloud.',
                                'es_correcta': False,
                                'fuerza': 59,
                                'defensa': 53,
                            },
                            {
                                'nombre': 'Espectro del Patch Cord',
                                'concepto': 'Cable de Red RJ-45',
                                'descripcion': 'Conecta puertos de red sin regular permisos en nubes virtuales.',
                                'es_correcta': False,
                                'fuerza': 52,
                                'defensa': 51,
                            },
                        ],
                    },
                ],
            },
            {
                'numero_nivel': 2,
                'titulo': 'Gestión de Identidades y Accesos Cloud (IAM)',
                'tipo': 'normal',
                'dificultad': 'normal',
                'recompensa_oro': 90,
                'recompensa_gemas': 18,
                'recompensa_xp': 180,
                'fases': [
                    {
                        'numero_fase': 1,
                        'titulo_incidente': 'Caso de Uso 1: Roles Efímeros y Privilegios Mínimos IAM',
                        'amenaza': 'Tokens de Administrador Permanentes y Fuga de Privilegios en la Nube',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Una función Serverless tiene permisos de administrador global sobre todas '
                            'las cuentas de la empresa en la nube en lugar de permisos restringidos a su tarea. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: El Control CLD.9.2 de ISO/IEC 27017 estipula la asignación granular '
                            'de accesos en la nube mediante roles y privilegios mínimos con vigencia temporal.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Custodio de Roles IAM y Políticas de Mínimo Privilegio',
                                'concepto': 'Control CLD.9.2 Gestión de Identidades y Accesos Cloud',
                                'descripcion': 'Entrega tokens temporales y roles con alcance quirúrgico a recursos cloud.',
                                'es_correcta': True,
                                'fuerza': 90,
                                'defensa': 93,
                            },
                            {
                                'nombre': 'Centinela del Conmutador KVM',
                                'concepto': 'Interruptor de Teclado, Video y Ratón',
                                'descripcion': 'Alterna pantallas en un centro de cómputo local sin conocimiento de IAM.',
                                'es_correcta': False,
                                'fuerza': 56,
                                'defensa': 52,
                            },
                            {
                                'nombre': 'Minotauro del Ratón Óptico',
                                'concepto': 'Dispositivo Puntero de Entrada',
                                'descripcion': 'Registra clics del usuario sin controlar políticas de acceso cloud.',
                                'es_correcta': False,
                                'fuerza': 50,
                                'defensa': 48,
                            },
                            {
                                'nombre': 'Titán de la Memoria EPROM',
                                'concepto': 'Memoria ROM Programable Antigua',
                                'descripcion': 'Conserva microcódigo físico sin intervenir en políticas de roles cloud.',
                                'es_correcta': False,
                                'fuerza': 60,
                                'defensa': 57,
                            },
                        ],
                    },
                    {
                        'numero_fase': 2,
                        'titulo_incidente': 'Caso de Uso 2: Protección y Rotación Automática de Secretos Cloud',
                        'amenaza': 'Exposición de Llaves de API y Acceso Total Ilegítimo',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Llaves de acceso de larga duración con permisos totales a la nube fueron '
                            'subidas accidentalmente a un repositorio de código público en GitHub por un programador. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: El Control CLD.9.5 de ISO/IEC 27017 requiere la protección '
                            'y rotación automática de credenciales programáticas y llaves de acceso en bóvedas seguras de nube.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Guardián del Almacén de Secretos y Rotación Automática',
                                'concepto': 'Control CLD.9.5 Bóveda de Secretos Cloud',
                                'descripcion': 'Invalida llaves expuestas y rota automáticamente credenciales mediante vaults seguros.',
                                'es_correcta': True,
                                'fuerza': 92,
                                'defensa': 91,
                            },
                            {
                                'nombre': 'Cazador de Antenas Wi-Fi',
                                'concepto': 'Recepción de Ondas Inalámbricas',
                                'descripcion': 'Capta señales de radio locales pero no gestiona tokens de acceso cloud.',
                                'es_correcta': False,
                                'fuerza': 62,
                                'defensa': 55,
                            },
                            {
                                'nombre': 'Vigía del Lápiz Óptico',
                                'concepto': 'Periférico de Dibujo Digital',
                                'descripcion': 'Interactúa con tabletas gráficas sin relación con la seguridad de APIs.',
                                'es_correcta': False,
                                'fuerza': 51,
                                'defensa': 49,
                            },
                            {
                                'nombre': 'Arquitecto de Cables SATA',
                                'concepto': 'Bus Serie de Discos Locales',
                                'descripcion': 'Conecta discos a la tarjeta madre sin intervenir en bóvedas de secretos.',
                                'es_correcta': False,
                                'fuerza': 57,
                                'defensa': 54,
                            },
                        ],
                    },
                    {
                        'numero_fase': 3,
                        'titulo_incidente': 'Caso de Uso 3: Federación de Identidades Cloud y Autenticación Única (SSO)',
                        'amenaza': 'Dispersión de Credenciales y Contraseñas Débiles en Múltiples SaaS',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Los colaboradores gestionan contraseñas independientes y desprotegidas '
                            'en 20 herramientas de nube diferentes, impidiendo revocar accesos de forma centralizada. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: El Control CLD.9.4 de ISO/IEC 27017 recomienda la federación de '
                            'identidades (SAML/OIDC) para centralizar la autenticación, aplicar MFA y auditar accesos a todas las aplicaciones cloud.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Heraldo de la Federación de Identidades y SSO Cloud',
                                'concepto': 'Control CLD.9.4 Identidad Federada en la Nube',
                                'descripcion': 'Unifica la identidad corporativa y permite revocación instantánea en todas las nubes.',
                                'es_correcta': True,
                                'fuerza': 91,
                                'defensa': 90,
                            },
                            {
                                'nombre': 'Espectro del Lector de DVD',
                                'concepto': 'Unidad Óptica de Lectura',
                                'descripcion': 'Lee discos láser locales sin capacidad de integración SAML.',
                                'es_correcta': False,
                                'fuerza': 53,
                                'defensa': 50,
                            },
                            {
                                'nombre': 'Caballero del Disco Flexible',
                                'concepto': 'Medio Magnético de 1.44MB',
                                'descripcion': 'Almacena datos minúsculos sin soporte para protocolos modernos de identidad.',
                                'es_correcta': False,
                                'fuerza': 48,
                                'defensa': 46,
                            },
                            {
                                'nombre': 'Cíclope del Panel Frontal',
                                'concepto': 'Luces LED de Gabinete',
                                'descripcion': 'Muestra actividad del disco físico sin gestionar sesiones web federadas.',
                                'es_correcta': False,
                                'fuerza': 55,
                                'defensa': 51,
                            },
                        ],
                    },
                ],
            },
            {
                'numero_nivel': 3,
                'titulo': 'Cifrado y Ciclo de Vida de Datos en la Nube',
                'tipo': 'normal',
                'dificultad': 'normal',
                'recompensa_oro': 120,
                'recompensa_gemas': 24,
                'recompensa_xp': 240,
                'fases': [
                    {
                        'numero_fase': 1,
                        'titulo_incidente': 'Caso de Uso 1: Gestión de Llaves Criptográficas Propias (BYOK)',
                        'amenaza': 'Descifrado Indebido de Datos por Terceros o Proveedores Cloud',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: La regulación financiera exige que la empresa posea control total y exclusivo '
                            'sobre las llaves de cifrado en la nube, garantizando que el proveedor no pueda descifrarlas. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: El Control CLD.9.5 de ISO/IEC 27017 establece que el cliente debe '
                            'mantener el control exclusivo sobre sus llaves de cifrado mediante mecanismos KMS y esquemas BYOK.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Señor del KMS y Llaves Propias del Cliente (BYOK)',
                                'concepto': 'Control CLD.9.5 Control de Llaves Criptográficas en Nube',
                                'descripcion': 'Mantiene la posesión absoluta de las llaves en módulos HSM sin injerencia del proveedor.',
                                'es_correcta': True,
                                'fuerza': 93,
                                'defensa': 94,
                            },
                            {
                                'nombre': 'Minotauro del Disco SCSI',
                                'concepto': 'Interfaz de Almacenamiento Antigua',
                                'descripcion': 'Conecta discos rígidos sin gestionar llaves criptográficas de nube.',
                                'es_correcta': False,
                                'fuerza': 61,
                                'defensa': 58,
                            },
                            {
                                'nombre': 'Centinela de la Torre ATX',
                                'concepto': 'Gabinete de Computador',
                                'descripcion': 'Estructura metálica sin conocimiento de algoritmos de cifrado en la nube.',
                                'es_correcta': False,
                                'fuerza': 54,
                                'defensa': 52,
                            },
                            {
                                'nombre': 'Oráculo de la Tarjeta de Red 10Mbps',
                                'concepto': 'Tarjeta Ethernet Obsoleta',
                                'descripcion': 'Transmite datos a baja velocidad sin bóvedas de claves de nube.',
                                'es_correcta': False,
                                'fuerza': 50,
                                'defensa': 49,
                            },
                        ],
                    },
                    {
                        'numero_fase': 2,
                        'titulo_incidente': 'Caso de Uso 2: Borrado Seguro y Desaprovisionamiento de Recursos Cloud',
                        'amenaza': 'Persistencia Residual de Datos Confidenciales en Medios Compartidos',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Al destruir una base de datos en la nube, se debe asegurar que ningún '
                            'bloque de almacenamiento físico residual conserve información recuperable por otros inquilinos. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: El Control CLD.8.1 de ISO/IEC 27017 exige la sanitización '
                            'y borrado seguro de los recursos de almacenamiento virtual desaprovisionados según estándares criptográficos.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Purificador del Borrado Seguro y Sanitización Cloud',
                                'concepto': 'Control CLD.8.1 Borrado Seguro de Activos de Nube',
                                'descripcion': 'Sobrescribe y destruye criptográficamente cualquier rastro de datos en bloques liberados.',
                                'es_correcta': True,
                                'fuerza': 90,
                                'defensa': 93,
                            },
                            {
                                'nombre': 'Titán del Papel Continuo',
                                'concepto': 'Papel de Impresión de Matriz',
                                'descripcion': 'Soporte físico de formularios sin relación con discos virtuales.',
                                'es_correcta': False,
                                'fuerza': 49,
                                'defensa': 46,
                            },
                            {
                                'nombre': 'Guardián del Escáner Plano',
                                'concepto': 'Digitalizador de Documentos',
                                'descripcion': 'Captura imágenes impresas sin gestionar el desaprovisionamiento en la nube.',
                                'es_correcta': False,
                                'fuerza': 55,
                                'defensa': 53,
                            },
                            {
                                'nombre': 'Vigía del Puerto Paralelo',
                                'concepto': 'Puerto LPT de Impresoras',
                                'descripcion': 'Comunica impresoras antiguas sin intervenir en la infraestructura de nube.',
                                'es_correcta': False,
                                'fuerza': 52,
                                'defensa': 50,
                            },
                        ],
                    },
                    {
                        'numero_fase': 3,
                        'titulo_incidente': 'Caso de Uso 3: Prevención de Pérdida de Datos Cloud (DLP)',
                        'amenaza': 'Exfiltración de Propiedad Intelectual desde Repositorios en la Nube',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Se detectó que empleados suben archivos con fórmulas y diseños patentados '
                            'hacia cuentas personales de almacenamiento en la nube sin autorización corporativa. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: El Control CLD.12.4 de ISO/IEC 27017 establece la necesidad de '
                            'monitorear y controlar la transferencia de datos para evitar la fuga de información sensible hacia nubes no gestionadas.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Centinela de Prevención de Fugas Cloud (DLP)',
                                'concepto': 'Control CLD.12.4 Prevención de Fuga de Información',
                                'descripcion': 'Inspecciona y bloquea la transferencia no autorizada de activos confidenciales hacia destinos cloud.',
                                'es_correcta': True,
                                'fuerza': 92,
                                'defensa': 91,
                            },
                            {
                                'nombre': 'Minotauro del Regulador de Voltaje',
                                'concepto': 'Estabilizador Eléctrico',
                                'descripcion': 'Evita picos de tensión sin inspeccionar el contenido de paquetes de datos.',
                                'es_correcta': False,
                                'fuerza': 61,
                                'defensa': 59,
                            },
                            {
                                'nombre': 'Cazador de Baterías CMOS',
                                'concepto': 'Batería de Reloj de Tarjeta Madre',
                                'descripcion': 'Alimenta la hora de la BIOS sin control sobre fugas de información.',
                                'es_correcta': False,
                                'fuerza': 50,
                                'defensa': 48,
                            },
                            {
                                'nombre': 'Custodio del Ventilador del Gabinete',
                                'concepto': 'Refrigeración de Aire',
                                'descripcion': 'Mueve aire dentro de una caja metálica sin filtrar tráfico de datos.',
                                'es_correcta': False,
                                'fuerza': 53,
                                'defensa': 51,
                            },
                        ],
                    },
                ],
            },
            {
                'numero_nivel': 4,
                'titulo': 'Monitoreo, Logs y Telemetría Cloud',
                'tipo': 'normal',
                'dificultad': 'normal',
                'recompensa_oro': 150,
                'recompensa_gemas': 30,
                'recompensa_xp': 300,
                'fases': [
                    {
                        'numero_fase': 1,
                        'titulo_incidente': 'Caso de Uso 1: Trazabilidad y Logs Inmutables en CloudTrail',
                        'amenaza': 'Borrado Malicioso de Auditoría y Falta de Evidencia Forense en la Nube',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Un atacante eliminó instancias de cómputo en la nube y los registros de '
                            'auditoría estaban almacenados en el mismo contenedor vulnerable, perdiéndose la trazabilidad del ataque. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: El Control CLD.12.4 de ISO/IEC 27017 exige registrar todas las '
                            'actividades de administración en la nube y proteger los logs de auditoría en depósitos inmutables con retención garantizada.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Vigía Inmutable de Registros y Telemetría CloudTrail',
                                'concepto': 'Control CLD.12.4 Registros de Auditoría Cloud',
                                'descripcion': 'Almacena bitácoras firmadas e inmutables con trazabilidad total de llamadas API en la nube.',
                                'es_correcta': True,
                                'fuerza': 93,
                                'defensa': 95,
                            },
                            {
                                'nombre': 'Espectro del Cable Null-Modem',
                                'concepto': 'Conexión Serial entre Dos PCs',
                                'descripcion': 'Conecta dos terminales físicas sin centralizar registros de nube.',
                                'es_correcta': False,
                                'fuerza': 54,
                                'defensa': 51,
                            },
                            {
                                'nombre': 'Caballero de la Tarjeta Fax',
                                'concepto': 'Módem Telefónico de Envío de Fax',
                                'descripcion': 'Transmite faxes analógicos desconociendo telemetría de eventos cloud.',
                                'es_correcta': False,
                                'fuerza': 49,
                                'defensa': 47,
                            },
                            {
                                'nombre': 'Cíclope de la Disquetera',
                                'concepto': 'Unidad de Almacenamiento Magnético',
                                'descripcion': 'Lee discos flexibles sin capacidad para almacenar gigabytes de auditoría.',
                                'es_correcta': False,
                                'fuerza': 51,
                                'defensa': 48,
                            },
                        ],
                    },
                    {
                        'numero_fase': 2,
                        'titulo_incidente': 'Caso de Uso 2: Protección Contra Ataques DDoS en Nube',
                        'amenaza': 'Denegación de Servicio Masiva y Desbordamiento de Costos de Cómputo',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Un ataque masivo de denegación de servicio distribuido satura los '
                            'balanceadores de carga en la nube provocando auto-escalamiento descontrolado y facturas astronómicas. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: El Control CLD.13.1 de ISO/IEC 27017 establece la necesidad de '
                            'implementar controles de mitigación anti-DDoS en el borde de la red cloud para absorber y filtrar tráfico malicioso.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Bastión Anti-DDoS y Blindaje de Perímetro Cloud',
                                'concepto': 'Control CLD.13.1 Mitigación de Ataques Distribuidos',
                                'descripcion': 'Filtra peticiones maliciosas en puntos de presencia globales antes de alcanzar los servidores.',
                                'es_correcta': True,
                                'fuerza': 94,
                                'defensa': 92,
                            },
                            {
                                'nombre': 'Minotauro de la Impresora de Matriz',
                                'concepto': 'Impresora de Agujas',
                                'descripcion': 'Imprime texto por impacto sin intervenir en ataques de red volumétricos.',
                                'es_correcta': False,
                                'fuerza': 52,
                                'defensa': 49,
                            },
                            {
                                'nombre': 'Cazador del Lápiz Infrarrojo',
                                'concepto': 'Sensor Óptico Infrarrojo',
                                'descripcion': 'Detecta haces de luz sin capacidad de mitigación de paquetes SYN flood.',
                                'es_correcta': False,
                                'fuerza': 50,
                                'defensa': 48,
                            },
                            {
                                'nombre': 'Oráculo del Transistor',
                                'concepto': 'Componente Electrónico Semiconductor',
                                'descripcion': 'Conmuta corriente eléctrica sin lógica de filtrado de tráfico web.',
                                'es_correcta': False,
                                'fuerza': 59,
                                'defensa': 55,
                            },
                        ],
                    },
                    {
                        'numero_fase': 3,
                        'titulo_incidente': 'Caso de Uso 3: Remediación Automatizada de Desviaciones de Seguridad',
                        'amenaza': 'Exposición Prolongada de Puertos por Errores Humanos de Configuración',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Desarrolladores abren accidentalmente puertos administrativos SSH '
                            'abiertos al mundo en sus grupos de seguridad, tardando días en ser detectados manualmente. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: El Control CLD.16.1 de ISO/IEC 27017 exige la monitorización continua '
                            'y remediación automática de desvíos en la postura de seguridad de la infraestructura en la nube.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Autómata de Detección y Remediación en Tiempo Real',
                                'concepto': 'Control CLD.16.1 Remediación Automática de Desvíos',
                                'descripcion': 'Detecta reglas inseguras en segundos y revierte automáticamente los permisos vulnerables.',
                                'es_correcta': True,
                                'fuerza': 91,
                                'defensa': 94,
                            },
                            {
                                'nombre': 'Titán de la Fuente Conmutada',
                                'concepto': 'Transformador Eléctrico de PC',
                                'descripcion': 'Transforma corriente alterna en continua sin evaluar políticas de grupos de seguridad.',
                                'es_correcta': False,
                                'fuerza': 62,
                                'defensa': 58,
                            },
                            {
                                'nombre': 'Guardián de la Cinta Perforada',
                                'concepto': 'Medio Primitivo de Entrada de Datos',
                                'descripcion': 'Lee perforaciones en papel sin relación con la automatización en la nube.',
                                'es_correcta': False,
                                'fuerza': 48,
                                'defensa': 46,
                            },
                            {
                                'nombre': 'Centinela del Teclado PS/2',
                                'concepto': 'Conector Mini-DIN de Periférico',
                                'descripcion': 'Comunica teclados antiguos desconociendo la infraestructura como código.',
                                'es_correcta': False,
                                'fuerza': 51,
                                'defensa': 50,
                            },
                        ],
                    },
                ],
            },
            {
                'numero_nivel': 5,
                'titulo': 'Auditoría Crítica de Arquitectura Cloud (Jefe)',
                'tipo': 'jefe',
                'dificultad': 'dificil',
                'recompensa_oro': 240,
                'recompensa_gemas': 60,
                'recompensa_xp': 480,
                'fases': [
                    {
                        'numero_fase': 1,
                        'titulo_incidente': 'Caso de Uso 1: Verificación de Reportes SOC e Informes del Proveedor CSP',
                        'amenaza': 'Falta de Garantía Contractual sobre la Seguridad del Proveedor Cloud',
                        'dificultad': 'dificil',
                        'caso_contexto': (
                            'Escenario / Caso: Un auditor exige evidencia formal de que los centros de datos físicos del '
                            'proveedor de nube cumplen con controles estrictos de seguridad que la empresa no puede inspeccionar físicamente. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: El Control CLD.15.1 de ISO/IEC 27017 establece la obligación de '
                            'revisar informes independientes de auditoría (SOC 1/2, ISO 27001) para evaluar la efectividad de los controles del CSP.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Gran Auditor de Reportes SOC e Informes del Proveedor',
                                'concepto': 'Control CLD.15.1 Supervisión de Servicios de Terceros Cloud',
                                'descripcion': 'Examina certificaciones de terceros y valida el cumplimiento estricto del proveedor de nube.',
                                'es_correcta': True,
                                'fuerza': 95,
                                'defensa': 96,
                            },
                            {
                                'nombre': 'Minotauro de la Bobina Térmica',
                                'concepto': 'Papel de Impresión de Recibos',
                                'descripcion': 'Imprime tickets térmicos sin capacidad probatoria en auditorías internacionales.',
                                'es_correcta': False,
                                'fuerza': 50,
                                'defensa': 48,
                            },
                            {
                                'nombre': 'Vigía del Tubo de Rayos Catódicos',
                                'concepto': 'Monitor CRT Antiguo',
                                'descripcion': 'Emite electrones para formar imágenes sin analizar informes de cumplimiento.',
                                'es_correcta': False,
                                'fuerza': 55,
                                'defensa': 52,
                            },
                            {
                                'nombre': 'Espectro del Búfer DMA',
                                'concepto': 'Acceso Directo a Memoria',
                                'descripcion': 'Acelera transferencias internas sin validar acuerdos de nivel de servicio.',
                                'es_correcta': False,
                                'fuerza': 61,
                                'defensa': 57,
                            },
                        ],
                    },
                    {
                        'numero_fase': 2,
                        'titulo_incidente': 'Caso de Uso 2: Auditoría de Grupos de Seguridad y Tráfico Este-Oeste',
                        'amenaza': 'Comunicaciones Permisivas entre Microservicios y Falta de Segmentación Cloud',
                        'dificultad': 'dificil',
                        'caso_contexto': (
                            'Escenario / Caso: Se detecta que cualquier pod de Kubernetes puede comunicarse libremente '
                            'con cualquier base de datos interna sin reglas de red que delimiten el tráfico Este-Oeste. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: El Control CLD.13.2 de ISO/IEC 27017 exige la segmentación estricta '
                            'de redes virtuales mediante políticas de red y security groups que bloqueen tráfico no autorizado entre servicios.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Inquisidor de Grupos de Seguridad y Reglas de Tráfico Cloud',
                                'concepto': 'Control CLD.13.2 Seguridad en Redes Virtuales Cloud',
                                'descripcion': 'Aplica políticas Zero Trust y corta comunicaciones arbitrarias entre microservicios.',
                                'es_correcta': True,
                                'fuerza': 94,
                                'defensa': 95,
                            },
                            {
                                'nombre': 'Caballero de la Placa Base AT',
                                'concepto': 'Factor de Forma Antiguo de Tarjeta Madre',
                                'descripcion': 'Soporta componentes físicos antiguos sin comprender redes superpuestas en la nube.',
                                'es_correcta': False,
                                'fuerza': 56,
                                'defensa': 53,
                            },
                            {
                                'nombre': 'Cazador del Puerto Joystick',
                                'concepto': 'Conector de Palancas de Mando',
                                'descripcion': 'Comunica periféricos de juego sin intervenir en topologías de red cloud.',
                                'es_correcta': False,
                                'fuerza': 51,
                                'defensa': 49,
                            },
                            {
                                'nombre': 'Titán de la Memoria Caché L1',
                                'concepto': 'Memoria Ultrarrápida del Procesador',
                                'descripcion': 'Almacena instrucciones de máquina sin gestionar firewalls virtuales.',
                                'es_correcta': False,
                                'fuerza': 64,
                                'defensa': 60,
                            },
                        ],
                    },
                    {
                        'numero_fase': 3,
                        'titulo_incidente': 'Caso de Uso 3: Resiliencia Multi-Región y Tolerancia a Fallos Cloud',
                        'amenaza': 'Pérdida Total de Servicio por Caída de una Región de Nube',
                        'dificultad': 'dificil',
                        'caso_contexto': (
                            'Escenario / Caso: Un apagón mayor inutilizó una región completa del proveedor cloud, '
                            'y la empresa tardó 48 horas en restablecer servicios por no contar con arquitectura multi-región. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: El Control CLD.17.1 de ISO/IEC 27017 establece la necesidad de '
                            'diseñar arquitecturas de alta disponibilidad con redundancia multi-zona y multi-región para soportar catástrofes del CSP.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Titán de la Arquitectura Multi-Región y Tolerancia a Desastres',
                                'concepto': 'Control CLD.17.1 Disponibilidad y Resiliencia Cloud',
                                'descripcion': 'Conmuta automáticamente el tráfico entre regiones geográficas ante desastres mayores.',
                                'es_correcta': True,
                                'fuerza': 96,
                                'defensa': 97,
                            },
                            {
                                'nombre': 'Centinela del Conector Molex',
                                'concepto': 'Enchufe Eléctrico de Alimentación Interna',
                                'descripcion': 'Alimenta discos duros sin alcance sobre la conmutación entre zonas de nube.',
                                'es_correcta': False,
                                'fuerza': 58,
                                'defensa': 55,
                            },
                            {
                                'nombre': 'Oráculo del Puerto FireWire',
                                'concepto': 'Interfaz IEEE 1394 de Alta Velocidad',
                                'descripcion': 'Transfiere video digital sin participar en balanceo global de regiones.',
                                'es_correcta': False,
                                'fuerza': 53,
                                'defensa': 51,
                            },
                            {
                                'nombre': 'Guardián del Chip BIOS',
                                'concepto': 'Firmware de Arranque de Placa Base',
                                'descripcion': 'Inicia el hardware de una máquina individual sin gestionar la redundancia de nube.',
                                'es_correcta': False,
                                'fuerza': 62,
                                'defensa': 58,
                            },
                        ],
                    },
                ],
            },
        ],
    },
    {
        'orden': 3,
        'codigo_iso': 'ISO/IEC 20000-1',
        'nombre_tematico': 'Gestión de Servicios de TI',
        'dominio': 'Gestión y Entrega de Servicios Tecnológicos (ITSM)',
        'dificultad': 'normal',
        'niveles': [
            {
                'numero_nivel': 1,
                'titulo': 'Fundamentos del SGS y Acuerdos de Nivel de Servicio',
                'tipo': 'normal',
                'dificultad': 'facil',
                'recompensa_oro': 70,
                'recompensa_gemas': 14,
                'recompensa_xp': 140,
                'fases': [
                    {
                        'numero_fase': 1,
                        'titulo_incidente': 'Caso de Uso 1: Definición y Monitoreo de Acuerdos SLA',
                        'amenaza': 'Incumplimiento de Expectativas y Falla en la Calidad del Servicio TI',
                        'dificultad': 'facil',
                        'caso_contexto': (
                            'Escenario / Caso: Los clientes corporativos se quejan de caídas constantes y no existen '
                            'tiempos pactados de respuesta ni umbrales de disponibilidad para medir el servicio. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 8.3.3 de ISO/IEC 20000-1 exige definir, acordar y monitorear '
                            'Acuerdos de Nivel de Servicio (SLA) para asegurar que los servicios cumplan con las necesidades del cliente.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Guardián de los Acuerdos de Nivel de Servicio (SLA)',
                                'concepto': 'Cláusula 8.3.3 Gestión de Niveles de Servicio',
                                'descripcion': 'Fija metas cuantitativas de disponibilidad y supervisa el cumplimiento pactado con el negocio.',
                                'es_correcta': True,
                                'fuerza': 89,
                                'defensa': 91,
                            },
                            {
                                'nombre': 'Minotauro del Driver de Escáner',
                                'concepto': 'Controlador de Periférico',
                                'descripcion': 'Comunica hardware de digitalización sin gestionar compromisos de servicio.',
                                'es_correcta': False,
                                'fuerza': 55,
                                'defensa': 52,
                            },
                            {
                                'nombre': 'Centinela del Puerto SCSI-2',
                                'concepto': 'Conector de Discos de Servidor Antiguo',
                                'descripcion': 'Transfiere bloques locales desconociendo acuerdos de satisfacción y SLAs.',
                                'es_correcta': False,
                                'fuerza': 58,
                                'defensa': 54,
                            },
                            {
                                'nombre': 'Vigía del Ventilador Auxiliar',
                                'concepto': 'Refrigeración Secundaria',
                                'descripcion': 'Disipa calor mecánico sin relación con indicadores de servicio de TI.',
                                'es_correcta': False,
                                'fuerza': 50,
                                'defensa': 48,
                            },
                        ],
                    },
                    {
                        'numero_fase': 2,
                        'titulo_incidente': 'Caso de Uso 2: Catálogo de Servicios y Base de Configuración (CMDB)',
                        'amenaza': 'Desconocimiento de Dependencias Críticas entre Servicios y Servidores',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Cuando se cae el sistema de facturación, los ingenieros no saben '
                            'qué servidores, bases de datos o contratos de proveedores están vinculados a dicha aplicación. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 8.2.4 de ISO/IEC 20000-1 requiere mantener un catálogo de '
                            'servicios actualizado y una CMDB con trazabilidad integral de todos los Ítems de Configuración (CI).'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Custodio de la CMDB y Catálogo Centralizado de Servicios',
                                'concepto': 'Cláusula 8.2.4 Catálogo de Servicios y Configuración',
                                'descripcion': 'Mantiene el mapa completo de relaciones y dependencias entre infraestructura y servicios.',
                                'es_correcta': True,
                                'fuerza': 91,
                                'defensa': 93,
                            },
                            {
                                'nombre': 'Cazador del Cable IDE Maestro',
                                'concepto': 'Bus Paralelo de Almacenamiento',
                                'descripcion': 'Conecta discos maestros sin modelar dependencias de servicios empresariales.',
                                'es_correcta': False,
                                'fuerza': 57,
                                'defensa': 53,
                            },
                            {
                                'nombre': 'Espectro de la Tarjeta Gráfica AGP',
                                'concepto': 'Ranura Antigua de Video',
                                'descripcion': 'Procesa gráficos en PCs de escritorio sin visión holística de ITSM.',
                                'es_correcta': False,
                                'fuerza': 53,
                                'defensa': 50,
                            },
                            {
                                'nombre': 'Titán del Lector de Código de Barras',
                                'concepto': 'Sensor Óptico de Inventario Físico',
                                'descripcion': 'Lee etiquetas de activos pero no gestiona topologías de servicios en la CMDB.',
                                'es_correcta': False,
                                'fuerza': 60,
                                'defensa': 56,
                            },
                        ],
                    },
                    {
                        'numero_fase': 3,
                        'titulo_incidente': 'Caso de Uso 3: Gestión de Capacidad y Demanda de Servicios TI',
                        'amenaza': 'Saturación Operativa y Degradación por Cargas de Trabajo Imprevistas',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Durante el cierre contable de fin de año los servidores colapsan '
                            'por sobrecarga de procesamiento no anticipada, paralizando la facturación corporativa. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 8.4 de ISO/IEC 20000-1 establece la obligación de planificar '
                            'y gestionar la capacidad y la demanda para garantizar que los recursos satisfagan las necesidades actuales y futuras.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Oráculo de Planificación de Capacidad y Demanda',
                                'concepto': 'Cláusula 8.4 Gestión de la Capacidad y Demanda',
                                'descripcion': 'Anticipa picos estacionales de carga y aprovisiona recursos antes del colapso operativo.',
                                'es_correcta': True,
                                'fuerza': 90,
                                'defensa': 92,
                            },
                            {
                                'nombre': 'Caballero del Bus ISA',
                                'concepto': 'Arquitectura de Bus de 16 bits',
                                'descripcion': 'Transfiere datos de hardware antiguo sin modelar curvas de demanda TI.',
                                'es_correcta': False,
                                'fuerza': 54,
                                'defensa': 51,
                            },
                            {
                                'nombre': 'Centinela del Cristal de Cuarzo',
                                'concepto': 'Oscilador de Frecuencia de Reloj',
                                'descripcion': 'Marca el pulso de los microcontroladores sin calcular capacidad computacional.',
                                'es_correcta': False,
                                'fuerza': 58,
                                'defensa': 55,
                            },
                            {
                                'nombre': 'Cíclope del Regulador Lineal',
                                'concepto': 'Control de Voltaje Eléctrico',
                                'descripcion': 'Estabiliza voltios en una placa sin evaluar la capacidad de infraestructura.',
                                'es_correcta': False,
                                'fuerza': 52,
                                'defensa': 49,
                            },
                        ],
                    },
                ],
            },
            {
                'numero_nivel': 2,
                'titulo': 'Gestión de Incidentes y Solicitudes de Servicio',
                'tipo': 'normal',
                'dificultad': 'normal',
                'recompensa_oro': 100,
                'recompensa_gemas': 20,
                'recompensa_xp': 200,
                'fases': [
                    {
                        'numero_fase': 1,
                        'titulo_incidente': 'Caso de Uso 1: Restauración Urgente ante Incidente Mayor TI',
                        'amenaza': 'Paralización de Operaciones Críticas y Pérdidas Comerciales Directas',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: La pasarela central de cobros se cayó a mitad de una jornada comercial '
                            'y las ventas están bloqueadas; el negocio exige restablecer el servicio a su estado normal de inmediato. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 8.6.1 de ISO/IEC 20000-1 define la gestión de incidentes '
                            'con el objetivo principal de restaurar la operación normal del servicio lo más rápido posible minimizando el impacto.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Comandante de Incidentes Mayores y Restauración Rápida',
                                'concepto': 'Cláusula 8.6.1 Gestión de Incidentes TI',
                                'descripcion': 'Moviliza brigadas técnicas y activa soluciones de contingencia para restaurar el servicio en minutos.',
                                'es_correcta': True,
                                'fuerza': 92,
                                'defensa': 91,
                            },
                            {
                                'nombre': 'Minotauro del Conector Coaxial BNC',
                                'concepto': 'Acoplador de Cable Antiguo',
                                'descripcion': 'Empalma cables de red sin capacidad de diagnóstico de fallas lógicas.',
                                'es_correcta': False,
                                'fuerza': 55,
                                'defensa': 50,
                            },
                            {
                                'nombre': 'Vigía del Disco Winchester',
                                'concepto': 'Primeros Discos Duros Sellados',
                                'descripcion': 'Custodia platos magnéticos antiguos sin procedimientos de restauración de servicios.',
                                'es_correcta': False,
                                'fuerza': 59,
                                'defensa': 56,
                            },
                            {
                                'nombre': 'Cazador de Líneas Telefónicas',
                                'concepto': 'Cable de Par de Cobre Analógico',
                                'descripcion': 'Rastrea tonos de discado sin intervenir en incidentes de aplicaciones transaccionales.',
                                'es_correcta': False,
                                'fuerza': 51,
                                'defensa': 49,
                            },
                        ],
                    },
                    {
                        'numero_fase': 2,
                        'titulo_incidente': 'Caso de Uso 2: Priorización por Matriz de Impacto y Urgencia',
                        'amenaza': 'Atención Invertida y Descuido de Incidentes Críticos por Solicitudes Menores',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: La mesa de ayuda atiende peticiones de cambio de mouse antes que la caída '
                            'del sistema de nómina porque los tickets se procesan por orden de llegada sin evaluar el daño al negocio. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 8.6.1 de ISO/IEC 20000-1 requiere clasificar y priorizar '
                            'todos los incidentes según su impacto en el negocio y la urgencia de resolución requerida.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Juez de la Matriz de Priorización e Impacto Operativo',
                                'concepto': 'Cláusula 8.6.1 Clasificación y Priorización de Incidentes',
                                'descripcion': 'Evalúa el daño financiero y usuarios afectados para asignar máxima prioridad a lo crítico.',
                                'es_correcta': True,
                                'fuerza': 91,
                                'defensa': 93,
                            },
                            {
                                'nombre': 'Centinela del Transformador de Corriente',
                                'concepto': 'Conversor de Voltaje de Red Eléctrica',
                                'descripcion': 'Reduce voltajes sin capacidad analítica para clasificar tickets de soporte.',
                                'es_correcta': False,
                                'fuerza': 60,
                                'defensa': 58,
                            },
                            {
                                'nombre': 'Titán del Cable Par Trenzado UTP',
                                'concepto': 'Cableado de Red Local Categoría 5',
                                'descripcion': 'Conecta jacks de red sin jerarquizar incidentes en el helpdesk.',
                                'es_correcta': False,
                                'fuerza': 56,
                                'defensa': 52,
                            },
                            {
                                'nombre': 'Espectro del Transmisor Óptico',
                                'concepto': 'Diodo Láser de Fibra Óptica',
                                'descripcion': 'Emite pulsos de luz sin evaluar prioridades de negocio en mesas de ayuda.',
                                'es_correcta': False,
                                'fuerza': 63,
                                'defensa': 59,
                            },
                        ],
                    },
                    {
                        'numero_fase': 3,
                        'titulo_incidente': 'Caso de Uso 3: Catálogo de Peticiones y Portal de Autoservicio',
                        'amenaza': 'Saturación del Soporte por Peticiones Rutinarias y Tiempos Largos de Espera',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Los ingenieros de infraestructura pierden el 40% de su jornada atendiendo '
                            'solicitudes manuales de cambio de contraseña e instalación de software estándar. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 8.6.2 de ISO/IEC 20000-1 estipula la gestión formal '
                            'de solicitudes de servicio separadas de incidentes, recomendando flujos automatizados de autoservicio.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Heraldo del Catálogo de Peticiones y Portal de Autoservicio',
                                'concepto': 'Cláusula 8.6.2 Gestión de Solicitudes de Servicio',
                                'descripcion': 'Automatiza la entrega de accesos y software estándar liberando a los ingenieros senior.',
                                'es_correcta': True,
                                'fuerza': 88,
                                'defensa': 90,
                            },
                            {
                                'nombre': 'Caballero del Soldador de Estaño',
                                'concepto': 'Herramienta de Reparación Electrónica',
                                'descripcion': 'Suelda componentes mecánicos sin impacto en flujos de autoservicio de TI.',
                                'es_correcta': False,
                                'fuerza': 52,
                                'defensa': 50,
                            },
                            {
                                'nombre': 'Oráculo del Jack de 3.5mm',
                                'concepto': 'Conector de Audio Analógico',
                                'descripcion': 'Transmite señales sonoras sin relacionarse con la gestión de tickets de servicio.',
                                'es_correcta': False,
                                'fuerza': 48,
                                'defensa': 47,
                            },
                            {
                                'nombre': 'Minotauro del Puerto RS-232',
                                'concepto': 'Interfaz Serial Antigua',
                                'descripcion': 'Conecta terminales mudas sin capacidades para portales de autoservicio web.',
                                'es_correcta': False,
                                'fuerza': 57,
                                'defensa': 54,
                            },
                        ],
                    },
                ],
            },
            {
                'numero_nivel': 3,
                'titulo': 'Control de Cambios y Configuración',
                'tipo': 'normal',
                'dificultad': 'normal',
                'recompensa_oro': 130,
                'recompensa_gemas': 26,
                'recompensa_xp': 260,
                'fases': [
                    {
                        'numero_fase': 1,
                        'titulo_incidente': 'Caso de Uso 1: Comité de Control de Cambios (CAB)',
                        'amenaza': 'Caídas del Entorno Productivo por Despliegues No Evaluados',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Un programador aplicó una modificación directa en la base de datos de producción '
                            'un viernes por la noche sin pruebas ni evaluación de riesgos, paralizando los servicios todo el fin de semana. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 8.5.1 de ISO/IEC 20000-1 establece el control estricto '
                            'de cambios y la evaluación formal de impacto, riesgos y plan de retroceso (rollback) mediante el CAB.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Canciller del Comité de Control de Cambios (CAB)',
                                'concepto': 'Cláusula 8.5.1 Gestión de Cambios',
                                'descripcion': 'Evalúa riesgos, aprueba ventanas de mantenimiento y exige planes de marcha atrás obligatorios.',
                                'es_correcta': True,
                                'fuerza': 93,
                                'defensa': 94,
                            },
                            {
                                'nombre': 'Vigía de la Cinta de Datos DLT',
                                'concepto': 'Unidad de Cartucho Magnético',
                                'descripcion': 'Almacena copias frías sin evaluar el impacto de cambios en código de producción.',
                                'es_correcta': False,
                                'fuerza': 58,
                                'defensa': 55,
                            },
                            {
                                'nombre': 'Centinela del Microprocesador 8086',
                                'concepto': 'Arquitectura de CPU Clásica',
                                'descripcion': 'Ejecuta instrucciones en ensamblador sin gobernar procesos organizacionales de TI.',
                                'es_correcta': False,
                                'fuerza': 62,
                                'defensa': 59,
                            },
                            {
                                'nombre': 'Cazador del Fusible Térmico',
                                'concepto': 'Protector de Sobrecarga Física',
                                'descripcion': 'Corta la corriente ante exceso de calor pero no previene cambios riesgosos en software.',
                                'es_correcta': False,
                                'fuerza': 54,
                                'defensa': 52,
                            },
                        ],
                    },
                    {
                        'numero_fase': 2,
                        'titulo_incidente': 'Caso de Uso 2: Procedimiento de Cambios de Emergencia (ECAB)',
                        'amenaza': 'Retrasos Fatales al Parchear Brechas de Seguridad en Tiempo Real',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Un ataque de seguridad en curso exige aplicar un parche crítico de inmediato, '
                            'pero el equipo no puede esperar 5 días a la sesión ordinaria del comité de cambios para actuar. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 8.5.1.3 de ISO/IEC 20000-1 define el procedimiento para '
                            'Cambios de Emergencia (ECAB), permitiendo autorizaciones ágiles con documentación y validación posterior.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Centinela de Cambios de Emergencia (ECAB)',
                                'concepto': 'Cláusula 8.5.1.3 Procedimiento de Cambio de Emergencia',
                                'descripcion': 'Habilita aprobación acelerada para neutralizar incidentes críticos con documentación inmediata.',
                                'es_correcta': True,
                                'fuerza': 92,
                                'defensa': 91,
                            },
                            {
                                'nombre': 'Minotauro de la Conexión Dial-Up',
                                'concepto': 'Acceso por Línea Conmutada',
                                'descripcion': 'Modula frecuencias acústicas sin capacidad de respuesta rápida en emergencias.',
                                'es_correcta': False,
                                'fuerza': 50,
                                'defensa': 47,
                            },
                            {
                                'nombre': 'Titán de la Memoria SRAM',
                                'concepto': 'Memoria Estática de Caché',
                                'descripcion': 'Mantiene datos volátiles sin gobernanza sobre despliegues críticos.',
                                'es_correcta': False,
                                'fuerza': 65,
                                'defensa': 61,
                            },
                            {
                                'nombre': 'Espectro de la Tarjeta Ethernet 10Base-T',
                                'concepto': 'Red Local Antigua',
                                'descripcion': 'Enruta tramas de red antiguas sin agilizar decisiones de emergencia.',
                                'es_correcta': False,
                                'fuerza': 56,
                                'defensa': 53,
                            },
                        ],
                    },
                    {
                        'numero_fase': 3,
                        'titulo_incidente': 'Caso de Uso 3: Auditoría y Verificación de la Configuración (CI)',
                        'amenaza': 'Desviación de Configuraciones no Autorizadas y Servidores Fantasma',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Se detectaron decenas de servidores virtuales desplegados en la red que no figuran '
                            'en la base de datos de configuración y nadie sabe qué servicios prestan ni quién es su dueño. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 8.2.5 de ISO/IEC 20000-1 requiere auditar periódicamente '
                            'los Ítems de Configuración (CI) para garantizar que la CMDB refleje exactamente la infraestructura real en producción.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Custodio de la Integridad de la Configuración y CI',
                                'concepto': 'Cláusula 8.2.5 Gestión de la Configuración',
                                'descripcion': 'Verifica la coincidencia estricta entre la infraestructura real y los registros de la CMDB.',
                                'es_correcta': True,
                                'fuerza': 91,
                                'defensa': 93,
                            },
                            {
                                'nombre': 'Oráculo del Cable Centronics',
                                'concepto': 'Cable de Impresión Paralelo IEEE 1284',
                                'descripcion': 'Transfiere caracteres a impresoras sin auditar servidores en la red.',
                                'es_correcta': False,
                                'fuerza': 52,
                                'defensa': 50,
                            },
                            {
                                'nombre': 'Caballero del Disco Magneto-Óptico',
                                'concepto': 'Almacenamiento Híbrido Reescribible',
                                'descripcion': 'Graba sectores con rayo láser y campo magnético sin conciliar CIs corporativos.',
                                'es_correcta': False,
                                'fuerza': 58,
                                'defensa': 55,
                            },
                            {
                                'nombre': 'Cíclope del Puente Rectificador',
                                'concepto': 'Componente de Electrónica de Potencia',
                                'descripcion': 'Convierte ondas sinusoidales sin registrar inventarios lógicos de TI.',
                                'es_correcta': False,
                                'fuerza': 61,
                                'defensa': 57,
                            },
                        ],
                    },
                ],
            },
            {
                'numero_nivel': 4,
                'titulo': 'Gestión de Problemas y Acuerdos de Soporte',
                'tipo': 'normal',
                'dificultad': 'normal',
                'recompensa_oro': 160,
                'recompensa_gemas': 32,
                'recompensa_xp': 320,
                'fases': [
                    {
                        'numero_fase': 1,
                        'titulo_incidente': 'Caso de Uso 1: Análisis de Causa Raíz (RCA) de Fallas Recurrentes',
                        'amenaza': 'Reincidencia Crónica de Incidentes y Desgaste del Equipo de Operaciones',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: El servidor de correo se reinicia espontáneamente cada semana y los técnicos '
                            'solo vuelven a encenderlo sin investigar el origen subyacente que provoca la falla. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 8.6.3 de ISO/IEC 20000-1 establece la gestión de problemas '
                            'para analizar la causa raíz de incidentes recurrentes y prevenir su reaparición definitiva.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Maestro del Análisis de Causa Raíz (RCA) y Problemas',
                                'concepto': 'Cláusula 8.6.3 Gestión de Problemas',
                                'descripcion': 'Investiga los fallos subyacentes y elimina definitivamente el origen de incidentes repetitivos.',
                                'es_correcta': True,
                                'fuerza': 94,
                                'defensa': 92,
                            },
                            {
                                'nombre': 'Centinela del Zócalo CPU',
                                'concepto': 'Socket de Procesador en Tarjeta Madre',
                                'descripcion': 'Fija físicamente el procesador sin realizar análisis metodológicos de causa raíz.',
                                'es_correcta': False,
                                'fuerza': 63,
                                'defensa': 60,
                            },
                            {
                                'nombre': 'Cazador del Cable SCSI Diferencial',
                                'concepto': 'Bus de Alta Tasa de Transferencia',
                                'descripcion': 'Comunica discos rígidos sin capacidad de análisis causa-efecto.',
                                'es_correcta': False,
                                'fuerza': 57,
                                'defensa': 54,
                            },
                            {
                                'nombre': 'Minotauro del Monitor Monocromático',
                                'concepto': 'Pantalla de Fósforo Verde',
                                'descripcion': 'Muestra terminales de texto sin relacionarse con el ciclo de vida de problemas.',
                                'es_correcta': False,
                                'fuerza': 51,
                                'defensa': 49,
                            },
                        ],
                    },
                    {
                        'numero_fase': 2,
                        'titulo_incidente': 'Caso de Uso 2: Base de Conocimiento y Errores Conocidos (KEDB)',
                        'amenaza': 'Pérdida de Tiempo Reinventando Soluciones ya Descubiertas',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Cuando surge un fallo en el ERP, los técnicos nuevos tardan horas '
                            'probando soluciones a ciegas porque el procedimiento de arreglo temporal no fue documentado. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 8.6.3 de ISO/IEC 20000-1 exige mantener una base de datos '
                            'de errores conocidos (KEDB) con soluciones provisionales (workarounds) documentadas y accesibles.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Sabio de la Base de Errores Conocidos (KEDB)',
                                'concepto': 'Cláusula 8.6.3 Registro de Errores Conocidos y Workarounds',
                                'descripcion': 'Documenta soluciones provisionales probadas para resolver incidentes en segundos.',
                                'es_correcta': True,
                                'fuerza': 91,
                                'defensa': 94,
                            },
                            {
                                'nombre': 'Titán del Papel Térmico',
                                'concepto': 'Consumible de Fax',
                                'descripcion': 'Imprime texto sensible al calor sin almacenar bases de conocimiento digital.',
                                'es_correcta': False,
                                'fuerza': 50,
                                'defensa': 48,
                            },
                            {
                                'nombre': 'Vigía del Tubo de Vacío',
                                'concepto': 'Válvula Termoiónica de Primera Generación',
                                'descripcion': 'Amplifica señales analógicas antiguas sin estructurar artículos de soporte.',
                                'es_correcta': False,
                                'fuerza': 58,
                                'defensa': 55,
                            },
                            {
                                'nombre': 'Espectro del Búfer de Impresión',
                                'concepto': 'Cola de Spooler de Documentos',
                                'descripcion': 'Gestiona impresiones pendientes sin registrar soluciones técnicas.',
                                'es_correcta': False,
                                'fuerza': 54,
                                'defensa': 51,
                            },
                        ],
                    },
                    {
                        'numero_fase': 3,
                        'titulo_incidente': 'Caso de Uso 3: Acuerdos de Nivel Operativo (OLA) Internos',
                        'amenaza': 'Echado de Culpas entre Áreas Internas y Retrasos al Resolver Tickets',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: El equipo de soporte al usuario no puede cumplir con sus clientes '
                            'porque el departamento interno de redes tarda 5 días en abrir un puerto de firewall sin compromisos formales. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 8.3.3 de ISO/IEC 20000-1 requiere establecer Acuerdos '
                            'de Nivel Operativo (OLA) entre áreas internas de la organización para sostener los SLA hacia el cliente.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Defensor de los Acuerdos Operativos Internos (OLA)',
                                'concepto': 'Cláusula 8.3.3 Acuerdos de Nivel Operativo (OLA)',
                                'descripcion': 'Compromete formalmente a las áreas internas de soporte técnico con tiempos de respuesta estrictos.',
                                'es_correcta': True,
                                'fuerza': 90,
                                'defensa': 92,
                            },
                            {
                                'nombre': 'Caballero del Ventilador de Chasis',
                                'concepto': 'Enfriamiento de Caja de Computador',
                                'descripcion': 'Expulsa aire caliente sin intervenir en acuerdos de cooperación entre áreas.',
                                'es_correcta': False,
                                'fuerza': 53,
                                'defensa': 50,
                            },
                            {
                                'nombre': 'Minotauro del Jack RJ-11',
                                'concepto': 'Conector Telefónico Clásico',
                                'descripcion': 'Enlaza cables de teléfono analógico sin regular tiempos de respuesta en el helpdesk.',
                                'es_correcta': False,
                                'fuerza': 51,
                                'defensa': 49,
                            },
                            {
                                'nombre': 'Oráculo del Transmisor Infrarrojo',
                                'concepto': 'Puerto IrDA de Comunicación Inalámbrica',
                                'descripcion': 'Conecta dispositivos por línea de vista sin alinear compromisos de soporte.',
                                'es_correcta': False,
                                'fuerza': 56,
                                'defensa': 53,
                            },
                        ],
                    },
                ],
            },
            {
                'numero_nivel': 5,
                'titulo': 'Auditoría Crítica de Calidad en Servicios TI (Jefe)',
                'tipo': 'jefe',
                'dificultad': 'dificil',
                'recompensa_oro': 280,
                'recompensa_gemas': 70,
                'recompensa_xp': 560,
                'fases': [
                    {
                        'numero_fase': 1,
                        'titulo_incidente': 'Caso de Uso 1: Gestión y Evaluación de Proveedores TI Críticos',
                        'amenaza': 'Degradación de Servicios por Dependencia de Terceros sin Control Contractual',
                        'dificultad': 'dificil',
                        'caso_contexto': (
                            'Escenario / Caso: Un proveedor externo de datacenter redujo su calidad y provocó caídas '
                            'masivas, pero el contrato carece de penalizaciones y de métricas periódicas de desempeño. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 8.3.4 de ISO/IEC 20000-1 exige gestionar y evaluar '
                            'regularmente a los proveedores externos para garantizar que cumplan con los requisitos de entrega del servicio.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Auditor del Desempeño y Gestión de Proveedores TI',
                                'concepto': 'Cláusula 8.3.4 Gestión de Proveedores',
                                'descripcion': 'Audita formalmente a terceros y vincula contratos a penalizaciones por incumplimiento de niveles de servicio.',
                                'es_correcta': True,
                                'fuerza': 95,
                                'defensa': 95,
                            },
                            {
                                'nombre': 'Centinela de la Pasta Térmica',
                                'concepto': 'Conductor Térmico de Disipadores',
                                'descripcion': 'Transfiere calor de silicio a cobre sin relación con contratos de proveedores.',
                                'es_correcta': False,
                                'fuerza': 55,
                                'defensa': 52,
                            },
                            {
                                'nombre': 'Cazador de la Ranura PCI',
                                'concepto': 'Ranura de Interconexión de Tarjetas',
                                'descripcion': 'Comunica tarjetas de red físicas sin supervisar acuerdos comerciales de TI.',
                                'es_correcta': False,
                                'fuerza': 58,
                                'defensa': 54,
                            },
                            {
                                'nombre': 'Titán del Condensador Electrolítico',
                                'concepto': 'Almacén de Energía en Placa Base',
                                'descripcion': 'Filtra rizado de corriente continua sin evaluar auditorías de terceros.',
                                'es_correcta': False,
                                'fuerza': 62,
                                'defensa': 59,
                            },
                        ],
                    },
                    {
                        'numero_fase': 2,
                        'titulo_incidente': 'Caso de Uso 2: Gestión de Continuidad y Disponibilidad del Servicio TI',
                        'amenaza': 'Inexistencia de Planes de Recuperación ante Caídas Catastróficas de TI',
                        'dificultad': 'dificil',
                        'caso_contexto': (
                            'Escenario / Caso: El auditor verifica que la empresa no ha probado la conmutación por error '
                            'hacia la infraestructura secundaria y no existen garantías de disponibilidad pactadas con el negocio. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 8.7 de ISO/IEC 20000-1 establece la necesidad de '
                            'planificar, verificar y mantener la continuidad y disponibilidad de los servicios de TI bajo contingencias.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Custodio de la Gestión de Continuidad del Servicio TI',
                                'concepto': 'Cláusula 8.7 Continuidad y Disponibilidad del Servicio',
                                'descripcion': 'Garantiza pruebas periódicas de recuperación y resiliencia para cumplir con los objetivos del SGS.',
                                'es_correcta': True,
                                'fuerza': 94,
                                'defensa': 96,
                            },
                            {
                                'nombre': 'Minotauro del Cable Coaxial Grueso (Thicknet)',
                                'concepto': 'Medio Físico 10Base5 Antiguo',
                                'descripcion': 'Transmite señales por cable vampiro sin planes de recuperación ante contingencias.',
                                'es_correcta': False,
                                'fuerza': 57,
                                'defensa': 53,
                            },
                            {
                                'nombre': 'Vigía del Diodo LED',
                                'concepto': 'Semiconductor Emisor de Luz',
                                'descripcion': 'Indica encendido de máquinas sin gestionar la disponibilidad del servicio.',
                                'es_correcta': False,
                                'fuerza': 50,
                                'defensa': 48,
                            },
                            {
                                'nombre': 'Espectro del Slot de Expansión',
                                'concepto': 'Conector de Tarjetas en Placa Base',
                                'descripcion': 'Acopla circuitos sin modelar estrategias de recuperación tecnológica.',
                                'es_correcta': False,
                                'fuerza': 60,
                                'defensa': 57,
                            },
                        ],
                    },
                    {
                        'numero_fase': 3,
                        'titulo_incidente': 'Caso de Uso 3: Plan de Mejora Continua del Servicio (SIP)',
                        'amenaza': 'Estancamiento de la Calidad y Pérdida Progresiva de Clientes',
                        'dificultad': 'dificil',
                        'caso_contexto': (
                            'Escenario / Caso: Las encuestas de satisfacción revelan insatisfacción de los usuarios corporativos '
                            'y la dirección de TI no cuenta con un programa estructurado de acciones para elevar la calidad. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 10.1 de ISO/IEC 20000-1 requiere identificar y evaluar '
                            'oportunidades de mejora, implementando un Plan de Mejora del Servicio (SIP) con objetivos medibles.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Arquitecto del Plan de Mejora Continua del Servicio (SIP)',
                                'concepto': 'Cláusula 10.1 Mejora Continua del SGS',
                                'descripcion': 'Transforma la retroalimentación de clientes en proyectos formales de optimización operativa.',
                                'es_correcta': True,
                                'fuerza': 96,
                                'defensa': 97,
                            },
                            {
                                'nombre': 'Caballero del Conector DB-25',
                                'concepto': 'Puerto Serial/Paralelo Clásico',
                                'descripcion': 'Acopla cables de 25 pines sin intervenir en encuestas de satisfacción ni calidad.',
                                'es_correcta': False,
                                'fuerza': 52,
                                'defensa': 50,
                            },
                            {
                                'nombre': 'Oráculo del Cristal Oscilador',
                                'concepto': 'Reloj Electrónico de Microchips',
                                'descripcion': 'Sincroniza microcircuitos sin capacidad para estructurar planes SIP.',
                                'es_correcta': False,
                                'fuerza': 58,
                                'defensa': 55,
                            },
                            {
                                'nombre': 'Cíclope del Bobinado de Inducción',
                                'concepto': 'Inductor Electromagnético',
                                'descripcion': 'Filtra armónicos de corriente sin relación con la satisfacción de usuarios.',
                                'es_correcta': False,
                                'fuerza': 61,
                                'defensa': 58,
                            },
                        ],
                    },
                ],
            },
        ],
    },
    {
        'orden': 4,
        'codigo_iso': 'ISO 22301',
        'nombre_tematico': 'Continuidad del Negocio',
        'dominio': 'Resiliencia Operativa y Planes de Continuidad',
        'dificultad': 'dificil',
        'niveles': [
            {
                'numero_nivel': 1,
                'titulo': 'Análisis de Impacto en el Negocio (BIA)',
                'tipo': 'normal',
                'dificultad': 'facil',
                'recompensa_oro': 80,
                'recompensa_gemas': 16,
                'recompensa_xp': 160,
                'fases': [
                    {
                        'numero_fase': 1,
                        'titulo_incidente': 'Caso de Uso 1: Identificación de Procesos Críticos y Evaluación BIA',
                        'amenaza': 'Incapacidad de Priorizar Operaciones Vitales ante una Crisis',
                        'dificultad': 'facil',
                        'caso_contexto': (
                            'Escenario / Caso: Ante un apagón mayor en el edificio corporativo, los líderes intentan '
                            'levantar todos los departamentos al tiempo sin saber cuáles son las actividades vitales que generan ingresos y salvan vidas. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 8.2.2 de ISO 22301 exige realizar un Análisis de Impacto '
                            'en el Negocio (BIA) para clasificar las actividades críticas y cuantificar el impacto temporal de su interrupción.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Mapeador de Procesos Críticos y Priorización BIA',
                                'concepto': 'Cláusula 8.2.2 Análisis de Impacto en el Negocio',
                                'descripcion': 'Identifica qué actividades son vitales para la supervivencia de la entidad y deben reactivarse de inmediato.',
                                'es_correcta': True,
                                'fuerza': 90,
                                'defensa': 92,
                            },
                            {
                                'nombre': 'Minotauro del Bobinado Primario',
                                'concepto': 'Devanado de Transformador Eléctrico',
                                'descripcion': 'Induce voltaje en cobre sin discernir la criticidad de los procesos del negocio.',
                                'es_correcta': False,
                                'fuerza': 58,
                                'defensa': 55,
                            },
                            {
                                'nombre': 'Centinela del Ventilador CPU',
                                'concepto': 'Disipador Térmico de Microprocesador',
                                'descripcion': 'Enfría silicio sin evaluar prioridades operativas de continuidad.',
                                'es_correcta': False,
                                'fuerza': 52,
                                'defensa': 49,
                            },
                            {
                                'nombre': 'Vigía de la Cinta de Papel',
                                'concepto': 'Medio Perforado de Lectura',
                                'descripcion': 'Registra secuencias de caracteres sin metodología de impacto en el negocio.',
                                'es_correcta': False,
                                'fuerza': 50,
                                'defensa': 48,
                            },
                        ],
                    },
                    {
                        'numero_fase': 2,
                        'titulo_incidente': 'Caso de Uso 2: Determinación del RTO (Tiempo de Recuperación Objetivo)',
                        'amenaza': 'Tardanza Excesiva en Recuperar Aplicaciones y Colapso Comercial',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: La dirección debe establecer el tiempo límite inaplazable en que la '
                            'aplicación de compras y pagos debe estar operando tras un siniestro antes de sufrir sanciones regulatorias. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 8.2.2 de ISO 22301 exige calcular el RTO (Recovery Time '
                            'Objective) para fijar el tiempo máximo aceptable de recuperación de un proceso interrumpido.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Cronómetro del RTO (Tiempo de Recuperación Objetivo)',
                                'concepto': 'Cláusula 8.2.2 Cálculo de RTO en el BIA',
                                'descripcion': 'Establece el lapso límite improrrogable para restaurar servicios antes de daños graves.',
                                'es_correcta': True,
                                'fuerza': 91,
                                'defensa': 91,
                            },
                            {
                                'nombre': 'Titán del Enlace Dial-Up',
                                'concepto': 'Módem Telefónico de Datos',
                                'descripcion': 'Establece conexiones lentas sin calcular límites temporales de recuperación.',
                                'es_correcta': False,
                                'fuerza': 53,
                                'defensa': 50,
                            },
                            {
                                'nombre': 'Cazador del Circuito Integrado',
                                'concepto': 'Microchip Electrónico',
                                'descripcion': 'Integra compuertas lógicas sin gobernar métricas de continuidad del negocio.',
                                'es_correcta': False,
                                'fuerza': 60,
                                'defensa': 57,
                            },
                            {
                                'nombre': 'Espectro del Búfer DMA',
                                'concepto': 'Canal de Transferencia en Memoria',
                                'descripcion': 'Mueve bytes entre periféricos sin estimar impactos temporales de recuperación.',
                                'es_correcta': False,
                                'fuerza': 57,
                                'defensa': 54,
                            },
                        ],
                    },
                    {
                        'numero_fase': 3,
                        'titulo_incidente': 'Caso de Uso 3: Determinación del RPO (Punto Objetivo de Recuperación)',
                        'amenaza': 'Pérdida Irrecuperable de Transacciones Financieras Recientes',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: El sistema contable no puede permitirse perder más de 10 minutos de datos '
                            'ante un fallo catastrófico, pero los respaldos actuales solo se ejecutan una vez cada 24 horas. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 8.2.2 de ISO 22301 establece la definición del RPO '
                            '(Recovery Point Objective) para determinar la cantidad máxima tolerable de datos que se pueden perder.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Guardián del RPO y Tolerancia de Pérdida de Datos',
                                'concepto': 'Cláusula 8.2.2 Cálculo de RPO en el BIA',
                                'descripcion': 'Fija la frecuencia de replicación para garantizar que la pérdida de datos no supere el umbral tolerable.',
                                'es_correcta': True,
                                'fuerza': 92,
                                'defensa': 93,
                            },
                            {
                                'nombre': 'Caballero del Puerto Serial',
                                'concepto': 'Línea COM de Comunicación',
                                'descripcion': 'Transmite bits en fila sin regular puntos objetivos de restauración de datos.',
                                'es_correcta': False,
                                'fuerza': 54,
                                'defensa': 51,
                            },
                            {
                                'nombre': 'Minotauro del Conector DIN',
                                'concepto': 'Enchufe Circular de Audio y Teclado',
                                'descripcion': 'Conecta clavijas circulares sin impacto en la tolerancia de pérdida de transacciones.',
                                'es_correcta': False,
                                'fuerza': 49,
                                'defensa': 47,
                            },
                            {
                                'nombre': 'Oráculo del Fusible de Cerámica',
                                'concepto': 'Protección Contra Sobrecorriente',
                                'descripcion': 'Interrumpe circuitos eléctricos sin evaluar políticas de sincronización de datos.',
                                'es_correcta': False,
                                'fuerza': 58,
                                'defensa': 55,
                            },
                        ],
                    },
                ],
            },
            {
                'numero_nivel': 2,
                'titulo': 'Evaluación de Riesgos y Estrategias de Resiliencia',
                'tipo': 'normal',
                'dificultad': 'normal',
                'recompensa_oro': 110,
                'recompensa_gemas': 22,
                'recompensa_xp': 220,
                'fases': [
                    {
                        'numero_fase': 1,
                        'titulo_incidente': 'Caso de Uso 1: Evaluación de Amenazas y Riesgos Disruptivos',
                        'amenaza': 'Vulnerabilidad ante Fenómenos Naturales y Catástrofes Ambientales',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: La planta principal fue construida en zona inundable y la compañía no cuenta '
                            'con una matriz que identifique riesgos de desastres naturales ni planes de contingencia asociados. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 8.2.3 de ISO 22301 exige evaluar sistemáticamente los '
                            'riesgos de interrupción, identificando amenazas verosímiles y su potencial para perturbar las operaciones.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Centinela de Amenazas y Riesgos Disruptivos',
                                'concepto': 'Cláusula 8.2.3 Evaluación de Riesgos Disruptivos',
                                'descripcion': 'Identifica y evalúa eventos adversos naturales, tecnológicos y humanos capaces de detener la empresa.',
                                'es_correcta': True,
                                'fuerza': 91,
                                'defensa': 92,
                            },
                            {
                                'nombre': 'Vigía del Tubo de Enfriamiento',
                                'concepto': 'Canal de Disipación Líquida',
                                'descripcion': 'Fluye líquido refrigerante sin calcular probabilidades de riesgos ambientales.',
                                'es_correcta': False,
                                'fuerza': 57,
                                'defensa': 54,
                            },
                            {
                                'nombre': 'Cazador de la Ranura AGP',
                                'concepto': 'Puerto Gráfico Acelerado',
                                'descripcion': 'Conecta tarjetas de video sin relación con mapas de amenazas geográficas.',
                                'es_correcta': False,
                                'fuerza': 52,
                                'defensa': 50,
                            },
                            {
                                'nombre': 'Titán de la Memoria EDO',
                                'concepto': 'Memoria RAM de los Años 90',
                                'descripcion': 'Retiene ciclos de datos sin participar en la evaluación de continuidad del negocio.',
                                'es_correcta': False,
                                'fuerza': 59,
                                'defensa': 56,
                            },
                        ],
                    },
                    {
                        'numero_fase': 2,
                        'titulo_incidente': 'Caso de Uso 2: Estrategia de Redundancia y Datacenter Alterno',
                        'amenaza': 'Pérdida Total de Sede Física sin Sitio Secundario de Operaciones',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Un incendio destruye la sede central y la organización no dispone de contratos '
                            'de contingencia con sitios alternos (Cold/Warm/Hot site) para reinstalar a sus operadores clave. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 8.3 de ISO 22301 exige seleccionar e implementar estrategias '
                            'y soluciones de continuidad, incluyendo instalaciones alternativas y recursos redundantes de respaldo.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Arquitecto de Estrategias de Continuidad y Sitio Alterno',
                                'concepto': 'Cláusula 8.3 Estrategias y Soluciones de Continuidad',
                                'descripcion': 'Diseña e implementa sedes de contingencia e infraestructura redundante lista para operar.',
                                'es_correcta': True,
                                'fuerza': 93,
                                'defensa': 94,
                            },
                            {
                                'nombre': 'Minotauro de la Disquetera de 5¼',
                                'concepto': 'Lector de Discos de Cartón Flexible',
                                'descripcion': 'Gira discos primitivos sin diseñar arquitecturas de sitios espejo de respaldo.',
                                'es_correcta': False,
                                'fuerza': 48,
                                'defensa': 46,
                            },
                            {
                                'nombre': 'Espectro del Panel Solar Auxiliar',
                                'concepto': 'Captador Fotovoltaico Menor',
                                'descripcion': 'Genera vatios para baterías sin modelar estrategias completas de continuidad operativa.',
                                'es_correcta': False,
                                'fuerza': 61,
                                'defensa': 58,
                            },
                            {
                                'nombre': 'Cíclope del Multímetro Analógico',
                                'concepto': 'Instrumento de Aguja de Voltaje',
                                'descripcion': 'Mide ohmios en cables sin estructurar contratos de sitios alternos de cómputo.',
                                'es_correcta': False,
                                'fuerza': 54,
                                'defensa': 51,
                            },
                        ],
                    },
                    {
                        'numero_fase': 3,
                        'titulo_incidente': 'Caso de Uso 3: Resiliencia en la Cadena de Suministro y Proveedores',
                        'amenaza': 'Quiebra Imprevista de Proveedores Únicos de Telecomunicaciones o Energía',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: El único proveedor de enlaces de fibra óptica de la empresa colapsa '
                            'sin que existan contratos de respaldo ni proveedores secundarios con rutas de red alternativas. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 8.3 de ISO 22301 establece que las soluciones de continuidad '
                            'deben cubrir explícitamente la cadena de suministro y la resiliencia de proveedores críticos esenciales.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Protector de la Cadena de Suministro y Proveedores Críticos',
                                'concepto': 'Cláusula 8.3 Resiliencia en la Cadena de Suministro',
                                'descripcion': 'Garantiza proveedores redundantes y acuerdos de soporte con respuesta prioritaria ante desastres.',
                                'es_correcta': True,
                                'fuerza': 90,
                                'defensa': 92,
                            },
                            {
                                'nombre': 'Caballero del Soldador de Gas',
                                'concepto': 'Herramienta Térmica de Gas Butano',
                                'descripcion': 'Funde estaño portátil sin evaluar riesgos en la cadena de suministro internacional.',
                                'es_correcta': False,
                                'fuerza': 53,
                                'defensa': 50,
                            },
                            {
                                'nombre': 'Oráculo del Relé Electromecánico',
                                'concepto': 'Conmutador Magnético de Contactos',
                                'descripcion': 'Abre y cierra contactos eléctricos sin gestionar acuerdos con proveedores externos.',
                                'es_correcta': False,
                                'fuerza': 59,
                                'defensa': 56,
                            },
                            {
                                'nombre': 'Centinela del Jack RCA',
                                'concepto': 'Conector de Audio/Video Compuesto',
                                'descripcion': 'Transmite señales de televisión analógica sin relación con redes de suministro corporativas.',
                                'es_correcta': False,
                                'fuerza': 50,
                                'defensa': 48,
                            },
                        ],
                    },
                ],
            },
            {
                'numero_nivel': 3,
                'titulo': 'Planes de Continuidad (BCP) y Recuperación (DRP)',
                'tipo': 'normal',
                'dificultad': 'normal',
                'recompensa_oro': 140,
                'recompensa_gemas': 28,
                'recompensa_xp': 280,
                'fases': [
                    {
                        'numero_fase': 1,
                        'titulo_incidente': 'Caso de Uso 1: Activación y Procedimientos del Plan de Continuidad (BCP)',
                        'amenaza': 'Caos Operativo y Falta de Protocolos Escritos para Trabajar en Contingencia',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Una fuga de gas tóxico en el parque industrial obliga a desalojar las oficinas '
                            'y el personal desconoce los protocolos documentados para reanudar operaciones de forma distribuida. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 8.4.2 de ISO 22301 exige documentar y mantener procedimientos '
                            'claros en el Plan de Continuidad del Negocio (BCP) para guiar la respuesta y continuidad de las actividades críticas.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Comandante del Plan de Continuidad del Negocio (BCP)',
                                'concepto': 'Cláusula 8.4.2 Planes y Procedimientos de Continuidad',
                                'descripcion': 'Activa directrices paso a paso para mantener el negocio operando durante y después del incidente.',
                                'es_correcta': True,
                                'fuerza': 92,
                                'defensa': 93,
                            },
                            {
                                'nombre': 'Titán del Potenciómetro',
                                'concepto': 'Resistencia Variable de Circuito',
                                'descripcion': 'Regula volumen o voltaje sin proveer procedimientos documentados de respuesta a emergencias.',
                                'es_correcta': False,
                                'fuerza': 55,
                                'defensa': 52,
                            },
                            {
                                'nombre': 'Cazador de la Clavija Telefónica',
                                'concepto': 'Conector Hembra de Conmutador',
                                'descripcion': 'Enruta llamadas de operadora manual sin estructurar planes BCP de negocio.',
                                'es_correcta': False,
                                'fuerza': 51,
                                'defensa': 49,
                            },
                            {
                                'nombre': 'Minotauro del Zócalo ISA',
                                'concepto': 'Ranura de Tarjetas Clásica',
                                'descripcion': 'Comunica tarjetas de cómputo antiguas sin capacidad de liderazgo en contingencias.',
                                'es_correcta': False,
                                'fuerza': 58,
                                'defensa': 55,
                            },
                        ],
                    },
                    {
                        'numero_fase': 2,
                        'titulo_incidente': 'Caso de Uso 2: Plan de Recuperación ante Desastres Tecnológicos (DRP)',
                        'amenaza': 'Destrucción de Bases de Datos por Ransomware y Falta de Restauración de TI',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Un ataque cibernético cifró todos los servidores del centro de cómputo; '
                            'se requiere restaurar la infraestructura tecnológica, sistemas y respaldos desde la bóveda aislada. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 8.4.4 de ISO 22301 estipula el desarrollo de planes '
                            'técnicos de recuperación ante desastres (DRP) para restaurar y recuperar sistemas y tecnologías tras una interrupción.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Estratega del Plan de Recuperación Tecnológica (DRP)',
                                'concepto': 'Cláusula 8.4.4 Recuperación Tecnológica ante Desastres',
                                'descripcion': 'Restaura servidores, bases de datos y telecomunicaciones de contingencia en estricto orden técnico.',
                                'es_correcta': True,
                                'fuerza': 94,
                                'defensa': 95,
                            },
                            {
                                'nombre': 'Vigía de la Cinta Perforada',
                                'concepto': 'Registro Físico de Caracteres',
                                'descripcion': 'Guarda datos en rollos de papel sin restaurar clústeres modernos de servidores.',
                                'es_correcta': False,
                                'fuerza': 50,
                                'defensa': 48,
                            },
                            {
                                'nombre': 'Espectro del Búfer Gráfico',
                                'concepto': 'VRAM de Tarjetas de Video',
                                'descripcion': 'Retiene píxeles en pantalla sin orquestar restauraciones de infraestructura DRP.',
                                'es_correcta': False,
                                'fuerza': 56,
                                'defensa': 53,
                            },
                            {
                                'nombre': 'Centinela del Diodo Zener',
                                'concepto': 'Regulador de Tensión en Avalancha',
                                'descripcion': 'Estabiliza voltajes en placas sin relación con planes de desastres tecnológicos.',
                                'es_correcta': False,
                                'fuerza': 59,
                                'defensa': 57,
                            },
                        ],
                    },
                    {
                        'numero_fase': 3,
                        'titulo_incidente': 'Caso de Uso 3: Plan de Comunicación y Gestión de Crisis',
                        'amenaza': 'Pánico Colectivo, Declaraciones Falsas y Daño Reputacional en Medios',
                        'dificultad': 'normal',
                        'caso_contexto': (
                            'Escenario / Caso: Durante la caída de los servicios surgen rumores en redes sociales '
                            'asegurando que la empresa quebró, y los ejecutivos no tienen designados voceros ni canales oficiales de comunicación. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 8.4.3 de ISO 22301 requiere establecer protocolos de '
                            'comunicación y advertencia estructurados para emitir información veraz a clientes, medios, empleados y reguladores.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Heraldo de Comunicación de Crisis y Notificación',
                                'concepto': 'Cláusula 8.4.3 Comunicación y Advertencia en Crisis',
                                'descripcion': 'Emite boletines oficiales autorizados y coordina las declaraciones a medios y partes interesadas.',
                                'es_correcta': True,
                                'fuerza': 91,
                                'defensa': 92,
                            },
                            {
                                'nombre': 'Caballero del Termistor',
                                'concepto': 'Resistencia Sensible a la Temperatura',
                                'descripcion': 'Mide grados Celsius en circuitos sin redactar comunicados de prensa ni gestionar crisis.',
                                'es_correcta': False,
                                'fuerza': 52,
                                'defensa': 50,
                            },
                            {
                                'nombre': 'Oráculo del Puente de Diodos',
                                'concepto': 'Rectificador de Corriente de Onda Completa',
                                'descripcion': 'Convierte corriente alterna sin emitir notificaciones a partes interesadas.',
                                'es_correcta': False,
                                'fuerza': 60,
                                'defensa': 56,
                            },
                            {
                                'nombre': 'Minotauro de la Bobina de Choque',
                                'concepto': 'Inductor de Filtro de Radiofrecuencia',
                                'descripcion': 'Filtra señales de alta frecuencia sin designar voceros oficiales de emergencia.',
                                'es_correcta': False,
                                'fuerza': 55,
                                'defensa': 53,
                            },
                        ],
                    },
                ],
            },
            {
                'numero_nivel': 4,
                'titulo': 'Pruebas, Simulacros y Gestión de Crisis',
                'tipo': 'normal',
                'dificultad': 'dificil',
                'recompensa_oro': 180,
                'recompensa_gemas': 36,
                'recompensa_xp': 360,
                'fases': [
                    {
                        'numero_fase': 1,
                        'titulo_incidente': 'Caso de Uso 1: Simulacros Integrales y Pruebas Operativas de Crisis',
                        'amenaza': 'Inoperancia de los Planes por Falta de Ejercitación Práctica',
                        'dificultad': 'dificil',
                        'caso_contexto': (
                            'Escenario / Caso: Los planes de continuidad existen en carpetas archivadas desde hace tres años, '
                            'pero jamás se ha realizado un simulacro para comprobar si los empleados saben qué hacer bajo presión. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 8.5 de ISO 22301 exige ejercitar y probar los planes de '
                            'continuidad a intervalos planificados y después de cambios significativos para asegurar su eficacia.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Director de Simulacros y Pruebas Operativas de Crisis',
                                'concepto': 'Cláusula 8.5 Ejercicio y Prueba de Planes',
                                'descripcion': 'Organiza simulaciones realistas para poner a prueba los procedimientos e identificar debilidades.',
                                'es_correcta': True,
                                'fuerza': 93,
                                'defensa': 94,
                            },
                            {
                                'nombre': 'Centinela de la Cinta Aislante',
                                'concepto': 'Material Aislante de Electricidad',
                                'descripcion': 'Aísla cables expuestos sin coordinar simulacros de crisis corporativa.',
                                'es_correcta': False,
                                'fuerza': 51,
                                'defensa': 49,
                            },
                            {
                                'nombre': 'Titán del Oscilador LC',
                                'concepto': 'Circuito Resonante de Bobina y Condensador',
                                'descripcion': 'Genera ondas electromagnéticas sin evaluar tiempos de respuesta humana.',
                                'es_correcta': False,
                                'fuerza': 62,
                                'defensa': 58,
                            },
                            {
                                'nombre': 'Cazador del Transistor PNP',
                                'concepto': 'Semiconductor Bipolar',
                                'descripcion': 'Conmuta polaridades de voltaje sin intervenir en ensayos de continuidad.',
                                'es_correcta': False,
                                'fuerza': 57,
                                'defensa': 54,
                            },
                        ],
                    },
                    {
                        'numero_fase': 2,
                        'titulo_incidente': 'Caso de Uso 2: Continuidad del Negocio e Impacto Operativo',
                        'amenaza': 'Interrupción Crítica Prolongada y Daño Financiero Insalvable',
                        'dificultad': 'dificil',
                        'caso_contexto': (
                            'Escenario / Caso: La dirección de la empresa necesita definir cuánto tiempo puede estar fuera '
                            'de servicio el núcleo del sistema transaccional antes de que la interrupción cause un daño financiero e insalvable '
                            'a la organización. ¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La norma ISO 22301 establece dentro del Análisis de Impacto en el Negocio '
                            '(BIA, Cláusula 8.2) la necesidad de calcular el MTPD (Maximum Tolerable Period of Disruption) para determinar '
                            'los límites temporales de recuperación tolerables antes del colapso.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Buscador del MTPD (Máximo Tiempo Tolerable de Interrupción)',
                                'concepto': 'Cláusula 8.2 Análisis BIA - MTPD',
                                'descripcion': 'Determina el umbral temporal máximo que la empresa puede soportar antes del daño irreparable.',
                                'es_correcta': True,
                                'fuerza': 95,
                                'defensa': 96,
                            },
                            {
                                'nombre': 'Cronómetro del RTO y RPO',
                                'concepto': 'Cláusula 8.2 Métricas de Recuperación Temporal y de Datos',
                                'descripcion': 'Mide tiempos objetivo de restauración pero depende previamente del cálculo del MTPD.',
                                'es_correcta': False,
                                'fuerza': 75,
                                'defensa': 72,
                            },
                            {
                                'nombre': 'Comandante del Equipo de Respuesta a Incidentes (ERT)',
                                'concepto': 'Estructura Operativa de Respuesta Táctica',
                                'descripcion': 'Atiende incidentes en tiempo real sin calcular el umbral macroeconómico del negocio.',
                                'es_correcta': False,
                                'fuerza': 70,
                                'defensa': 68,
                            },
                            {
                                'nombre': 'Centinela de Amenazas Disruptivas',
                                'concepto': 'Evaluación de Riesgos Operativos',
                                'descripcion': 'Monitorea peligros externos pero no define los límites de tolerancia financiera de la dirección.',
                                'es_correcta': False,
                                'fuerza': 68,
                                'defensa': 65,
                            },
                        ],
                    },
                    {
                        'numero_fase': 3,
                        'titulo_incidente': 'Caso de Uso 3: Pruebas de Respaldo y Restauración en Entornos Aislados',
                        'amenaza': 'Inconsistencia de Respaldos e Imposibilidad de Restaurar en Crisis',
                        'dificultad': 'dificil',
                        'caso_contexto': (
                            'Escenario / Caso: Las copias de respaldo se ejecutan cada medianoche sin errores aparentes, '
                            'pero jamás se ha realizado una prueba para restaurarlas en un servidor aislado y verificar la integridad de las tablas. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 8.5 de ISO 22301 exige verificar que las medidas técnicas '
                            'de contingencia, incluidos los respaldos, sean plenamente funcionales y restaurables ante un siniestro real.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Verificador de Pruebas de Restauración e Integridad de Respaldos',
                                'concepto': 'Cláusula 8.5 Verificación de Capacidades Técnicas',
                                'descripcion': 'Restaura copias en entornos aislados y certifica la consistencia total de las bases de datos.',
                                'es_correcta': True,
                                'fuerza': 93,
                                'defensa': 94,
                            },
                            {
                                'nombre': 'Minotauro del Cable Coaxial Fino',
                                'concepto': 'Cable de Red 10Base2',
                                'descripcion': 'Conecta terminales en serie sin comprobar la validez de los backups en la nube.',
                                'es_correcta': False,
                                'fuerza': 52,
                                'defensa': 49,
                            },
                            {
                                'nombre': 'Vigía del Zócalo SIMM',
                                'concepto': 'Módulo de Memoria de 30 Contactos',
                                'descripcion': 'Aloja módulos de memoria física sin capacidad de restauración de bases de datos.',
                                'es_correcta': False,
                                'fuerza': 56,
                                'defensa': 53,
                            },
                            {
                                'nombre': 'Espectro del Búfer UART',
                                'concepto': 'Controlador Asíncrono de Puertos Serie',
                                'descripcion': 'Sincroniza bytes de módem sin intervenir en pruebas periciales de copias de seguridad.',
                                'es_correcta': False,
                                'fuerza': 59,
                                'defensa': 56,
                            },
                        ],
                    },
                ],
            },
            {
                'numero_nivel': 5,
                'titulo': 'Auditoría Crítica de Resiliencia y Continuidad (Jefe)',
                'tipo': 'jefe',
                'dificultad': 'dificil',
                'recompensa_oro': 320,
                'recompensa_gemas': 80,
                'recompensa_xp': 640,
                'fases': [
                    {
                        'numero_fase': 1,
                        'titulo_incidente': 'Caso de Uso 1: Verificación de Tiempos Reales de Recuperación vs MTPD',
                        'amenaza': 'Tiempos de Recuperación Excesivos que Superan el Límite de Quiebra',
                        'dificultad': 'dificil',
                        'caso_contexto': (
                            'Escenario / Caso: En la auditoría final se demuestra que el tiempo real de restauración '
                            'tarda 48 horas cuando el MTPD aprobado por la junta directiva establecía un límite improrrogable de 12 horas. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 9.1 de ISO 22301 exige realizar seguimiento, medición '
                            'y análisis para asegurar que los tiempos reales de recuperación no excedan el MTPD y se alineen con los RTO pactados.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Gran Juez de Resiliencia y Métricas de Tolerancia',
                                'concepto': 'Cláusula 9.1 Seguimiento y Medición de la Continuidad',
                                'descripcion': 'Compara los tiempos de respuesta empíricos frente al MTPD y exige el rediseño de las arquitecturas deficientes.',
                                'es_correcta': True,
                                'fuerza': 96,
                                'defensa': 97,
                            },
                            {
                                'nombre': 'Caballero del Transformador Toroidal',
                                'concepto': 'Transformador en Forma de Rosquilla',
                                'descripcion': 'Reduce pérdidas magnéticas de energía sin analizar métricas de tiempo de recuperación BIA.',
                                'es_correcta': False,
                                'fuerza': 60,
                                'defensa': 57,
                            },
                            {
                                'nombre': 'Centinela del Termostato Bimetálico',
                                'concepto': 'Interruptor por Dilatación Térmica',
                                'descripcion': 'Desconecta fuentes por sobrecalentamiento sin evaluar tiempos de contingencia empresarial.',
                                'es_correcta': False,
                                'fuerza': 54,
                                'defensa': 51,
                            },
                            {
                                'nombre': 'Cazador del Filtro de Relleno',
                                'concepto': 'Circuito de Atenuación de Ruidos',
                                'descripcion': 'Atenúa señales espurias en líneas de alimentación sin impacto en métricas de auditoría.',
                                'es_correcta': False,
                                'fuerza': 58,
                                'defensa': 55,
                            },
                        ],
                    },
                    {
                        'numero_fase': 2,
                        'titulo_incidente': 'Caso de Uso 2: Auditoría y Actualización Periódica de Planes BCP y DRP',
                        'amenaza': 'Planes Obsoletos que No Contemplan Nuevas Tecnologías ni Cambios de Negocio',
                        'dificultad': 'dificil',
                        'caso_contexto': (
                            'Escenario / Caso: Los procesos de la empresa migraron por completo a una nueva arquitectura '
                            'pero los planes de continuidad continúan describiendo servidores físicos dados de baja hace dos años. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: La Cláusula 9.2 de ISO 22301 exige realizar auditorías internas '
                            'para comprobar que el SGCN permanece actualizado, cumple los requisitos de la norma y refleja los cambios de la organización.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Inquisidor de Vigencia y Actualización de Planes BCP/DRP',
                                'concepto': 'Cláusula 9.2 Auditoría Interna del SGCN',
                                'descripcion': 'Audita la vigencia de los planes y exige su actualización inmediata ante cualquier cambio organizativo.',
                                'es_correcta': True,
                                'fuerza': 95,
                                'defensa': 96,
                            },
                            {
                                'nombre': 'Minotauro del Búfer de Impresión Matricial',
                                'concepto': 'Memoria Intermedia de Spooling',
                                'descripcion': 'Retiene hojas de cálculo impresas sin auditar procedimientos de resiliencia.',
                                'es_correcta': False,
                                'fuerza': 51,
                                'defensa': 48,
                            },
                            {
                                'nombre': 'Titán del Reóstato',
                                'concepto': 'Resistencia Ajustable de Potencia',
                                'descripcion': 'Controla intensidad de corriente sin verificar vigencia de planes de crisis.',
                                'es_correcta': False,
                                'fuerza': 59,
                                'defensa': 56,
                            },
                            {
                                'nombre': 'Oráculo del Sensor Óptico',
                                'concepto': 'Fotodiodo de Detección de Luz',
                                'descripcion': 'Detecta presencia de objetos sin examinar la idoneidad de los procedimientos DRP.',
                                'es_correcta': False,
                                'fuerza': 55,
                                'defensa': 52,
                            },
                        ],
                    },
                    {
                        'numero_fase': 3,
                        'titulo_incidente': 'Caso de Uso 3: Mejora Continua y Aprendizaje post-Incidente',
                        'amenaza': 'Repetición de Fallas Críticas por Desidia en Incorporar Lecciones Aprendidas',
                        'dificultad': 'dificil',
                        'caso_contexto': (
                            'Escenario / Caso: La compañía superó un incidente de interrupción mayor pero no se redactó '
                            'un informe de lecciones aprendidas ni se ajustaron los procedimientos para evitar que el mismo error vuelva a suceder. '
                            '¿A qué entidad mitológica debes recurrir para este análisis?\n\n'
                            'Explicación breve: Las Cláusulas 10.1 y 10.2 de ISO 22301 estipulan la mejora continua '
                            'del Sistema de Gestión de Continuidad del Negocio mediante la adopción formal de lecciones aprendidas y acciones correctivas.'
                        ),
                        'opciones': [
                            {
                                'nombre': 'Archimago de la Mejora Continua y Resiliencia Organizacional',
                                'concepto': 'Cláusulas 10.1 y 10.2 Acciones Correctivas y Mejora Continua',
                                'descripcion': 'Consolida lecciones aprendidas, subsana debilidades detectadas y blinda la organización ante el futuro.',
                                'es_correcta': True,
                                'fuerza': 97,
                                'defensa': 98,
                            },
                            {
                                'nombre': 'Vigía de la Llave de Palanca',
                                'concepto': 'Interruptor Mecánico Basculante',
                                'descripcion': 'Abre circuitos con palanca manual sin registrar lecciones aprendidas.',
                                'es_correcta': False,
                                'fuerza': 52,
                                'defensa': 50,
                            },
                            {
                                'nombre': 'Espectro del Puente Rectificador',
                                'concepto': 'Arreglo de 4 Diodos de Potencia',
                                'descripcion': 'Convierte polaridades eléctricas sin capacidad pedagógica de resiliencia.',
                                'es_correcta': False,
                                'fuerza': 60,
                                'defensa': 58,
                            },
                            {
                                'nombre': 'Cíclope del Condensador de Tantalio',
                                'concepto': 'Capacitor Electrolítico Polarizado',
                                'descripcion': 'Filtra frecuencias parásitas en placas de circuitos sin gobernar la mejora continua del negocio.',
                                'es_correcta': False,
                                'fuerza': 57,
                                'defensa': 55,
                            },
                        ],
                    },
                ],
            },
        ],
    },
]
