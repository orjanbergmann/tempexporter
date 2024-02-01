TAG := exporter.temp:latest

all: image

image: Dockerfile
	docker build --rm -t $(TAG) .

run:
	docker run --rm -p 9102:9102 $(TAG)

purge:
	docker image prune
