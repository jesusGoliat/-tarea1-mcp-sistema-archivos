# Tarea 1 — MCP y sistema de archivos: investigación e implementación

## Datos de identificación

- **Nombre completo:** [NOMBRE COMPLETO]
- **Número de boleta:** [BOLETA]
- **Grupo:** [GRUPO]

## Resumen de la actividad

Esta tarea investiga cómo un modelo de lenguaje pasa de estar aislado (solo texto de entrada/salida) a poder operar sobre archivos locales mediante el **Model Context Protocol (MCP)**, distinguiéndolo con precisión de una API tradicional. La parte práctica implementa, verifica y documenta la instalación de un **servidor MCP de sistema de archivos** delimitado a un directorio de trabajo específico, usando **Claude Code** como cliente/host. Adicionalmente (parte opcional) se implementó un **servidor MCP propio** con dos herramientas, usando el SDK oficial de Python.

## Índice de `docs/`

| Documento | Contenido |
|---|---|
| [`docs/01-evolucion-modelos.md`](docs/01-evolucion-modelos.md) | De modelo de lenguaje (LM) a LLM; modelos con razonamiento explícito y por qué no emerge solo de la escala. |
| [`docs/02-aislamiento.md`](docs/02-aislamiento.md) | Por qué un LLM no puede ver ni modificar archivos por sí mismo: razones de arquitectura vs. de seguridad. |
| [`docs/03-mcp-vs-api.md`](docs/03-mcp-vs-api.md) | **Punto central**: qué es una API, qué es MCP, tabla comparativa, y por qué MCP no sustituye a las APIs. |
| [`docs/04-arquitectura-mcp.md`](docs/04-arquitectura-mcp.md) | Modelo host/cliente/servidor, primitivas (tools/resources/prompts, roots/elicitation), transportes (stdio/Streamable HTTP), versión de la especificación. |
| [`docs/05-servidor-filesystem.md`](docs/05-servidor-filesystem.md) | El servidor de sistema de archivos como servidor de referencia (no parte del protocolo), sus herramientas y el alcance por directorios permitidos. |
| [`docs/06-seguridad.md`](docs/06-seguridad.md) | Riesgos (inyección de instrucciones, path traversal, escritura no deseada) y mitigaciones. |
| [`docs/07-casos-de-uso.md`](docs/07-casos-de-uso.md) | Tres herramientas reales que implementan MCP (Claude Code, Cursor, Google Antigravity) y cómo editan repos completos. |
| [`docs/exposicion-contexto.md`](docs/exposicion-contexto.md) | Contexto/guion para preparar la exposición y sus diapositivas (no es la presentación en sí). |

## Tabla comparativa: MCP vs. API

(Versión resumida; la tabla completa con más contexto está en [`docs/03-mcp-vs-api.md`](docs/03-mcp-vs-api.md).)

| Dimensión | API tradicional | MCP |
|---|---|---|
| Quién decide qué se invoca | La persona desarrolladora, en el código, de antemano | El modelo, en tiempo de ejecución, según la petición del usuario |
| Cómo se descubren las capacidades | Leyendo documentación externa antes de programar | El cliente descubre el catálogo de herramientas en tiempo de ejecución |
| Acoplamiento cliente–servicio | Alto: el código depende de esa API específica | Bajo: cualquier cliente MCP habla con cualquier servidor MCP |
| Formato de los mensajes | Varía (REST/JSON, XML, gRPC, GraphQL...) | Estandarizado: JSON-RPC 2.0 |
| Autenticación y consentimiento | Definida por cada proveedor | Contemplada en el protocolo (OAuth remoto, *elicitation* para consentimiento) |
| Reutilización entre aplicaciones | Baja: cada app reimplementa su integración | Alta: un mismo servidor MCP sirve a múltiples clientes sin cambios |

**MCP no sustituye a las APIs**: un servidor MCP casi siempre envuelve una API o recurso existente (en este caso, el propio sistema de archivos), agregando una capa que lo hace descubrible e invocable por un modelo.

