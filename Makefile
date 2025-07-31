help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

clean: ## Remove __pycache__
	@echo "$(WHALE) $@"
	@find . -type d -name '__pycache__' | xargs -I{} rm -rf {}

style: ## Format the codebase
	@echo "$(WHALE) $@"
	@poetry run ruff format examples svt
	@poetry run ruff check --extend-select I examples svt --fix
