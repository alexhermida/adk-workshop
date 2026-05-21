# Workshop: Introducción práctica a Google ADK

**VigoTech Events Assistant** — construimos en 75 min un agente que consulta eventos reales de [vigotech.org](https://vigotech.org).

Mental model: **Model + Instructions + Tools = Agent**.

## Requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Una clave de [Google AI Studio](https://aistudio.google.com/apikey) (gratis)

## Setup (2 pasos)

```bash
git clone <este-repo>
cd adk-workshop
make setup           # uv sync + crea .env
# Edita .env y pega tu GOOGLE_API_KEY
```

## Lanzar

```bash
make web             # equivale a `uv run adk web`
```

Abre la URL que imprime ADK (normalmente <http://localhost:8000>) y selecciona el agente que quieras probar en el menú desplegable.

## Pasos del taller

1. **`step1_basic_agent/`** — Model + Instructions, sin tools. El agente alucina eventos plausibles que no existen. **Esa es la lección.**
2. **`step2_tools/`** — Añadimos `get_vigotech_events`. El agente decide cuándo llamarla y con qué parámetros. Datos reales.
3. **`step3_structured_output/`** — `SequentialAgent`: un agente obtiene eventos, otro devuelve una `EventRecommendation` tipada con Pydantic. (Sí, multi-agent, mínimo. Ver [ADR-0001](docs/adr/0001-sequential-agent-for-structured-output.md).)

## Bonus tracks (opcional)

Dos extras para después del taller — fuera del recorrido principal:

- **`bonus_mcp/`** — el agente del paso 2 + una segunda tool (`fetch`) servida por `mcp-server-fetch` en otro proceso vía MCP. Pre-requisito: `uvx` (incluido con `uv`).
- **`bonus_ollama/`** — el agente del paso 1 corriendo con Gemma 4 local en lugar de Gemini. Pre-requisito: [Ollama](https://ollama.com/download) + `ollama pull gemma4:e2b` (~7.2 GB).

Cada bonus tiene su propio `README.md` con instrucciones.

## Preguntas para probar

- "¿Qué eventos hay esta semana?"
- "¿Hay algún meetup de IA?"
- "What Python events do you have?"
- "Recomenda un evento para alguén que comeza con IA"

## Para seguir explorando

- **Multi-agent** — `SequentialAgent` (que ya viste), `ParallelAgent`, `LoopAgent`, delegación con `sub_agents`.
- **MCP** — tus tools no tienen que ser funciones Python; pueden venir de un servidor MCP (`MCPToolset`).
- **Deployment** — `adk deploy agent-engine` o Cloud Run.
- **Evals** — `adk eval` para evaluar la calidad del agente con datasets.

Docs: <https://adk.dev>
