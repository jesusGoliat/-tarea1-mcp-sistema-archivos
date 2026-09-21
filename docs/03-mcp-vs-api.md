# 3. MCP frente a una API (punto obligatorio)

## Qué es una API

Una **API** (*Application Programming Interface*) es un contrato entre dos programas. Alguien que desarrolla software lee la documentación de esa API (por ejemplo, la de una API REST de clima), decide de antemano **qué endpoint** necesita llamar (`GET /weather?city=CDMX`), arma la petición con los parámetros correctos, la envía, y escribe código específico que sabe interpretar la forma exacta de la respuesta (por ejemplo, un JSON con una clave `temperature`).


## Qué es MCP

El **Model Context Protocol (MCP)** es un protocolo abierto, basado en **JSON-RPC 2.0**, mediante el cual un **servidor** publica un catálogo de **herramientas** (además de recursos y plantillas de prompt) con su nombre, su descripción en lenguaje natural y el **esquema** (tipo, forma) de los parámetros que aceptan. Un **cliente** MCP —dentro de una aplicación *host*, como Claude Code— se conecta a ese servidor y **descubre ese catálogo en tiempo de ejecución**: no necesita conocer de antemano qué herramientas existen.

Todo el intercambio (descubrimiento del catálogo, invocación de herramientas, respuestas) viaja como mensajes JSON-RPC 2.0 (`request`/`response`/`notification`), sobre uno de los transportes definidos por el protocolo (ver [04-arquitectura-mcp.md](04-arquitectura-mcp.md)).

## Tabla comparativa

| Dimensión | API tradicional | MCP |
|---|---|---|
| **Quién decide qué se invoca** | La persona desarrolladora, en tiempo de diseño/código. La secuencia de llamadas está fija de antemano. | El modelo, en tiempo de ejecución, a partir de la petición del usuario y las descripciones de las herramientas disponibles. |
| **Cómo se descubren las capacidades** | Leyendo documentación externa (Swagger/OpenAPI, docs en un sitio web) antes de escribir el código. | El cliente consulta al servidor en tiempo de ejecución (ej. listado de herramientas/capacidades) y obtiene nombre, descripción y esquema de cada herramienta de forma programática. |
| **Acoplamiento cliente–servicio** | Alto: el código cliente está escrito contra la forma exacta de esa API particular; cambiar el endpoint o el formato de respuesta rompe el cliente. | Bajo: cualquier cliente MCP puede hablar con cualquier servidor MCP porque ambos comparten el mismo protocolo de descubrimiento e invocación; el cliente no conoce de antemano las herramientas específicas. |
| **Formato de los mensajes** | Varía por API: puede ser REST/JSON, XML, gRPC, GraphQL, SOAP, etc. — cada una con sus propias convenciones. | Estandarizado: siempre JSON-RPC 2.0, con una estructura de mensajes (requests, responses, notifications) definida por la especificación de MCP. |
| **Autenticación y consentimiento** | Definida por cada proveedor (API keys, OAuth, tokens propios); el consentimiento del usuario final suele resolverse fuera del flujo técnico. | El protocolo contempla mecanismos propios de autorización (OAuth para transportes remotos) y primitivas explícitas de interacción con el usuario, como *elicitation*, para pedir consentimiento o datos adicionales antes de ejecutar una acción sensible. |
| **Reutilización entre aplicaciones distintas** | Baja: cada aplicación que quiera usar esa API debe implementar su propio código de integración contra esa API específica. | Alta: un mismo servidor MCP (p. ej. el de sistema de archivos) puede conectarse, sin cambios, a Claude Code, Claude Desktop, Cursor, VS Code o cualquier otro cliente que implemente el protocolo. |

## MCP no sustituye a las APIs

Es fundamental dejarlo explícito: **MCP no reemplaza ni vuelve obsoletas a las APIs**. Un servidor MCP casi siempre **envuelve** (hace de *wrapper* de) una API, una base de datos, un sistema de archivos o cualquier otro recurso ya existente. El servidor MCP de sistema de archivos, por ejemplo, internamente sigue usando las llamadas normales del sistema operativo para leer y escribir archivos — MCP solo agrega, por encima de eso, una capa que:

1. Describe esas operaciones en un catálogo que un modelo puede leer y entender.
2. Permite que el modelo decida cuál invocar según el lenguaje natural del usuario.
3. Estandariza cómo se transmiten esa invocación y su resultado.
