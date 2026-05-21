"""Paso 2: Agente + tool.

Mismo agente que en el paso 1, pero ahora con una herramienta real
que consulta vigotech.org. El LLM decide cuándo llamarla y con qué
parámetros (topic, days_ahead) en función de la pregunta del usuario.

Demo: repite "¿Qué eventos de Python hay esta semana en Vigo?".
Esta vez el agente llama a get_vigotech_events y responde con datos
de verdad.
"""
from google.adk.agents import Agent

from utils.vigotech import get_vigotech_events

root_agent = Agent(
    name="vigotech_events_assistant",
    model="gemini-3-flash-preview",
    instruction=(
        "Eres un asistente de eventos de la alianza VigoTech en Vigo. "
        "Usa la tool `get_vigotech_events` para obtener eventos reales "
        "antes de responder. Nunca te inventes eventos: si la tool "
        "no devuelve nada, dilo claramente. "
        "Responde en el mismo idioma que el usuario "
        "(castellano, gallego o inglés). Sé conciso."
    ),
    tools=[get_vigotech_events],
)
