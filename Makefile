stubs:
	buf generate buf.build/vulpemventures/ocean

env:
	python3.9 -m venv venv

deps:
	pip install -r requirements.txt

run:
	python gdk-ocean.py