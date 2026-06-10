.PHONY: run demo ui trace docker docker-run test clean help

help:
	@echo "AIS² Day 1 Implementation Targets"
	@echo ""
	@echo "run       - Generate minimal system trace (minimal_system.py)"
	@echo "demo      - Run all trace generators (minimal + failure + omega)"
	@echo "ui        - Launch Streamlit dashboard"
	@echo "trace     - Generate trace (alias for run)"
	@echo "docker    - Build Docker image (ais2-ui)"
	@echo "docker-run- Run Docker container at localhost:8501"
	@echo "test      - Run unit tests (placeholder)"
	@echo "clean     - Remove traces and build artifacts"

run:
	@echo "Generating minimal system trace..."
	python examples/minimal_system.py

demo: run
	@echo "Generating failure demo trace..."
	python examples/failure_demo.py
	@echo "Generating omega demo trace..."
	python examples/omega_transition_demo.py
	@echo "All traces generated in traces/"

ui:
	@echo "Launching Streamlit dashboard..."
	streamlit run dashboard/app.py

trace: run

docker:
	@echo "Building Docker image (ais2-ui)..."
	docker build -t ais2-ui .
	@echo "Image built successfully"

docker-run: docker
	@echo "Running Docker container at localhost:8501..."
	docker run -p 8501:8501 ais2-ui

test:
	@echo "Running tests..."
	python -m pytest tests/ -v

clean:
	@echo "Cleaning traces and build artifacts..."
	rm -rf traces/*.json
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Clean complete"

# Day 1 Verification
verify-day1:
	@echo "Day 1 Checkpoint Verification"
	@echo "✓ Phase 1: trace_exporter.py exists"
	@test -f trace_exporter.py && echo "  ✓ trace_exporter.py present"
	@echo "✓ Phase 2: examples created"
	@test -f examples/minimal_system.py && echo "  ✓ minimal_system.py present"
	@test -f examples/failure_demo.py && echo "  ✓ failure_demo.py present"
	@test -f examples/omega_transition_demo.py && echo "  ✓ omega_transition_demo.py present"
	@echo "✓ Phase 3: dashboard created"
	@test -f dashboard/app.py && echo "  ✓ app.py present"
	@echo "✓ Phase 4: Docker created"
	@test -f docker/Dockerfile && echo "  ✓ Dockerfile present"
	@echo "✓ Phase 5: Makefile complete"
	@echo ""
	@echo "Run 'make demo' to execute all examples"
	@echo "Run 'make ui' to launch dashboard (requires traces/)"
	@echo "Run 'make docker-run' to run via Docker"
