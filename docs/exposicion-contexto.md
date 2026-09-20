# Contexto para preparar la exposición (no son las diapositivas)

Este documento **no** es el material de la presentación. Es el contexto que resume la investigación y la implementación, pensado para pegarlo en otra herramienta de IA (o usarlo como guion propio) y generar ahí las diapositivas. La exposición dura 5–7 minutos por persona, con diapositivas de apoyo que **no se leen textualmente**, e incluye una demo en vivo (con video de respaldo de máx. 2 minutos por si falla el equipo o la conexión).

## Estructura sugerida (5–7 min)

1. **Gancho inicial (30 s)** — De "copiar y pegar en un navegador" a un modelo que lee y modifica archivos locales. Plantear la pregunta que resuelve la exposición: ¿qué cambió técnicamente para que eso sea posible?
2. **El problema del aislamiento (1 min)** — Un LLM es texto-entra/texto-sale; no tiene syscalls. Aislamiento por arquitectura (modelo remoto) + aislamiento por seguridad (consentimiento, riesgo de inyección). Ver `docs/02-aislamiento.md`.
3. **MCP frente a una API — el núcleo (2 min)** — Mostrar la tabla comparativa de `docs/03-mcp-vs-api.md`. Idea central a transmitir con palabras propias: en una API, la persona decide de antemano qué se llama; en MCP, el servidor publica un catálogo descubrible y **el modelo decide en tiempo de ejecución** qué herramienta usar según lo que pidió el usuario. Enfatizar: **MCP no sustituye a las APIs, las envuelve**.
4. **Arquitectura (1 min)** — Host/cliente/servidor mapeado al ejemplo real: Claude Code = host + cliente; `@modelcontextprotocol/server-filesystem` = servidor. Mencionar brevemente tools/resources/prompts (servidor) y roots/elicitation (cliente), y los dos transportes (stdio local vs. Streamable HTTP remoto). Citar la versión de la especificación consultada: `2026-07-28`.
5. **Demo en vivo (1.5–2 min)** — Ver guion de demo abajo.
6. **Seguridad (30–45 s)** — Prompt injection, path traversal, escritura no deseada → mitigado con alcance a un directorio + confirmación humana. Mostrar/mencionar la prueba del límite de seguridad (intento de acceso fuera del directorio, rechazado).
7. **Cierre (15–20 s)** — Una frase propia sobre cómo esta combinación cambia la forma de desarrollar software: el modelo deja de ser un oráculo de texto y pasa a ser un agente que opera sobre el entorno real, bajo límites explícitos.

## Guion de la demo en vivo

Ejecutar, en este orden, sobre el directorio `workspace-demo/` con el servidor filesystem ya conectado en Claude Code:

1. Listar el contenido del directorio autorizado.
2. Leer un archivo existente y mostrar su contenido.
3. Crear un archivo nuevo con contenido.
4. Modificar ese archivo (o uno existente).
5. Buscar un archivo por nombre o contenido.
6. **Cierre de la demo**: pedir acceso a un archivo fuera de `workspace-demo/` (por ejemplo, algo en `/home/.../Desktop/Moviles/`) y mostrar en vivo el rechazo — es el momento de mayor impacto de la demo porque hace tangible el límite de seguridad explicado en la diapositiva anterior.

Si algo falla en vivo, cortar a un video de respaldo pregrabado (máximo 2 minutos) que muestre exactamente esos mismos 6 pasos.

## Respuestas preparadas a las dos preguntas obligatorias

**1. ¿En qué se diferencia MCP de consumir una API?**
Al consumir una API tradicional, la persona desarrolladora ya decidió, en el código, qué endpoint se llama y cuándo — el programa solo ejecuta esa decisión fija. Con MCP, el servidor publica un catálogo de herramientas descubrible en tiempo de ejecución (nombre, descripción, esquema de parámetros), y es el modelo quien decide, a partir de lo que pide el usuario en lenguaje natural, cuál herramienta invocar y con qué argumentos, en ese momento. MCP no es una API distinta ni mejor: es una capa de descubribilidad sobre APIs/recursos ya existentes, que resuelve el problema de acoplamiento (cada API requiere su propio código de integración) usando un protocolo común (JSON-RPC 2.0) que cualquier cliente MCP puede hablar con cualquier servidor MCP.

**2. ¿Qué es exactamente lo que habilita el servidor de sistema de archivos?**
No habilita "acceso a archivos" en abstracto — habilita un **catálogo concreto y acotado de operaciones** (listar, leer, escribir, crear, mover, buscar) sobre uno o más **directorios explícitamente permitidos**, que se configuran al arrancar el servidor (por argumentos o vía el protocolo de Roots). El modelo nunca toca el disco directamente: invoca una herramienta del servidor, el servidor valida que la ruta solicitada esté dentro del alcance permitido, y solo entonces ejecuta la operación real del sistema operativo. Fuera de ese alcance, toda operación se rechaza — eso es lo que se demuestra en la prueba del límite de seguridad.
