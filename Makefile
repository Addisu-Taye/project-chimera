# Project Chimera Makefile
# Standardized commands for development and CI/CD

.PHONY: setup test spec-check docker-build docker-test clean

# Environment variables
PYTHON ?= python3
DOCKER_IMAGE ?= project-chimera:latest

# Setup dependencies
setup:
	@echo "🔧 Setting up Python environment..."
	@if command -v uv >/dev/null 2>&1; then \
		echo "Using uv for faster installs..."; \
		uv pip install --system --all-extras; \
	else \
		echo "Using pip..."; \
		pip install --upgrade pip; \
		pip install -e .[dev]; \
	fi

# Run tests (should fail initially - this is success!)
test:
	@echo "🧪 Running TDD tests (expect failures - this defines agent goal posts)..."
	$(PYTHON) -m pytest tests/ -v

# Verify code aligns with specs (optional but recommended)
spec-check:
	@echo "🔍 Checking spec alignment..."
	@echo "TODO: Implement spec validation script"
	@exit 0

# Build Docker image
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t $(DOCKER_IMAGE) .

# Run tests in Docker
docker-test: docker-build
	@echo "🧪 Running tests in Docker container..."
	docker run --rm $(DOCKER_IMAGE)

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache

# Help
help:
	@echo "Project Chimera Makefile Commands:"
	@echo "  make setup      - Install dependencies"
	@echo "  make test       - Run TDD tests (expect failures)"
	@echo "  make spec-check - Verify code-spec alignment"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-test  - Run tests in Docker"
	@echo "  make clean      - Clean build artifacts"