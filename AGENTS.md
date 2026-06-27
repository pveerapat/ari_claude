NO MAGIC
VERIFY BEFORE DONE
DISSENT
SCOPE DRIFT
R0/R1/R2

Do not redesign ARI.
Do not add new architecture.
Do not add new database tables.
Do not add new RBAC roles.
Do not create QR registry.
Do not create consultation entity.
Do not create farm_memberships.
Do not create permission service.
Do not create knowledge graph.
Do not create vector database.
Do not create RAG system.
Do not create internal AI assistant.
Do not create robot module.
Do not create commerce module.
Follow ARI V1 — P2-1 and P2-2.
If something is missing, mark API Gap / Revision Proposal.

---

## Project Rules

ARI V1 uses one backend, one database architecture, one mobile app, one web app, one domain model, and one RBAC system.

## Source of Truth Order

1. P0 Domain Model Specification v1.0 + v1.1
2. P0 Database Schema Specification v1.0 + v1.1
3. P0 API Specification v1.0 + v1.1
4. P1-1 Backend Implementation Specification v1.0
5. P1-2 Mobile App Implementation Specification v1.0
6. P1-3 Web App Implementation Specification v1.0
7. P2-1 Coding Execution Plan v1.0 (FROZEN)
8. P2-2 Monorepo & Local Development Setup v1.0 (FROZEN)

## Allowed P2-2 Files

- backend/app/main.py, core/config.py, api/v1/health.py, api/v1/router.py
- backend/app/db/base.py, backend/app/db/session.py
- backend/Dockerfile, backend/pyproject.toml, backend/alembic.ini
- docker-compose.yml, .env.example, .gitignore
- README.md, AGENTS.md, CLAUDE.md, CODEX.md
- mobile/README.md, web/README.md, infra/, docs/, scripts/

## Forbidden Files

- backend/app/api/v1/auth.py
- backend/app/api/v1/users.py, farms.py, zones.py, trees.py
- backend/app/api/v1/notebook_entries.py, note_items.py, follow_ups.py
- backend/app/api/v1/notifications.py, upload_queue.py, files.py, sync.py
- backend/app/models/, schemas/, repositories/, services/
- Any forbidden service: permission_service, qr_registry_service, consultation_service

## How to Handle Missing Specs

Do not infer or invent missing implementation. Create an API Gap note in docs/api-gaps/ using the template in P2-2 section 36.4.

## Smoke Test

Before marking any task done:
- curl http://localhost:8000/health returns {"status":"ok","service":"ari-backend","api":"/api/v1"}
- curl http://localhost:8000/api/v1/health returns the same
- docker compose ps shows only: api, postgres, minio, emqx
