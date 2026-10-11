# GRILL-0001 — Multi-Tenant SaaS Modernisation Requirements

## Status

Completed

## Review Type

```text
requirement
```

## Reviewed Artifact

```text
docs/architecture/requirements.md
```

## Purpose

Challenge the requirements for modernising the existing database-per-tenant SaaS platform before selecting a target architecture.

The review focused on identifying material unknowns, validating architecture drivers, surfacing hidden assumptions, and determining whether architecture design could safely proceed.

---

## Outcome

The requirements provide a sufficient basis to proceed to architecture design, subject to several conditions.

The modernisation must reduce operating cost and operational complexity while preserving:

- tenant isolation
- recovery
- availability
- migration safety
- residency requirements
- customer-visible backup and restore behaviour

The requirements intentionally do not prescribe a target database topology.

---

## Confirmed Facts

### Tenant Scale

```text
Current tenants:
~100,000

3–5 year target:
250,000–300,000
```

Tenant workloads are highly skewed.

Most tenants are expected to be small or medium sized, while a smaller number of large tenants may generate disproportionately high transaction, storage and integration loads.

### Workload

```text
Aggregate sustained throughput:
10,000–20,000 TPS

Short bursts:
~30,000 TPS

Largest tenants:
500–1,000 TPS peak
```

Interactive API targets:

```text
P95 < 300 ms
P99 < 750 ms
```

### Tenant Isolation

Shared infrastructure is acceptable for standard tenants where strong logical isolation can be enforced.

Dedicated databases are required or permitted for selected tenants based on:

- regulatory requirements
- contractual isolation requirements
- workload thresholds
- explicit commercial isolation tiers

Customer preference alone does not automatically imply dedicated placement.

### Migration

Migration must be incremental and tenant-specific.

Bulk copy and catch-up should occur while the tenant remains online where practical.

Final cutover may briefly quiesce writes.

Target maximum write downtime:

```text
5 minutes
```

Migration requires:

- validation before cutover
- rollback before activation
- explicit handling of partial failure
- observable migration state

### Recovery

Independent tenant recovery is required.

Prototype targets:

```text
RPO: 15 minutes
RTO: 4 hours
```

for standard tenants.

### Availability

```text
Standard tenants:
99.95%

Higher service tiers:
99.99% where justified
```

Routine deployments and schema changes should avoid platform-wide downtime.

### Residency

GDPR and EU/EEA residency form the initial regulatory baseline.

Tenant placement must support regional restrictions.

Primary data, replicas, backups and recovery copies must respect the tenant's permitted geography.

Other regulatory regimes and regions remain later-validation items.

### Data Retention and Deletion

Prototype targets:

```text
Active production deletion:
<= 30 days

Standard backup retention:
35 days
```

Deleted data may remain temporarily in immutable backups but must not return to active processing after restore.

Restore workflows must preserve deletion state.

### Cross-Tenant Analytics

Operational telemetry may contain tenant identifiers where required for authorised operational use.

Cross-tenant business analytics should use:

```text
aggregated
or
de-identified
```

data by default.

### Backup Compatibility

Backward compatibility refers to preserving customer-visible recovery capability.

The modernised platform does not need to retain the legacy database backup format internally.

Legacy backups require a supported transitional import/recovery path during migration.

---

## Prototype Targets / Accepted Assumptions

The following are working targets rather than validated production baselines:

```text
>= 40% reduction in infrastructure/database operating cost per tenant

new tenant provisioning:
< 5 minutes

shared/sharded schema rollout:
< 2 hours

manual database-related operational intervention:
>= 60% reduction
```

These values must be validated against real operational baselines before production adoption.

Other currently accepted assumptions include:

- workload distribution remains highly skewed
- higher service tiers may need stronger recovery targets
- GDPR/EU residency is sufficient for the initial prototype
- existing external contracts can be preserved during migration

---

## Critical Challenges

### 1. Migration Rollback Contract

**Severity:** BLOCKER

The migration design must define the exact point at which the target data store becomes authoritative.

A simple routing rollback after the target has accepted new writes could lose or duplicate acknowledged transactions.

Required decision:

```text
When does rollback stop being safe,
and what happens to writes accepted after cutover?
```

