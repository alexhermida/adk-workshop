# Bonus: agente sin tools, modelo local con Ollama

Igual que `step1_basic_agent`, pero el modelo no es Gemini en la
nube — es Gemma 4 corriendo en tu máquina, servido por Ollama.

## Pre-requisitos

1. [Ollama](https://ollama.com/download) instalado y arrancado.
2. Descargar el modelo (~7.2 GB):

   ```bash
   ollama pull gemma4:e2b
   ```

3. Verificar que Ollama responde:

   ```bash
   ollama list   # debería listar gemma4:e2b
   ```

## Cómo lanzarlo

```bash
make web    # o: uv run adk web
```

Selecciona `bonus_ollama` en el desplegable del UI.

## Pregunta de prueba

> "¿Qué eventos de Python hay esta semana en Vigo?"

Como en `step1_basic_agent`, el modelo se inventa eventos
plausibles. **Esa sigue siendo la lección.** La diferencia: ahora
ocurre en tu portátil, offline, sin tocar la nube.

## Por qué sólo el paso 1

Los modelos de 2B parámetros llaman a tools de forma menos fiable
que Gemini. Steps 2 y 3 dependen de tool-calling robusto — si
intentas el swap ahí con `gemma4:e2b`, verás al agente saltarse las
tools o pasar parámetros raros.

Para reproducir steps 2 y 3 en local: prueba con un modelo más
grande como `qwen2.5:7b-instruct` o `llama3.1:8b`.

## La lección

ADK no acopla tu agente a un proveedor de modelos. Cambias una línea
(`model=LiteLlm(...)`) y el mismo agente corre contra Ollama, Vertex,
Anthropic, OpenAI... Modelo y agente son piezas separadas.
