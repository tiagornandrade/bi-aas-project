IMAGE_NAME=airbyte-container
TAG=latest

.PHONY: build run clean

build:
	docker build -t $(IMAGE_NAME):$(TAG) .

run:
	docker run --rm -it \
    -v /var/run/docker.sock:/var/run/docker.sock \
    airbyte-container

clean:
	docker rmi $(IMAGE_NAME):$(TAG)

install:
	abctl local install --low-resource-mode --no-browser

uninstall:
	abctl local uninstall

credential:
	abctl local credentials --password YamsLab
