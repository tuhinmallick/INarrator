lint:
	black . --check
	ruff --config pyproject.toml .
	mypy .

format:
	black .
	ruff --config pyproject.toml --fix .

spell_check:
	poetry run codespell --toml pyproject.toml

spell_fix:
	poetry run codespell --toml pyproject.toml -w