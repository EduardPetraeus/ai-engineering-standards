# README Template

Copy this template when creating a new project README. Fill in each section. Delete sections that don't apply.

---

```markdown
# Project Name

One-line description of what this project does and who it's for.

## Overview

2-3 sentences explaining the project's purpose, key value proposition, and where it fits in the larger system. Include a link to any parent project or documentation.

**Status:** Active / Beta / Deprecated
**Version:** 0.1.0

## Quick Start

Minimum steps to get the project running locally:

\```bash
# Clone
git clone https://github.com/org/project-name.git
cd project-name

# Install
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your settings

# Run
python -m src.main
\```

## Architecture

Brief description of the system architecture. Include a diagram if it helps:

\```
┌─────────┐     ┌──────────┐     ┌──────────┐
│  Client  │────►│   API    │────►│ Database │
└─────────┘     └──────────┘     └──────────┘
                     │
                     ▼
                ┌──────────┐
                │  Queue   │
                └──────────┘
\```

Key components:
- **API** — FastAPI service handling HTTP requests
- **Database** — PostgreSQL for persistent storage
- **Queue** — Redis for async job processing

## Development

### Prerequisites

- Python 3.11+
- Docker (for local database)
- Make (optional, for task shortcuts)

### Setup

\```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies (including dev)
pip install -r requirements-dev.txt

# Start local database
docker compose up -d

# Run database migrations
python -m alembic upgrade head
\```

### Run

\```bash
# Development server with auto-reload
python -m uvicorn src.main:app --reload --port 8000

# Or via Make
make run
\```

### Test

\```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=term-missing

# Only unit tests (fast)
pytest -m "not integration"

# Only integration tests
pytest -m integration
\```

### Lint

\```bash
# Check
ruff check .

# Fix auto-fixable issues
ruff check . --fix

# Type checking
mypy src/
\```

## Deployment

Describe how to deploy:

\```bash
# Build
docker build -t project-name:latest .

# Deploy (example)
docker push registry.example.com/project-name:latest
\```

Environment variables required in production:

| Variable | Description | Required |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `REDIS_URL` | Redis connection string | Yes |
| `API_KEY` | External service API key | Yes |
| `LOG_LEVEL` | Logging level (default: INFO) | No |

## Contributing

1. Branch from `main` using the naming convention: `feature/description`, `fix/description`
2. Follow the [engineering standards](link-to-standards)
3. Write tests for new functionality
4. Submit a PR using the [PR template](.github/pull_request_template.md)
5. Get at least one review before merging

## License

MIT — see [LICENSE](LICENSE) for details.
```

---

## Usage Notes

- **Delete unused sections** — if the project has no deployment, remove that section
- **Keep Quick Start minimal** — 5 commands or fewer to go from clone to running
- **Architecture section scales** — simple projects need a sentence, complex ones need a diagram
- **Link, don't duplicate** — link to detailed docs instead of copying them into the README
- **Update on significant changes** — README should always reflect the current state
