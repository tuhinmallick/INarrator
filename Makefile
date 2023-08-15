lint:
	black inarrator --check
	ruff --config pyproject.toml inarrator
	mypy inarrator

format:
	black inarrator
	ruff --config pyproject.toml --fix inarrator

spell_check:
	poetry run codespell --toml pyproject.toml

spell_fix:
	poetry run codespell --toml pyproject.toml -w