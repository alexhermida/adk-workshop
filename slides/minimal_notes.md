# Notas mínimas del speaker — Workshop ADK VigoTech (75 min)

## Timeline

| Min   | Bloque                              | Descripción                                       |
|-------|-------------------------------------|--------------------------------------------------|
| 0-10  | Setup                               | Doors open + ayudar con `uv sync` y `.env`       |
| 10-15 | Intro                               | "Model + Instructions + Tools = Agent"           |
| 15-25 | **step1_basic_agent**               | No tools                |
| 25-45 | **step2_tools**                     | Mismo prompt, ahora con tool.      |
| 45-60 | **step3_structured_output**         | SequentialAgent + Pydantic                       |
| 60-75 | Q&A + Para seguir explorando        | Multi-agent / MCP / Deploy / Evals               |

## Intro (10-15) — 5 min

- ¿Qué es un agente? **Model + Instructions + Tools.** Tres cosas, nada más.

- ADK

http://adk.dev/
https://adk.dev/tutorials/coding-with-ai/

- ¿Qué aporta ADK? Una forma idiomática y Python-nativa de juntar esas tres cosas, con runtime (`adk web`), orquestación (`SequentialAgent`...), y conexiones (tools, MCP, deploy).
- Hoy: construimos un asistente de eventos VigoTech, en tres pasos.

## Step 1 (15-25) — 10 min

Mostrar `step1_basic_agent/agent.py` (15 líneas).


- "Aquí está el agente. Model + Instructions. Cero tools."
- Lanzar `adk web`, seleccionar `step1_basic_agent`.
- Preguntar: **"¿Qué eventos de Python hay esta semana en Vigo?"**
- El modelo inventa 3 eventos plausibles.
- **PAUSAR.** "Busca esos eventos. No existen."
- Explicar: el LLM es autocompletado elegante. Sin tools, no sabe nada del mundo real.
- "En el siguiente paso le damos datos reales."

## Step 2 (25-45) — 20 min

Mostrar `utils/vigotech.py` primero (~50 líneas):
- Pydantic `Event` para validar datos al cruzar el borde de la red.
- `get_vigotech_events(topic, days_ahead)` — *una* tool, con parámetros opcionales.

Mostrar `step2_tools/agent.py` (~20 líneas):
- Mismo agente, pero `tools=[get_vigotech_events]`.
- Resaltar: ADK construye el schema de la tool a partir del **type hint + docstring**. Nada más.
- La instruction ahora dice "usa la tool, no te inventes nada".

Lanzar `adk web`, seleccionar `step2_tools`. Repetir la pregunta.

- El agente llama a la tool. El UI muestra el tool call.
- Responde con eventos reales.
- Probar variantes:
  - "¿Hay algún meetup de IA?" → ver al LLM elegir `topic="IA"`.
  - "What Python events do you have?" → cambio de idioma + parámetro.

**El punto pedagógico:** el LLM no solo *llama* la tool, *elige los parámetros* en función del prompt. Esa es la inteligencia que ADK conecta.

## Step 3 (45-60) — 15 min

- "Vale, ahora queremos respuesta tipada — Pydantic."
- "Pero hay una trampa: `output_schema` **deshabilita las tools**."
- Solución canónica de ADK: dos agentes en `SequentialAgent`.

Mostrar `step3_structured_output/agent.py` (~50 líneas):
- `EventRecommendation` — Pydantic con `Literal["junior", "senior", "any"]`.
- `fetcher` — tiene la tool, escribe a `output_key="events_json"`.
- `recommender` — tiene `output_schema`, lee `{events_json}` de state.
- `root_agent = SequentialAgent(sub_agents=[fetcher, recommender])`.

Resaltar la **state injection**: `{events_json}` en la instruction se sustituye por el valor en state. Eso es ADK haciendo pipelining.

Lanzar `adk web`, seleccionar `step3_structured_output`.

- "Recomenda un evento para alguén interesado en IA."
- Ver dos turnos: primero el fetcher (con tool), después el recommender (JSON tipado).

## Q&A + Futuro (60-75) — 15 min

Cada uno ~2 min, en este orden de "más relevante a lo ya tocado":

1. **Multi-agent**: ya viste `SequentialAgent`. También `ParallelAgent`, `LoopAgent`, y delegación con `sub_agents` (el coordinador decide a quién pasarle la petición).
2. **MCP**: tus tools no tienen que ser funciones locales. `MCPToolset(...)` conecta a un servidor MCP y expone esas tools al agente.
3. **Deployment**: `adk deploy agent-engine` (Vertex) o Cloud Run.
4. **Evals**: `adk eval` con datasets. Tracking de calidad como tests pero con criterios LLM.

*Si Q&A se anima:* dejar caer 1-2 temas (típicamente MCP y Evals). Si no, presentarlos todos y abrir preguntas al final.

## Datos reales: la situación al día del taller

Verifica con **`make smoke`** antes de empezar (imprime los eventos vivos y sugiere prompts). A día de hoy hay **1 evento próximo en toda la alianza**: la propia "Reunión mayo 2026" de PythonVigo (2 días después del taller).

Esto es un regalo, no un problema:
- **Auto-referencia perfecta**: el agente recomienda al público asistir a su propio meetup mensual. Buen humor en sala.
- **"location: Por confirmar"**: PythonVigo no tiene location en el JSON. La normalización en `utils/vigotech.py` lo rellena con un fallback. Punto de discusión sobre calidad de datos reales y normalización en el borde.
- **Si una query no encuentra nada** (ej. "Rust", "Go"): el agente del paso 2 debe decirlo (la instruction lo fuerza). Demo de "no alucinar es una *propiedad* del prompt".

Prompts seguros para el demo (todos producen ≥1 resultado):
- "¿Qué eventos próximos hay en Vigo?"
- "¿Hay algo de Python?"
- "Recomenda un evento [paso 3]"

Prompts que devuelven vacío (úsalos *intencionalmente* para mostrar el manejo):
- "¿Hay algo de Rust?" (paso 2 — el agente dice 'no hay')
- "Recomenda un evento de bases de datos" (paso 3 — riesgo, ver siguiente sección)

## Errores típicos durante el taller

| Síntoma                                      | Causa probable                                  |
|----------------------------------------------|-------------------------------------------------|
| "GOOGLE_API_KEY not set"                     | Faltó `cp .env.example .env` o editarlo         |
| `adk: command not found`                     | No corrió `uv sync` o no está usando `uv run`   |
| Agente del paso 2 NO llama a la tool         | Modelo ignorando la instrucción — reformula     |
| Tool devuelve `[]`                           | Sin eventos que coincidan (es real, ver arriba) |
| Step 3 produce recomendación rara con `[]`   | `output_schema` no tiene "no hay" — evita queries que no matcheen |
