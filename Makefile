UV := uv run
ALEMBIC := $(UV) alembic

.PHONY: start migration upgrade downgrade history current lint fix typecheck

start:
	$(UV) uvicorn app.main:app --reload --no-access-log

migration:
	$(ALEMBIC) revision --autogenerate -m "$(msg)"

upgrade:
	$(ALEMBIC) upgrade head

downgrade:
	$(ALEMBIC) downgrade -1

history:
	$(ALEMBIC) history

current:
	$(ALEMBIC) current

lint:
	$(UV) ruff check .

fix:
	$(UV) ruff check --fix .

typecheck:
	$(UV) mypy .