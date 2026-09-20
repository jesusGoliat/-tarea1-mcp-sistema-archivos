"""Servidor MCP propio (opcional) para la Tarea 1.

Expone dos herramientas propias, distintas de las que ya ofrece el
servidor de sistema de archivos, usando el SDK oficial de Python (mcp).
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("tarea1-servidor-propio")


@mcp.tool()
def contar_texto(texto: str) -> dict:
    """Cuenta caracteres, palabras y lineas de un texto dado."""
    return {
        "caracteres": len(texto),
        "palabras": len(texto.split()),
        "lineas": len(texto.splitlines()) or 1,
    }


@mcp.tool()
def convertir_temperatura(valor: float, origen: str, destino: str) -> dict:
    """Convierte una temperatura entre celsius, fahrenheit y kelvin.

    origen/destino deben ser uno de: "celsius", "fahrenheit", "kelvin".
    """
    unidades = {"celsius", "fahrenheit", "kelvin"}
    origen = origen.lower()
    destino = destino.lower()
    if origen not in unidades or destino not in unidades:
        raise ValueError(f"Unidades validas: {sorted(unidades)}")

    # Normalizar a celsius primero
    if origen == "celsius":
        celsius = valor
    elif origen == "fahrenheit":
        celsius = (valor - 32) * 5 / 9
    else:  # kelvin
        celsius = valor - 273.15

    # Convertir de celsius a la unidad destino
    if destino == "celsius":
        resultado = celsius
    elif destino == "fahrenheit":
        resultado = celsius * 9 / 5 + 32
    else:  # kelvin
        resultado = celsius + 273.15

    return {"valor_original": valor, "origen": origen, "destino": destino, "resultado": round(resultado, 2)}


if __name__ == "__main__":
    mcp.run()
