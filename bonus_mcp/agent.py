"""Bonus: tools desde un servidor MCP (server-fetch).

Mismo agente que `step2_tools`, pero con DOS herramientas:

  · get_vigotech_events  — función Python en este repo.
  · fetch                 — tool MCP servida por `mcp-server-fetch`,
                            un proceso independiente que arrancamos
                            vía `uvx`.

La promesa de MCP: las tools no tienen que vivir en tu repo. Pueden
venir de cualquier proceso que hable el protocolo — otro lenguaje,
otro equipo, otra empresa.

Flujo típico: el LLM llama a `get_vigotech_events` para listar
eventos, luego a `fetch` con la URL de uno concreto para leer la
página de anuncio y dar más contexto.

Pre-requisitos en bonus_mcp/README.md.
"""
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from mcp import StdioServerParameters

from utils.vigotech import get_vigotech_events

fetch_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="uvx",
            args=["mcp-server-fetch"],
        ),
    ),
)

root_agent = Agent(
    name="vigotech_events_assistant",
    model="gemini-3-flash-preview",
    instruction=(
        "Eres un asistente de eventos de la alianza VigoTech en Vigo. "
        "Usa `get_vigotech_events` para listar eventos. Si el usuario "
        "quiere más detalles de un evento concreto, usa `fetch` con su "
        "URL para leer la página de anuncio y resumirla. "
        "Responde en el mismo idioma que el usuario "
        "(castellano, gallego o inglés). Sé conciso."
    ),
    tools=[get_vigotech_events, fetch_toolset],
)
