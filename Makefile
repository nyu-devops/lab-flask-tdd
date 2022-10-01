.PHONY: all help install venv test run

help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-\\.]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

all: help

venv: ## Create a Python virtual environment
	$(info Creating Python 3 virtual environment...)
	python3 -m venv .venv

install: ## Install dependencies
	$(info Installing dependencies...)
	sudo pip install -r requirements.txt

lint: ## Run the linter
	$(info Running linting...)
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --max-complexity=10 --max-line-length=127 --statistics
	pylint service tests --max-line-length=127

test: ## Run the unit tests
	$(info Running tests...)
	nosetests --with-spec --spec-color

run: ## Run the service
	$(info Starting service...)
	honcho start
