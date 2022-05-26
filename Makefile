build:
	docker-compose build

run:
	docker-compose up -d --remove-orphans

restart:
	make stop && make build && make run

stop:
	docker-compose down -v

test:
	make build && make run
	chmod +x ./run-ps-tests.sh
	./run-ps-tests.sh
	make stop