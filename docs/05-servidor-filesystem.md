# 5. El servidor de sistema de archivos

## "FS" no es parte del protocolo

Es importante aclararlo de forma explícita porque es uno de los errores conceptuales más comunes en este tema: **"FS" (filesystem) no es una primitiva ni una parte de la especificación de MCP**. MCP define el protocolo genérico (JSON-RPC 2.0, arquitectura host/cliente/servidor, primitivas de tools/resources/prompts, transportes). El servidor de sistema de archivos es, simplemente, **uno de los servidores de referencia** publicados por el equipo de Model Context Protocol (`@modelcontextprotocol/server-filesystem`), entre una gran cantidad de servidores posibles — de bases de datos, de control de versiones, de APIs de terceros, etc. Cualquier persona puede implementar un servidor MCP para cualquier recurso; el de sistema de archivos es solo uno de los primeros y más usados como ejemplo didáctico.

## Herramientas que expone

Según la implementación de referencia oficial (`modelcontextprotocol/servers`, carpeta `src/filesystem`), el servidor expone, entre otras, las siguientes herramientas:

| Herramienta | Qué hace |
|---|---|
| `list_directory` / `list_directory_with_sizes` | Lista el contenido de un directorio (con o sin tamaños de archivo). |
| `directory_tree` | Devuelve la estructura de un directorio de forma recursiva. |
| `read_text_file` / `read_media_file` / `read_multiple_files` | Lee el contenido de uno o varios archivos (texto o binarios/multimedia). |
| `write_file` | Crea un archivo nuevo o sobrescribe uno existente con contenido dado. |
| `edit_file` | Modifica un archivo existente aplicando cambios puntuales. |
| `create_directory` | Crea un directorio nuevo. |
| `move_file` | Mueve o renombra un archivo. |
| `search_files` | Busca archivos por nombre/patrón dentro del alcance permitido. |
| `get_file_info` | Devuelve metadatos de un archivo (tamaño, fechas, permisos). |
| `list_allowed_directories` | Devuelve el listado de directorios a los que el servidor tiene permitido operar. |

(Modelcontextprotocol/servers, s.f.)

## Cómo se delimita el alcance: directorios permitidos

El servidor **exige** que se le indique, al arrancar, al menos un directorio permitido — no puede correr sin ninguno. Esto se hace de dos formas:

1. **Argumentos de línea de comandos**, al lanzar el proceso:
   ```bash
   npx -y @modelcontextprotocol/server-filesystem /ruta/al/directorio-permitido
   ```
2. **El protocolo de Roots** (ver [04-arquitectura-mcp.md](04-arquitectura-mcp.md)): un cliente que soporte Roots puede actualizar dinámicamente los directorios permitidos, en tiempo de ejecución, sin reiniciar el servidor.

Todas las operaciones de las herramientas listadas arriba se validan contra esa lista de directorios permitidos antes de ejecutarse: si una ruta solicitada (incluso a través de enlaces simbólicos o rutas relativas con `..`) resuelve fuera de esos directorios, la operación se rechaza.

## Por qué existe ese límite y qué pasaría sin él

El límite existe porque el modelo, al decidir qué herramienta invocar y con qué argumentos, **puede equivocarse o ser manipulado** (ver [06-seguridad.md](06-seguridad.md)). Sin un límite explícito de directorios:

- Una instrucción ambigua, un error del modelo, o contenido malicioso dentro de un archivo leído previamente (inyección de instrucciones) podría hacer que el servidor intente leer, sobrescribir o borrar archivos fuera del proyecto en el que se está trabajando — por ejemplo, archivos de configuración del sistema, credenciales guardadas en el directorio *home*, o cualquier otro archivo al que el proceso del sistema operativo tuviera acceso.
- El "radio de explosión" (*blast radius*) de un error sería tan amplio como los permisos del usuario del sistema operativo que ejecuta el servidor — potencialmente toda la cuenta de usuario.

Al restringir el servidor a un directorio de trabajo específico (en esta tarea, `workspace-demo/`), cualquier error de razonamiento del modelo, o cualquier intento de manipulación vía contenido de archivos, queda contenido dentro de ese directorio: el mecanismo de validación de rutas del propio servidor rechaza cualquier operación que intente salir de él, independientemente de lo que el modelo "quiera" hacer (ver la prueba de límite de seguridad documentada en el README).

## Referencias de este documento

- Modelcontextprotocol/servers. (s.f.). *Filesystem MCP Server* [Repositorio de código]. GitHub. https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem
