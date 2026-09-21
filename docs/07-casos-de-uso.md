# 7. Casos de uso

## 1. Claude Code (Anthropic)

Claude Code es una herramienta de línea de comandos (y extensión de IDE) que actúa como **host y cliente MCP**: puede conectarse a servidores MCP definidos en un archivo `.mcp.json` del proyecto y usar sus herramientas —en esta misma tarea, el servidor de sistema de archivos— para leer, escribir, buscar y modificar archivos del repositorio directamente, sin que la persona copie y pegue código manualmente. También puede conectarse a servidores MCP de control de versiones, issue trackers, bases de datos, etc., ampliando lo que puede hacer sobre un proyecto completo según qué servidores estén conectados.

## 2. Cursor

Cursor es un editor de código basado en VS Code con capacidades agénticas integradas. Según su propia documentación (cursor.com/docs/context/mcp), Cursor implementa el lado cliente de MCP: permite configurar servidores MCP (locales vía stdio o remotos vía HTTP) y usar sus herramientas dentro del flujo de edición asistida por IA del editor, para que el modelo pueda operar sobre archivos del proyecto, ejecutar consultas a servicios externos o interactuar con APIs de terceros sin que la persona desarrolladora tenga que escribir manualmente el código de integración para cada una.

## 3. Google Antigravity

Google Antigravity es la plataforma de desarrollo agéntico de Google (basada en el modelo Gemini 3), presentada como una evolución del IDE tradicional hacia un flujo de trabajo "agent-first" (Google Developers Blog, s.f.). A diferencia de Qwen —que es una *familia de modelos* y no una plataforma de desarrollo, por lo que no es un ejemplo válido en este contexto—, Google Antigravity sí es un entorno agéntico real: desde principios de 2026 soporta servidores MCP (por ejemplo, el *MCP Toolbox for Databases* de Google, que conecta agentes a AlloyDB, BigQuery, Spanner o Cloud SQL) para que sus agentes puedan operar sobre datos y herramientas externas dentro del propio flujo de desarrollo (Google Cloud Blog, s.f.).

## Cómo editan repositorios completos sin subida manual de archivos

Las tres herramientas comparten el mismo patrón habilitado por MCP: en lugar de que la persona usuaria copie y pegue fragmentos de código en un chat web, el **host** (Claude Code, Cursor o Antigravity) ya tiene, a través de un servidor MCP de sistema de archivos (o de Git/control de versiones), acceso de lectura y escritura **directo y local** al directorio del proyecto. Cuando el modelo decide que necesita ver un archivo, invoca la herramienta `read_file` (o equivalente); cuando decide que necesita modificarlo, invoca `write_file` o `edit_file`. Como el servidor corre como proceso local (transporte stdio) sobre el propio repositorio abierto, **el modelo puede leer, crear, modificar o mover cualquier archivo del proyecto —dentro del alcance permitido— sin que la persona tenga que subir manualmente nada a un chat**: el ida y vuelta de "copiar salida del modelo, pegarla en el editor" desaparece, porque el propio modelo, a través del servidor MCP, ya está operando sobre los archivos reales del disco.
