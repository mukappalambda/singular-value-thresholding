clean:
	@find . -type d -name '__pycache__' | xargs -I{} rm -rf {}

style:
	@poetry run ruff format examples svt
	@poetry run ruff check --select I examples svt --fix
