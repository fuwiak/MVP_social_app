# AI Business System - Docker Commands
# Make commands for easy Docker management

.PHONY: help build up down logs clean dev prod restart status

# Default target
help: ## Show this help message
	@echo "AI Business System - Docker Management"
	@echo "======================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Development commands
dev: ## Start development environment (backend only)
	@echo "🚀 Starting development environment..."
	docker-compose -f docker-compose.dev.yml up -d
	@echo "✅ Development environment started!"
	@echo "🌐 Backend API: http://localhost:8000"
	@echo "📖 API Docs: http://localhost:8000/docs"

dev-full: ## Start full development environment (backend + N8N)
	@echo "🚀 Starting full development environment..."
	docker-compose -f docker-compose.dev.yml --profile local-db up -d
	@echo "✅ Full development environment started!"
	@echo "🌐 Backend API: http://localhost:8000"
	@echo "📖 API Docs: http://localhost:8000/docs"
	@echo "🗄️  PostgreSQL: localhost:5432"

# Production commands
build: ## Build all Docker images
	@echo "🔨 Building Docker images..."
	docker-compose build --no-cache
	@echo "✅ Build completed!"

up: ## Start production environment
	@echo "🚀 Starting production environment..."
	docker-compose up -d
	@echo "✅ Production environment started!"
	@echo "🌐 Frontend: http://localhost:3000"
	@echo "🌐 Backend API: http://localhost:8000"
	@echo "📖 API Docs: http://localhost:8000/docs"

up-automation: ## Start with N8N automation
	@echo "🚀 Starting with N8N automation..."
	docker-compose --profile automation up -d
	@echo "✅ Environment with automation started!"
	@echo "🌐 Frontend: http://localhost:3000"
	@echo "🌐 Backend API: http://localhost:8000"
	@echo "🤖 N8N Automation: http://localhost:5678"

# Control commands
down: ## Stop all services
	@echo "🛑 Stopping all services..."
	docker-compose down
	docker-compose -f docker-compose.dev.yml down
	@echo "✅ All services stopped!"

restart: ## Restart all services
	@echo "🔄 Restarting all services..."
	make down
	make up
	@echo "✅ Services restarted!"

# Monitoring commands
logs: ## Show logs from all services
	docker-compose logs -f

logs-backend: ## Show backend logs only
	docker-compose logs -f backend

logs-frontend: ## Show frontend logs only
	docker-compose logs -f frontend

status: ## Show status of all containers
	@echo "📊 Container Status:"
	@echo "=================="
	docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Maintenance commands
clean: ## Clean up Docker resources
	@echo "🧹 Cleaning up Docker resources..."
	docker-compose down -v --remove-orphans
	docker-compose -f docker-compose.dev.yml down -v --remove-orphans
	docker system prune -f
	docker volume prune -f
	@echo "✅ Cleanup completed!"

clean-all: ## Clean everything including images
	@echo "🧹 Cleaning everything..."
	make clean
	docker image prune -a -f
	@echo "✅ Deep cleanup completed!"

# Database commands
db-reset: ## Reset development database
	@echo "🗄️  Resetting development database..."
	docker-compose -f docker-compose.dev.yml down postgres-dev
	docker volume rm test_next_postgres_dev_data 2>/dev/null || true
	docker-compose -f docker-compose.dev.yml --profile local-db up -d postgres-dev
	@echo "✅ Database reset completed!"

# Quick setup commands
setup: ## First time setup with environment file
	@echo "⚙️  Setting up environment..."
	@if [ ! -f .env ]; then \
		cp env.docker.example .env; \
		echo "📝 Created .env file from template"; \
		echo "⚠️  Please edit .env file with your API keys!"; \
	else \
		echo "📝 .env file already exists"; \
	fi
	make build
	@echo "✅ Setup completed!"

quick-start: ## Quick start for development
	@echo "🚀 Quick start for development..."
	make setup
	make dev
	@echo "✅ Development environment ready!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Edit .env file with your API keys"
	@echo "2. Start frontend: cd frontend && pnpm dev"
	@echo "3. Visit: http://localhost:3000"

# Health checks
health: ## Check health of all services
	@echo "🏥 Health Check:"
	@echo "==============="
	@curl -s http://localhost:8000/health | jq '.' 2>/dev/null || echo "❌ Backend not responding"
	@curl -s http://localhost:3000 > /dev/null 2>&1 && echo "✅ Frontend responding" || echo "❌ Frontend not responding"

# Development helpers
frontend-dev: ## Run frontend in development mode (outside Docker)
	@echo "🌐 Starting frontend development server..."
	@cd $(shell pwd) && pnpm install && pnpm dev

backend-shell: ## Get shell access to backend container
	docker-compose exec backend bash

redis-cli: ## Access Redis CLI
	docker-compose exec redis redis-cli

# Environment info
info: ## Show environment information
	@echo "AI Business System - Environment Info"
	@echo "===================================="
	@echo "Docker version: $$(docker --version)"
	@echo "Docker Compose version: $$(docker-compose --version)"
	@echo "Current directory: $$(pwd)"
	@echo "Environment file: $$([ -f .env ] && echo "✅ Found" || echo "❌ Missing")"
	@echo ""
	@echo "Available make commands:"
	@make help