## Elección del cliente

Se eligió **Claude Code** como cliente/host MCP porque:

- Soporta MCP de forma nativa a través del archivo de configuración `.mcp.json` en la raíz del proyecto, sin instalación adicional de un cliente separado.
- Permite ejecutar, documentar y versionar todo el flujo de instalación y demostración dentro de la misma sesión de trabajo usada para el resto de la tarea.
- Es el mismo tipo de herramienta (agente de desarrollo con acceso a MCP) que se describe en el punto 7 de la investigación (`docs/07-casos-de-uso.md`), lo que permite conectar teoría y práctica sobre el mismo ejemplo.

## Instalación paso a paso (reproducible en máquina limpia)

**Sistema operativo usado:** Linux (Ubuntu, kernel 6.17).
**Versiones usadas:** Node.js v24.18.0 / npm 11, Python 3.12.3, git (la instalada por el SO).

1. Instalar Node.js (v18+) y tener `npx` disponible (`node --version`, `npx --version`).
2. Clonar este repositorio y ubicarse en su raíz.
3. Verificar que existe el directorio delimitado `workspace-demo/` (ya incluido en el repo con archivos de ejemplo).
4. Revisar el archivo `.mcp.json` en la raíz del proyecto (idéntico al que está en `config/mcp.json`, sin credenciales):

   ```json
   {
     "mcpServers": {
       "filesystem-tarea1": {
         "command": "npx",
         "args": [
           "-y",
           "@modelcontextprotocol/server-filesystem",
           "/ruta/absoluta/al/repo/workspace-demo"
         ]
       },
       "servidor-propio": {
         "command": "/ruta/a/tu/venv/bin/python",
         "args": ["/ruta/absoluta/al/repo/servidor-propio/server.py"]
       }
     }
   }
   ```

   Ajustar las rutas absolutas a donde se haya clonado el repositorio en tu máquina.
5. Abrir Claude Code en la raíz del proyecto. Al detectar `.mcp.json`, pedirá aprobar la conexión a los servidores MCP definidos — aprobar `filesystem-tarea1` (y `servidor-propio` si se probará el bonus).
6. Verificar que el cliente reconoce el servidor: ejecutar `/mcp` dentro de Claude Code y confirmar que aparecen `filesystem-tarea1` con sus herramientas (`list_directory`, `read_text_file`, `write_file`, `edit_file`, `search_files`, `move_file`, etc.) — ver evidencia en `img/`.
7. (Opcional, bonus) Para el servidor propio: `cd servidor-propio && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`, y confirmar que `contar_texto` y `convertir_temperatura` aparecen listadas en `/mcp`.

## Evidencias

Todas las operaciones se ejecutaron realmente (no simuladas) dentro de una sesión de Claude Code conectada a `filesystem-tarea1` y `servidor-propio`. Capturas de pantalla en `img/` (nomenclatura sugerida, tomadas de esa sesión):

- `img/01-listar-directorio.png` — `list_directory` sobre `workspace-demo/` (devuelve `notas.txt`, `tareas-pendientes.txt`).
- `img/02-leer-archivo.png` — `read_text_file` de `workspace-demo/notas.txt`.
- `img/03-crear-archivo.png` — `write_file` crea `workspace-demo/creado-por-mcp.txt`.
- `img/04-modificar-archivo.png` — `edit_file` agrega una línea a `workspace-demo/tareas-pendientes.txt` (diff mostrado por la propia herramienta).
- `img/05-buscar-archivo.png` — `search_files` con patrón `*pendientes*` encuentra `tareas-pendientes.txt`.
- `img/06-limite-seguridad.png` — intento de `list_directory` sobre `/home/jesus/Desktop/Moviles` (fuera del proyecto), rechazado.

### Nota: el directorio autorizado real terminó siendo todo el proyecto, no solo `workspace-demo/`

