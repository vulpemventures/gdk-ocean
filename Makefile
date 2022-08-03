stubs:
	rm -rf ocean
	cp -r specs/api-spec/protobuf/gen/python/ocean ocean

env:
	python3.9 -m venv venv

deps:
	pip install -r requirements.txt

run:
	python gdk-ocean.py

docker-image:
	docker build -t gdk-ocean .  

container:
	docker run -it --net=host gdk-ocean