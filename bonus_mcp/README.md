# Bonus: tools via MCP (`server-fetch`)

Igual que `step2_tools`, pero con una segunda herramienta — `fetch` —
que vive en otro proceso (`mcp-server-fetch`) y se comunica con el
agente vía stdio.

## Pre-requisito

Sólo necesitas `uvx` (incluido con `uv`, ya instalado). La primera
vez que arranques el agente, `uvx` descarga `mcp-server-fetch` en
segundo plano (un par de segundos).

## Cómo lanzarlo

```bash
make web    # o: uv run adk web
```

Selecciona `bonus_mcp` en el desplegable del UI.

## Pregunta de prueba

> "Lista los eventos próximos en Vigo y dame los detalles del primero."

El agente debería:

1. Llamar a `get_vigotech_events` (función Python local).
2. Llamar a `fetch` (tool MCP) con la URL del primer evento.
3. Resumir el contenido de la página.

## La lección

`fetch` no es una función en este repo. Es un proceso
independiente publicado en PyPI por terceros. El agente la usa
exactamente igual que usa `get_vigotech_events`. **Esa es la
promesa de MCP**: tools desde cualquier lenguaje, repo o equipo,
expuestas al LLM con el mismo schema y la misma plomería.
