# ARI V1 — Agricultural Intelligence Platform

ARI V1 uses one backend, one database architecture, one mobile app, one web app, one domain model, and one RBAC system.

---

## Architecture Rules

- One FastAPI backend
- One PostgreSQL / TimescaleDB database
- One Flutter mobile app (Android + iOS only)
- One browser-based Web App
- One RBAC system
- No apps/ structure — roots are backend/, mobile/, web/

**Do not add:** permission service, QR registry, consultation entity, farm membership table, knowledge graph, vector database, RAG, internal AI assistant, robot module, commerce module, desktop app.

---

## Local Prerequisites

- Git
- Docker
- Docker Compose
- curl

---

## Local Startup

```bash
git clone <repo-url> ari
cd ari

cp .env.example .env

docker compose up -d --build

curl http://localhost:8000/health
curl http://localhost:8000/api/v1/health
```

---

## Service URLs

| Service           | URL                          |
|-------------------|------------------------------|
| Backend API       | http://localhost:8000        |
| Root Health       | http://localhost:8000/health |
| API v1 Health     | http://localhost:8000/api/v1/health |
| PostgreSQL        | localhost:5432               |
| MinIO API         | http://localhost:9000        |
| MinIO Console     | http://localhost:9001        |
| EMQX MQTT         | localhost:1883               |
| EMQX Dashboard    | http://localhost:18083       |

---

## Local Shutdown

```bash
# Stop, preserve volumes
docker compose down

# Stop and remove all local data volumes (clean reset)
docker compose down -v
```

---

## What P2-2 Includes

- Monorepo root structure
- FastAPI backend skeleton with health endpoints
- Docker Compose local stack (api, postgres, minio, emqx)
- `.env.example` template
- AI coding agent guardrails (AGENTS.md, CLAUDE.md, CODEX.md)
- docs/ and scripts/ scaffolding

## What P2-2 Does Not Include

- Auth, JWT, phone registration/login
- Database schema migrations
- Farm / Zone / Tree APIs
- Notebook / Note Item / Follow-Up APIs
- File upload / sync
- Mobile screens
- Web pages
- Production deployment

See [docs/execution/P2-2_Monorepo.md](docs/execution/P2-2_Monorepo.md) for full scope.

---

## Forbidden Services

`docker compose ps` must NOT include: worker, permission-service, ai-service, rag-service, vector-db, robot-service, commerce-service, admin-backend, web-backend.
