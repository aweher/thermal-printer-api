# Variables
REPO_NAME = registry.ayuda.la/public
IMAGE_NAME = thermal-printer-api
NOW = $(shell date +"%Y%m%d%H%M%S")

# Build the Docker image with two tags: :latest and :$NOW
build:
	docker build --no-cache -t $(REPO_NAME)/$(IMAGE_NAME):latest -t $(REPO_NAME)/$(IMAGE_NAME):$(NOW) .

push:
	@echo "Pushing latest tag..."
	@docker push $(REPO_NAME)/$(IMAGE_NAME):latest || (echo "Retrying push..." && sleep 5 && docker push $(REPO_NAME)/$(IMAGE_NAME):latest)
	@echo "Pushing timestamp tag..."
	@docker push $(REPO_NAME)/$(IMAGE_NAME):$(NOW) || (echo "Retrying push..." && sleep 5 && docker push $(REPO_NAME)/$(IMAGE_NAME):$(NOW))

all: build push