---

### 2. Tenant Placement Policy

**Severity:** SIGNIFICANT

Dedicated placement cannot rely on subjective decisions.

The architecture must eventually define measurable criteria for:

- workload thresholds
- regulatory placement
- contractual isolation
- promotion
- demotion
- tenant movement

---

### 3. Tenant-Level Recovery

**Severity:** SIGNIFICANT

Candidate architectures must demonstrate that one tenant can be restored independently without:

- reverting other tenants
- exposing other tenant data
- resurrecting deleted data
- violating residency policy

The stated RPO/RTO must be proven rather than assumed.

---

### 4. Performance Acceptance Model

**Severity:** SIGNIFICANT

The throughput and latency targets require a repeatable workload definition.

Still required:

- transaction mix
- read/write ratio
- burst duration
- concurrency profile
- workload distribution
- acceptance-test methodology

---

### 5. Residency Enforcement

**Severity:** SIGNIFICANT

The architecture requires an enforceable placement model covering:

- primary data
- replicas
- backups
- disaster recovery
- tenant migration

Region placement must not depend on application convention alone.

---

### 6. Legacy Backup Transition

**Severity:** SIGNIFICANT

The transitional compatibility mechanism must define:

- supported legacy backup versions
- validation process
- transformation/import process
- support lifetime
- retirement criteria

---

## Important Failure Scenarios

The architecture must explicitly address:

```text
tenant context missing or forged

cross-tenant query or cache access

hot tenant exhausting shared capacity

partial tenant migration

post-cutover migration failure

tenant restore affecting neighbouring tenants

deleted data reappearing after restore

regional failover violating residency

partial schema rollout

stale tenant-routing metadata
```

---

## Complexity Assessment

```text
appropriately simple
```

The requirements justify evaluating shared, sharded and dedicated placement models.

They do not yet justify:

- microservices
- Kubernetes
- service mesh
- event sourcing
- CQRS
- distributed transactions
- globally distributed databases

Any such complexity must be justified later by a specific architecture driver.

---

## Decisions Required

| Severity | Decision |
|---|---|
| BLOCKER | Define migration rollback and point-of-no-return semantics |
| SIGNIFICANT | Define tenant placement and promotion policy |
| SIGNIFICANT | Prove tenant-level recovery model |
| SIGNIFICANT | Define performance acceptance workload |
| SIGNIFICANT | Define availability and residency operational boundaries |
| SIGNIFICANT | Define legacy-backup transition policy |
| SIGNIFICANT | Select target tenancy topology |

---

## Recommendation

```text
PROCEED WITH CONDITIONS
```

Proceed to architecture option analysis and ADR creation using the current values as explicit prototype assumptions.

Do not begin production-oriented migration implementation until the migration rollback contract, placement policy, recovery proof and measurable performance acceptance criteria are resolved.

Production adoption additionally requires validation against real operational baselines.

---

## Resolution of Requirement-Stage Blocker

The migration rollback contract is adopted as the working architecture rule:

```text
Before cutover:
rollback to the legacy database is permitted.

During final quiesce:
writes are not accepted.

After routing switches:
the target store becomes the candidate system of record.

After the first successful committed write on the target:
routing back to the legacy database is not considered a safe rollback.

From that point:
recovery uses reconciliation or forward-fix rather than destructive rollback.
```

This removes the requirement-stage blocker sufficiently to proceed with topology design.

The migration implementation will require a more detailed state machine and reconciliation design later.

---

## Next Engineering Activity

Create:

```text
docs/decisions/0001-multi-tenant-data-topology.md
```

Compare:

```text
Database per tenant
Shared database / shared schema
Shared database / schema per tenant
Tenant shards / database pools
Hybrid tenancy
```

against the confirmed architecture drivers.

After the ADR:

```text
architecture-review
        ↓
resolve architecture findings
        ↓
implementation-plan
        ↓
grill implementation-plan
```

---

## Evidence

This document records the outcome of the requirements Grill and may be referenced as architecture-governance evidence for:

```text
ARC-001 — Grill Review
```

It is not itself an architecture decision.

Architecture decisions resulting from this review must be recorded separately as ADRs.
