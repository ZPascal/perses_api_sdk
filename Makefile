.PHONY: test integration-up integration-down integration integration-logs

test:
	uv run pytest tests/unit/ -v

integration-up:
	docker compose up -d --wait

integration-down:
	docker compose down

integration-logs:
	docker compose logs perses

integration: integration-up
	curl -sf -X POST http://localhost:8080/api/v1/users \
		-H "Content-Type: application/json" \
		-d '{"kind":"User","metadata":{"name":"admin"},"spec":{"firstName":"Admin","lastName":"","nativeProvider":{"password":"password"}}}' || true
	TOKEN=$$(curl -sf -X POST http://localhost:8080/api/auth/providers/native/login \
		-H "Content-Type: application/json" \
		-d '{"login":"admin","password":"password"}' | python3 -c "import sys,json; print(json.load(sys.stdin)[\"access_token\"])") && \
	curl -sf -X POST http://localhost:8080/api/v1/globalroles \
		-H "Content-Type: application/json" \
		-H "Authorization: Bearer $$TOKEN" \
		-d '{"kind":"GlobalRole","metadata":{"name":"admin"},"spec":{"permissions":[{"actions":["*"],"scopes":["*"]}]}}' && \
	curl -sf -X POST http://localhost:8080/api/v1/globalrolebindings \
		-H "Content-Type: application/json" \
		-H "Authorization: Bearer $$TOKEN" \
		-d '{"kind":"GlobalRoleBinding","metadata":{"name":"admin"},"spec":{"role":"admin","subjects":[{"kind":"User","name":"admin"}]}}' || true
	PERSES_HOST=http://localhost:8080 \
	PERSES_USERNAME=admin \
	PERSES_PASSWORD=password \
	uv run pytest tests/integration/ -v; \
	status=$$?; \
	$(MAKE) integration-down; \
	exit $$status
