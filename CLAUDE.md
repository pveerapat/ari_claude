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

## Claude-Specific Guardrails

Do not infer missing ARI architecture.
Do not create services because they seem useful.
Do not convert consultation into a separate entity.
Do not convert QR into a registry.
Do not add RBAC guards, middleware, or role checks not in the frozen spec.
Do not add background workers, queues, or schedulers.
Do not create any module that is explicitly deferred in P2-2 section 5.2.

If a required detail is unclear, create a API Gap / Revision Proposal in docs/api-gaps/ — do not implement a guess.
