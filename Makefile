.PHONY: help setup smoke web slides clean

help:
	@echo "Workshop ADK VigoTech — comandos disponibles:"
	@echo ""
	@echo "  make setup   Instala dependencias con uv y crea .env si no existe"
	@echo "  make smoke   Comprueba que la fuente de datos está viva (PRE-TALLER)"
	@echo "  make web     Lanza adk web (UI en http://localhost:8000)"
	@echo "  make slides  Sirve slides/backdrop.md en http://localhost:8080 (Marp)"
	@echo "  make clean   Borra .venv y cachés"

setup:
	uv sync
	@test -f .env || cp .env.example .env
	@echo "→ Edita .env y pega tu GOOGLE_API_KEY antes de 'make web'"

smoke:
	@uv run python -m utils.vigotech

web:
	uv run adk web

slides:
	npx --yes @marp-team/marp-cli@latest -s slides

clean:
	rm -rf .venv __pycache__ */__pycache__ */*/__pycache__
