# How to run

## Minimal stacks

### Postgres
```bash
cp infra/env/.env.example infra/env/.env
make up STACK=postgres
make smoke STACK=postgres
make down STACK=postgres

**`/docs/stacks/stacks-matrix.md`**
```md
# Stacks Matrix (draft)

| Module | Topic | Minimal stack |
|-------:|-------|---------------|
| 00 | API -> Postgres ingestion | postgres (+ jupyter later) |
