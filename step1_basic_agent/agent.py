"""Paso 1: Agente mínimo.

Model + Instructions = Agente. Sin tools.

Demo: pregunta "¿Qué eventos de Python hay esta semana en Vigo?"
y observa cómo el modelo se inventa eventos plausibles que no existen.
Ese es el punto: un LLM sin tools es autocompletado elegante.
En el paso 2 le daremos datos reales.
"""
from dotenv import load_dotenv
from google.adk.agents import Agent

load_dotenv()

root_agent = Agent(
    name="vigotech_events_assistant",
    model="gemini-3-flash-preview",
    instruction=(
        "Eres un asistente de eventos de la alianza VigoTech en Vigo. "
        "Responde en el mismo idioma que el usuario "
        "(castellano, gallego o inglés). Sé conciso."
    ),
)
