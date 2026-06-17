.PHONY: backend dashboard edge mlops test lint

backend:
	cd backend && go run ./cmd/server

backend-test:
	cd backend && go test ./...

dashboard:
	cd dashboard && npm run dev

edge-test:
	cd edge && python -m pytest tests/

mlops-eval:
	cd mlops && make eval

lint:
	cd backend && go vet ./...
	cd dashboard && npm run lint

up:
	docker-compose up

down:
	docker-compose down
