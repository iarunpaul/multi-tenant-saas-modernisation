# Multi-Tenant SaaS Modernisation

This repository uses the Agentic Engineering Platform.

Platform assets are installed under:

```text
.engineering/platform/
```

The configured platform version is defined in:

```text
.engineering/platform.yaml
```

## Repository Guidance

Before substantial engineering work:

1. read the applicable standards under `.engineering/platform/standards/`
2. read applicable policies under `.engineering/platform/policies/`
3. use relevant skills under `.engineering/platform/skills/`
4. inspect decisions under `docs/decisions/`
5. follow project-specific architecture requirements

## Project Context

This repository demonstrates the modernisation of a large-scale database-per-tenant SaaS platform into a secure and scalable multi-tenant architecture.

## Architecture Workflow

For material architecture work use:

```text
grill
  ↓
architecture decision
  ↓
architecture-review
  ↓
implement
  ↓
test
  ↓
security-review
  ↓
production-readiness
```

Platform policies and standards take precedence over project-specific agent guidance.