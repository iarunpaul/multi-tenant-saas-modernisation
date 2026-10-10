# Production Readiness

## Purpose

Determine whether a service, system or significant change can be operated safely and reliably in production.

Production readiness covers more than successful deployment.

## When to Use

Use before:

- first production launch
- major releases
- material infrastructure changes
- migration cutovers
- significant architectural changes

## Workflow

### 1. Deployment

Confirm:

- deployment is repeatable
- configuration is externalised appropriately
- secrets are handled securely
- environments are understood
- required migrations are defined

### 2. Rollback and Recovery

Determine:

- whether rollback is possible
- whether data changes are reversible
- whether roll-forward is preferable
- what happens after partial deployment failure

### 3. Observability

Confirm relevant:

- logs
- metrics
- traces
- dashboards
- alerts

exist or are planned.

Signals should enable detection and diagnosis of material failure.

### 4. Reliability

Review:

- dependency failures
- timeouts
- retries
- resilience
- capacity
- graceful degradation
- recovery

### 5. Data Safety

Review:

- migrations
- backup
- restore
- retention
- corruption scenarios
- reconciliation where relevant

### 6. Security

Confirm required security review and automated controls have completed.

### 7. Operational Ownership

Determine:

- who owns the service
- who responds to incidents
- how escalation works
- what operational documentation is necessary

### 8. Service Objectives

For material services identify relevant:

- availability targets
- latency targets
- capacity expectations
- recovery objectives

Do not invent SLOs without business justification.

### 9. Change Safety

Assess:

- blast radius
- staged rollout
- feature flags
- canary or progressive delivery
- compatibility
- monitoring during release

Use only where justified.

### 10. Human Approval

Identify any required approval before production action.

## Output

### Readiness Summary

Brief overall assessment.

### Blocking Gaps

Issues that prevent safe production use.

### Significant Risks

Important but potentially acceptable risks.

### Operational Evidence

Summarise:

- deployment validation
- observability
- recovery
- security
- tests
- operational ownership

### Recommendation

Conclude:

```text
READY
READY WITH CONDITIONS
NOT READY
```

### Required Approval

Clearly identify human approval still required.

## Behaviour Rules

Do not:

- equate CI success with production readiness
- require enterprise-scale operational machinery for trivial systems
- approve irreversible production changes without appropriate recovery planning
- claim rollback capability without validating the underlying assumptions
