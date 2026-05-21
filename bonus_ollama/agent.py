"""Bonus: el agente del paso 1, ahora con modelo local (Ollama + Gemma 4).

Mismo Model + Instructions = Agente del paso 1. Lo único que cambia
es el modelo: en lugar de Gemini en la nube, Gemma 4 (~2B efectivos)
corriendo en tu portátil vía Ollama.

La lección: el modelo es un parámetro, no un compromiso. Para una
demo sin tools como esta, un modelo pequeño local es perfectamente
viable, gratis, y privado.

Por qué sólo el paso 1: los modelos pequeños (2B) llaman a tools de
forma menos fiable. Steps 2 y 3 dependen de eso — para reproducirlos
en local querrás algo como `qwen2.5:7b-instruct` o `llama3.1:8b`.

Pre-requisitos en bonus_ollama/README.md.
"""
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from utils.vigotech import get_vigotech_events

root_agent = Agent(
    name="vigotech_events_assistant",
    model=LiteLlm(model="ollama_chat/gemma4:e2b", think=False),
    instruction=(
        "Eres un asistente de eventos de la alianza VigoTech en Vigo. "
        "Responde en el mismo idioma que el usuario "
        "(castellano, gallego o inglés). Sé conciso."
    ),
    tools=[get_vigotech_events],
)
