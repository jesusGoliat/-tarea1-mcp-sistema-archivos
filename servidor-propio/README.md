# Servidor MCP propio (opcional, +10 pts)

Servidor mínimo construido con el SDK oficial de Python (`mcp`, específicamente `mcp.server.fastmcp.FastMCP`), con dos herramientas propias distintas de las que ya ofrece el servidor de sistema de archivos.

## Herramientas expuestas

| Herramienta | Parámetros | Qué hace |
|---|---|---|
| `contar_texto` | `texto: str` | Devuelve caracteres, palabras y líneas de un texto dado. |
| `convertir_temperatura` | `valor: float`, `origen: str`, `destino: str` | Convierte una temperatura entre `celsius`, `fahrenheit` y `kelvin`. |

## Instalación reproducible

Requiere Python 3.10+ (probado con Python 3.12.3).

```bash
cd servidor-propio
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> Nota de este entorno: en la máquina donde se desarrolló esta tarea ya existía un virtualenv (`~/venvs/pipeline`) con `mcp` instalado, así que en la práctica se usó `source ~/venvs/pipeline/bin/activate` en vez de crear uno nuevo. En una máquina limpia, sigue los pasos de arriba para crear tu propio entorno virtual.

## Probar que arranca

```bash
python server.py
```

El proceso queda esperando mensajes JSON-RPC por `stdin`/`stdout` (transporte stdio) — es exactamente lo que un cliente MCP como Claude Code hace por ti al lanzarlo como subproceso, así que no hace falta ejecutarlo manualmente salvo para verificar que no tiene errores de arranque (`Ctrl+C` para salir).

## Conectarlo a Claude Code

Se agrega como un segundo servidor en el `.mcp.json` del proyecto, apuntando al intérprete del entorno virtual (no al `python` del sistema):

```json
{
  "mcpServers": {
    "filesystem-tarea1": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/ruta/al/workspace-demo"]
    },
    "servidor-propio": {
      "command": "/home/jesus/venvs/pipeline/bin/python",
      "args": ["/home/jesus/Desktop/Moviles/Tarea1/servidor-propio/server.py"]
    }
  }
}
```

Tras recargar los servidores MCP en Claude Code (reiniciar sesión o `/mcp`), `contar_texto` y `convertir_temperatura` deben aparecer listadas junto con las herramientas del servidor de sistema de archivos.
