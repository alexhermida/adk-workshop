---
marp: true
theme: default
class: invert
paginate: true
style: |
  section { font-family: -apple-system, system-ui, sans-serif; }
  h1 { font-size: 2.4em; }
  h2 { color: #4dd0e1; }
  code { background: #2a2a2a; padding: 2px 8px; border-radius: 4px; }
  .big { font-size: 2em; text-align: center; margin-top: 1em; }
---

<!-- _class: invert -->

# Workshop ADK VigoTech

### Introducción práctica a Google ADK

<br>

**Python Vigo / VigoTech**

`make setup && make web`

---

## El mental model

<br>

<div class="big">

`Model` **+** `Instructions` **+** `Tools`

**=** `Agent`

</div>

---

## Tres pasos, 75 minutos

<br>

**1. `step1_basic_agent`** — el agente alucina — *10 min*

**2. `step2_tools`** — datos reales de vigotech.org — *20 min*

**3. `step3_structured_output`** — Pydantic + SequentialAgent — *15 min*

<br>

> El código vive en el repo. Lo que ves aquí es el menú.

---

## Para seguir explorando

<br>

- **Multi-agent** — `ParallelAgent`, `LoopAgent`, delegación
- **MCP** — `McpToolset`, tools desde servidores externos
- **Deployment** — `adk deploy agent-engine`, Cloud Run
- **Evals** — `adk eval` con datasets

<br>

En el repo: `bonus_mcp/` · `bonus_ollama/` — pruébalos en casa

<br>

Docs: **adk.dev**

---

# Grazas / Gracias

<br>

Repo: este `git clone` que acabas de hacer

Charla: **<https://vigotech.org>**

<br>

*¿Preguntas?*
