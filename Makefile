.PHONY: help setup smoke web clean

help:
	@echo "Workshop ADK VigoTech — comandos disponibles:"
	@echo ""
	@echo "  make setup   Instala dependencias con uv y crea .env si no existe"
	@echo "  make smoke   Comprueba que la fuente de datos está viva (PRE-TALLER)"
	@echo "  make web     Lanza adk web (UI en http://localhost:8000)"
	@echo "  make clean   Borra .venv y cachés"

setup:
	uv sync
	@test -f .env || (cp .env.example .env && echo "→ Creado .env: edítalo y pega tu GOOGLE_API_KEY")

smoke:
	@uv run python -m utils.vigotech

web:
	uv run adk web

clean:
	rm -rf .venv __pycache__ */__pycache__ */*/__pycache__
