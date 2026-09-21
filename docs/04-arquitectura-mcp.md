# 4. Arquitectura de MCP

## Modelo host / cliente / servidor

MCP define tres roles:

- **Host**: el proceso de la aplicación que contiene y coordina todo. Crea y administra las instancias de cliente, controla los permisos de conexión, hace cumplir las políticas de seguridad y gestiona el consentimiento del usuario, y coordina la integración con el modelo de lenguaje. **En nuestro caso, Claude Code es el host.**
- **Cliente**: vive dentro del host y se comunica con **exactamente un** servidor (relación 1:1). Adjunta la versión del protocolo y sus capacidades a cada petición, enruta los mensajes y mantiene el límite de seguridad entre servidores distintos. **En nuestro caso, el cliente MCP integrado en Claude Code** es quien habla con el servidor de sistema de archivos.
- **Servidor**: expone capacidades específicas (herramientas, recursos, prompts) y opera de forma independiente, enfocado en una responsabilidad concreta. No puede ver el resto de la conversación ni "asomarse" a otros servidores conectados al mismo host. **En nuestro caso, el servidor `@modelcontextprotocol/server-filesystem`**, delimitado a un directorio de trabajo específico.

Un mismo host puede administrar varios clientes simultáneamente, cada uno hablando con un servidor distinto (por ejemplo: un servidor de archivos y, en paralelo, nuestro servidor propio del punto opcional).

## Primitivas del lado del servidor

Un servidor MCP puede exponer tres tipos de primitivas:

- **Tools (herramientas)**: funciones invocables con efectos (leer, escribir, buscar, llamar a una API externa). Son la primitiva que el modelo decide invocar según la petición del usuario.
- **Resources (recursos)**: datos que el servidor pone a disposición del cliente (el contenido de un archivo, una fila de base de datos, resultado de una consulta) para que se usen como contexto, sin que eso implique necesariamente "ejecutar una acción".
- **Prompts (plantillas de prompt)**: plantillas de instrucciones reutilizables y parametrizables que el servidor ofrece, para estandarizar flujos comunes de interacción con el modelo.

Es un error frecuente mencionar solo las *tools* y omitir *resources* y *prompts* — las tres son primitivas de primera clase del protocolo, aunque en la práctica (como en el servidor de sistema de archivos) las herramientas suelen ser la primitiva más usada.

## Primitivas del lado del cliente

El cliente también expone primitivas que los servidores pueden invocar cuando necesitan algo del usuario o del entorno:

- **Roots**: forma en que el cliente comunica al servidor qué directorios o archivos son relevantes para la sesión actual (por ejemplo, la carpeta del proyecto abierto). Es información orientativa, no un mecanismo de control de acceso en sí mismo. *Nota de actualidad*: en la versión `2026-07-28` de la especificación, **Roots quedó marcado como obsoleto** (deprecado) en favor de pasar directorios o archivos explícitamente como parámetros de herramienta, URIs de recurso o configuración del servidor (Model Context Protocol) — aunque sigue vigente en la especificación durante un período de transición y muchos servidores desplegados hoy, incluido el de sistema de archivos, siguen soportándolo.
- **Elicitation**: mecanismo estandarizado para que un servidor pida información adicional al usuario **a través del cliente**, ya sea con un formulario estructurado validado por un esquema JSON (modo *form*) o redirigiendo a una URL externa para interacciones sensibles como flujos de autenticación (modo *url*) (Model Context Protocol). Esto es lo que en la práctica se traduce, por ejemplo, en la confirmación humana antes de que un servidor ejecute una operación sensible.

## Transportes

MCP separa claramente el **significado** de los mensajes (definido por el protocolo, igual en todos los transportes) de **cómo se entregan** (definido por el "binding" de transporte) (Model Context Protocol, s.f.-e):

- **stdio**: para servidores locales que corren como **proceso hijo** del cliente. Los mensajes JSON-RPC se transmiten delimitados por saltos de línea sobre la entrada/salida estándar (`stdin`/`stdout`) de ese subproceso. Es el transporte que usamos en esta tarea: Claude Code lanza `npx @modelcontextprotocol/server-filesystem ...` como subproceso local.
- **Streamable HTTP**: para servidores remotos. Cada mensaje del cliente es un `POST` HTTP a un único endpoint MCP; la respuesta llega como un objeto JSON o, si la operación es de larga duración o produce varios eventos, como un flujo `Server-Sent Events (SSE)` asociado a esa petición.

En todos los casos, el formato de los mensajes es **JSON-RPC 2.0**: el servidor nunca inicia una petición JSON-RPC hacia el cliente por su cuenta ni el cliente envía respuestas JSON-RPC sin que exista una petición previa — la dirección de los mensajes está estrictamente definida por el protocolo.