Al conectar el servidor, `list_allowed_directories` reportó como único directorio permitido la carpeta completa del proyecto (`.../Tarea1`), y no `workspace-demo/` como se había configurado por argumento de arranque. La causa (documentada con más detalle en [`docs/05-servidor-filesystem.md`](docs/05-servidor-filesystem.md)) es que Claude Code, como cliente MCP, implementa el protocolo de **Roots** y comparte automáticamente la raíz del proyecto abierto con el servidor — y, según la documentación oficial del servidor, esa notificación de Roots **reemplaza por completo** el directorio pasado por argumento, no lo restringe. Se confirmó en vivo: leer `README.md` (dentro de `Tarea1`, fuera de `workspace-demo/`) funcionó sin problema. El directorio del proyecto sigue siendo una carpeta específica creada para esta tarea —nunca la raíz del disco ni la carpeta de usuario completa—, así que el requisito de delimitar el alcance se sigue cumpliendo, solo que a nivel de todo el proyecto en lugar de únicamente `workspace-demo/`.

### Prueba del límite de seguridad

Se solicitó al modelo, a través de Claude Code, listar el contenido de `/home/jesus/Desktop/Moviles` — el directorio **padre** del proyecto, fuera del alcance real autorizado. El servidor `filesystem-tarea1` rechazó la operación con el error `Access denied - path outside allowed directories: /home/jesus/Desktop/Moviles not in /home/jesus/Desktop/Moviles/Tarea1`, porque valida cada ruta solicitada contra la lista de directorios permitidos (en este caso, la raíz del proyecto notificada vía Roots); cualquier ruta que resuelva fuera de esa lista —incluyendo intentos con `..` o enlaces simbólicos— se rechaza antes de tocar el sistema de archivos real. El mecanismo que impidió la operación es, por lo tanto, la validación de rutas del propio servidor MCP, no un permiso del sistema operativo ni una regla de Claude Code. Ver captura en `img/06-limite-seguridad.png` y detalle técnico en [`docs/05-servidor-filesystem.md`](docs/05-servidor-filesystem.md).

## Conclusiones personales

[Completar aquí con tus propias palabras: qué aprendiste sobre MCP vs. APIs, qué te sorprendió del límite de seguridad, y cómo ves que esto cambia la forma de desarrollar software. Esta sección es intencionalmente un placeholder — es la parte que no se puede delegar.]

## Referencias (APA)

- Model Context Protocol. (2026). *Specification* (Versión 2026-07-28, la versión consultada para esta tarea). https://modelcontextprotocol.io/specification/2026-07-28/
- Model Context Protocol. (s.f.). *Versioning*. https://modelcontextprotocol.io/specification/versioning
- Model Context Protocol. (s.f.). *Architecture*. https://modelcontextprotocol.io/specification/2026-07-28/architecture
- Model Context Protocol. (s.f.). *Transports*. https://modelcontextprotocol.io/specification/2026-07-28/basic/transports
- Model Context Protocol. (s.f.). *Roots*. https://modelcontextprotocol.io/specification/2026-07-28/client/roots
- Model Context Protocol. (s.f.). *Elicitation*. https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation
- Modelcontextprotocol/servers. (s.f.). *Filesystem MCP Server* [Repositorio de código]. GitHub. https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem
- Google Developers Blog. (s.f.). *Build with Google Antigravity, our new agentic development platform*. https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/
- Cursor. (s.f.). *Model Context Protocol*. https://cursor.com/docs/context/mcp
- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). *Attention is all you need*. Advances in Neural Information Processing Systems, 30.

## Estructura del repositorio

```text
README.md          Este documento
docs/               Investigación, en archivos .md
config/             Archivos de configuración MCP utilizados (sin credenciales)
img/                Capturas de pantalla de la demo
servidor-propio/    Servidor MCP propio (opcional, bonus)
workspace-demo/     Directorio de trabajo delimitado usado por el servidor filesystem
```
