"""Paso 3: Output estructurado con SequentialAgent.

Restricción de ADK: `output_schema` deshabilita tool calling en el mismo
LlmAgent. Para combinar "llamar a una tool" + "devolver Pydantic"
componemos dos agentes en secuencia:

  fetcher (con tool, output_key="events_json")
    │
    ▼  pasa los eventos por session.state
  recommender (con output_schema=EventRecommendation, sin tools)

ADK sustituye `{events_json}` en la instruction del recommender por el
valor que el fetcher escribió en `session.state["events_json"]`. Esa es
la "pipelining" del SequentialAgent. Patrón canónico para este caso —
ver docs/adr/0001-*.md.

Demo: "Recomienda un evento para alguien interesado en IA".
"""
from datetime import datetime
from typing import Literal

from google.adk.agents import Agent, SequentialAgent
from pydantic import BaseModel, Field

from utils.vigotech import get_vigotech_events


class EventRecommendation(BaseModel):
    title: str
    date: datetime
    url: str
    reason: str = Field(description="Por qué este evento, breve.")
    level: Literal["junior", "senior", "any"]


fetcher = Agent(
    name="event_fetcher",
    model="gemini-3-flash-preview",
    instruction=(
        "Llama a `get_vigotech_events` con los filtros adecuados según la "
        "petición del usuario y responde ÚNICAMENTE con el array JSON crudo "
        "que devuelva la tool — empezando por `[`, sin fences ni prosa."
    ),
    tools=[get_vigotech_events],
    output_key="events_json",
)

recommender = Agent(
    name="event_recommender",
    model="gemini-3-flash-preview",
    instruction=(
        "Eres un recomendador de eventos. "
        "Eventos disponibles (JSON):\n{events_json}\n\n"
        "Examina la petición original del usuario y elige UN evento. "
        "Clasifica `level` como 'junior' si es introductorio, 'senior' si "
        "es avanzado, o 'any' si es mixto. "
        "Escribe `reason` en el mismo idioma que el usuario."
    ),
    output_schema=EventRecommendation,
)

root_agent = SequentialAgent(
    name="vigotech_events_assistant",
    sub_agents=[fetcher, recommender],
)
