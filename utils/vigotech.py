"""Cliente sencillo para obtener eventos próximos de VigoTech.

La fuente (https://vigotech.org/vigotech-generated.json) es un objeto con
los grupos del alianza VigoTech. Cada grupo activo tiene un `nextEvent`.
Aquí lo aplanamos a una lista plana de `Event` y filtramos por tema/fecha.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

import requests
from pydantic import BaseModel

VIGOTECH_URL = "https://vigotech.org/vigotech-generated.json"

_cache: dict[str, Any] | None = None


class Event(BaseModel):
    title: str
    date: datetime
    location: str
    url: str
    group: str


def _fetch() -> dict[str, Any]:
    global _cache
    if _cache is None:
        response = requests.get(VIGOTECH_URL, timeout=10)
        response.raise_for_status()
        _cache = response.json()
    return _cache


def _normalize(members: dict[str, Any]) -> list[Event]:
    events: list[Event] = []
    for key, group in members.items():
        if group.get("inactive"):
            continue
        raw = group.get("nextEvent")
        if not raw:
            continue
        events.append(
            Event(
                title=raw["title"],
                date=datetime.fromtimestamp(raw["date"] / 1000),
                location=raw.get("location", "Por confirmar"),
                url=raw["url"],
                group=group.get("name", key),
            )
        )
    return events


def get_vigotech_events(
    topic: str | None = None,
    days_ahead: int = 30,
) -> list[Event]:
    """Devuelve los próximos eventos tech de la alianza VigoTech.

    Args:
        topic: Palabra clave opcional. Filtra por coincidencia en título o
            grupo (case-insensitive). Ejemplos: "python", "IA", "agile".
        days_ahead: Solo eventos en los próximos N días (por defecto 30).

    Returns:
        Lista de eventos próximos ordenada por fecha, filtrada por los
        criterios. Puede estar vacía si no hay coincidencias.
    """
    events = _normalize(_fetch().get("members", {}))

    now = datetime.now()
    deadline = now + timedelta(days=days_ahead)
    events = [e for e in events if now <= e.date <= deadline]

    if topic:
        needle = topic.lower()
        events = [
            e for e in events
            if needle in e.title.lower() or needle in e.group.lower()
        ]

    return sorted(events, key=lambda e: e.date)


if __name__ == "__main__":
    # Self-test: ejecutar como `python -m utils.vigotech` o `make smoke`.
    # Imprime qué eventos están disponibles hoy para preparar el demo.
    print(f"Fuente: {VIGOTECH_URL}\n")
    events = get_vigotech_events()
    if not events:
        print("⚠️  CERO eventos próximos. Revisa los prompts del demo —")
        print("   no funcionará 'qué eventos hay esta semana'.")
    else:
        print(f"{len(events)} evento(s) próximo(s):\n")
        for e in events:
            print(f"  · [{e.date.date()}] {e.group}")
            print(f"    {e.title}")
            print(f"    📍 {e.location}")
            print(f"    🔗 {e.url}\n")
        print("Prompts recomendados para el demo:")
        topics = sorted({e.group.split()[0].lower() for e in events})
        print(f"  - ¿Qué eventos próximos hay en Vigo?")
        for t in topics:
            print(f"  - ¿Hay algún evento de {t}?")
