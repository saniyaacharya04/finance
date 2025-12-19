.PHONY: run test lint clean

run:
	python -m src.app.main

test:
	pytest

lint:
	python -m py_compile $(shell find src -name "*.py")

clean:
	rm -rf __pycache__ .pytest_cache flask_session
