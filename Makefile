stubs:
	buf generate buf.build/vulpemventures/ocean:b2facb6f8278a6377c344b1b16446b4a5a905abe

env:
	python3.9 -m venv venv

deps:
	pip install -r requirements.txt

run:
	python gdk-ocean.py