
.PHONY: build
build:
	docker build -t clients-db -f Dockerfile .

.PHONY: run
run:
	- docker network create "clients"
	- docker-compose -f docker-compose.yaml up -d
