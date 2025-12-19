run:
	python -m src.app.main

test:
	pytest

lint:
	flake8 src
