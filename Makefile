stubs:
	buf generate buf.build/vulpemventures/ocean
	touch ./ocean/v1/__init__.py

env:
	python3.9 -m venv venv

deps:
	pip install -r requirements.txt

deps-cli:
	pip install -r requirements_cli.txt

deps-cli-reinstall:
	pip install --force-reinstall -r requirements_cli.txt 

deps-reinstall:
	pip install --force-reinstall -r requirements.txt

run:
	python gdk-ocean.py

test:
	pytest -s 