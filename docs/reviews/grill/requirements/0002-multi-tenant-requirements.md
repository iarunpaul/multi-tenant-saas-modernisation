# GRILL-0002 — Multi-Tenant SaaS Modernisation Requirements

## Metadata

```yaml
id: REVIEW-REQ-0002
type: requirement
skill: grill
status: completed
date: 2026-10-14
reviewed-artifact: docs/architecture/requirements.md
platform-version: v0.2.1
protocol-version: "1"
execution-mode: canonical
target-sha256: f5912d5217c136493a4eda96883ba14f1cc2dab94368da029bbcce48cca982f1
input-fingerprint: 0c0410529f71f713b4c616766f98396a3f5a9f048d4b6307d7fb0587d497cbd4
```

## Review Context

### Review Target

`docs/architecture/requirements.md`

### Material Context

- `docs/architecture/ADRs/0001-multi-tenant-data-topology.md`
- `.engineering/platform/standards/architecture/principles.md`
- `.engineering/platform/standards/security/secure-engineering.md`
- `.engineering/platform/standards/testing/testing-standard.md`
- `.engineering/platform/standards/observability/observability-standard.md`
- `.engineering/platform/standards/api/api-standard.md`
- `.engineering/platform/policies/quality-gates.md`

The earlier review, `docs/reviews/grill/requirements/0001-multi-tenant-requirements.md`, was consulted as same-target review history. It predates canonical review protocol metadata and was not included in the fingerprint manifest.

## Purpose

Challenge whether the requirements for modernising the database-per-tenant SaaS platform are sufficiently clear, testable, and current to guide detailed architecture and eventual implementation without prescribing unnecessary technology.

## Outcome

The requirements establish a coherent modernization goal: reduce tenant-database operating burden and cost while preserving isolation, availability, recovery, residency, and migration safety. The target topology has since been documented as a proposed hybrid, sharded-default model in ADR-0001.

The requirements are adequate to continue detailed design using the prototype assumptions recorded in the prior Grill. They are not yet an evidence-backed acceptance baseline for production sizing or rollout. The document's status section is stale relative to the current repository state and should be updated.

## Confirmed Facts

The prior requirements Grill recorded the following as confirmed facts; this review does not independently validate them against operational data:

- Current estate of approximately 100,000 tenants, with 250,000–300,000 expected over three to five years.
- Highly skewed tenant workloads.
- Aggregate sustained throughput of 10,000–20,000 TPS, short bursts near 30,000 TPS, and largest-tenant peaks of 500–1,000 TPS.
- Interactive API targets of P95 below 300 ms and P99 below 750 ms.
- Availability targets of 99.95% for standard tenants and 99.99% for higher tiers where justified.
- Tenant-level restore is required, with prototype RPO/RTO of 15 minutes/four hours for standard tenants.
- Migration is tenant-by-tenant, with online copy/catch-up where practical and a five-minute maximum final write-quiesce target.
- EU/EEA residency is the initial baseline, including primary data, replicas, backups, and recovery copies.
- Active deletion has a prototype target of 30 days and standard backup retention is assumed to be 35 days.
- Customer-visible backup and restore capability must be retained; legacy backup formats require a transitional import/recovery path.

## Accepted Assumptions

- The figures above are working inputs for architecture exploration; they are not proven production capacity targets or service commitments.
- Workload remains highly skewed, and a small number of tenants may require promotion, throttling, or isolation.
- EU/EEA residency is sufficient for the initial prototype; other regions and regulatory regimes will be assessed later.
- Higher service tiers may need stronger recovery objectives.
- Existing external contracts can be preserved during migration, but the contract inventory has not yet been evidenced.
- The ADR's hybrid sharded-default direction is proposed, not yet an accepted production decision.

## What Looks Sound

- The requirements separate business outcomes and quality attributes from the target technology.
- Tenant isolation is treated as an end-to-end boundary across authentication, data, caches, messaging, background work, telemetry, recovery, and administration.
- The target recognizes non-uniform workloads, tenant mobility, noisy-neighbor risks, and the need for distinct placement classes.
- Migration is explicitly incremental, with validation, partial-failure handling, reconciliation, observability, and rollback/recovery concerns.
- Recovery includes deletion-state preservation and residency rather than treating backup restoration as an isolated database operation.
- The requirements explicitly reject introducing distributed-system patterns without a measurable driver.
- The previous Grill resolved the initial rollback ambiguity sufficiently to proceed to topology analysis while retaining implementation-level fencing and reconciliation as follow-up work.

## Critical Challenges

### 1. Requirement status no longer reflects repository state

**Issue:** The requirements still state that the next activity is requirements Grill and that no architecture decision has been made, while ADR-0001 now documents a proposed topology and has completed architecture reviews.  
**Why it matters:** Readers cannot tell whether the requirements are pre-decision inputs, current acceptance criteria, or an obsolete discovery artifact. The ADR also depends on them as its driver baseline.  
**Question or evidence required:** Update the status and next activity to state that the hybrid topology is proposed, decision-owner acceptance is pending, and detailed design/validation remain.  
**Potential consequence:** Teams may repeat completed discovery or treat an unaccepted proposal as an approved decision.

### 2. Quantitative targets lack workload definitions and evidence ownership

**Issue:** The prior Grill records precise tenant, throughput, latency, and availability figures, but the requirements document itself does not define their provenance, workload mix, measurement window, or accountable owner.  
**Why it matters:** TPS and latency targets cannot drive shard sizing or objective acceptance without transaction mix, read/write ratio, burst duration, concurrency, tenant distribution, and measurement conditions.  
**Question or evidence required:** For each target, identify its source/baseline, owner, measurement method, workload profile, and whether it is a prototype objective, launch criterion, or contractual SLO.  
**Potential consequence:** Architecture sizing and production readiness may be judged against ambiguous or unattainable numbers.

### 3. Isolation requirements need testable acceptance criteria

**Issue:** Isolation principles are broad, but the requirements do not define the evidence required to demonstrate that cross-tenant access is prevented, including privileged support and administrative access.  
**Why it matters:** Shared-schema tenancy makes isolation defects high-impact, and application filtering alone is explicitly insufficient.  
**Question or evidence required:** Define the isolation test boundary and acceptance evidence for tenant-scoped reads/writes, cache keys, asynchronous work, restore workflows, and privileged access; leave implementation mechanisms to detailed design.  
**Potential consequence:** The topology could be implemented without objective proof of its primary security constraint.

### 4. Residency and regulatory scope is only an initial assumption

**Issue:** EU/EEA is the prototype baseline, while exact applicable regimes and contractual obligations remain unconfirmed.  
**Why it matters:** Requirements for replicas, backups, recovery, support access, and tenant movement may differ across customers and can alter placement and recovery design.  
**Question or evidence required:** Identify the owner and trigger for validating jurisdiction-specific and contractual requirements before each production region or tenant cohort is onboarded.  
**Potential consequence:** A technically correct regional placement may still violate an unrecorded legal or contractual obligation.

### 5. Backup compatibility and deletion obligations lack bounded acceptance

**Issue:** The requirements preserve customer-visible recovery and require a transitional legacy-backup path, but do not state the supported format/version set, integrity criteria, support lifetime, or how deletion obligations interact with immutable backup retention.  
**Why it matters:** Restore can fail for legacy customers or reintroduce deleted data; indefinite format support also creates ongoing security and maintenance obligations.  
**Question or evidence required:** Define the compatibility window, restore integrity checks, deletion replay evidence, retention exceptions, and retirement owner before migration rollout.  
**Potential consequence:** Customer recovery commitments or deletion/residency obligations may not be met.

## Hidden Assumptions

- Tenant counts and workload projections remain representative over the chosen planning horizon.
- Aggregate and per-tenant peak TPS figures can occur concurrently in the expected tenant distribution.
- Customer-facing backup behavior can be preserved even when its internal format changes.
- A five-minute write-quiesce window is achievable for tenants with the largest data volumes and highest change rates.
- The cost-reduction and operational-effort targets can be measured consistently against current-state baselines.
- “Dedicated database,” “dedicated shard,” and “dedicated infrastructure” represent distinct, governed service levels.

## Missing Non-Functional Requirements

- A repeatable workload specification and acceptance method for latency, throughput, burst, and noisy-neighbor tests.
- A target population and workload limit per shard, plus an acceptable shard failure/overload blast radius.
- Directory/control-plane availability, recovery, and stale-route behavior objectives.
- Recovery acceptance criteria for tenant isolation, deletion preservation, residency, and measured RPO/RTO.
- Isolation acceptance tests and administrative-access controls.
- A defined measurement/ownership model for availability and the higher service tier.
- Tenant-identifying telemetry access, retention, redaction, and cardinality rules.
- Baseline and calculation method for cost, provisioning, schema rollout, and manual-intervention improvement targets.

## Failure Scenarios

- Stale tenant placement routes requests or background work to a previous shard during movement.
- A hot tenant exhausts shared capacity and degrades unrelated tenants.
- Migration catch-up loses, duplicates, or reorders writes before cutover.
- A stale worker continues writing to the legacy store after the target becomes authoritative.
- Tenant restore affects neighboring data or resurrects data deleted after the backup.
- Recovery replicas or backups violate a tenant's permitted geography.
- Privileged support access bypasses normal tenant-context checks.
- A regional or directory outage prevents tenant resolution or recovery within service objectives.

## Complexity Check

```text
appropriately simple
```

The requirements justify comparing pooled/sharded and dedicated placement models because tenant count, workload skew, isolation, residency, and recovery all materially constrain the solution. They do not justify selecting microservices, Kubernetes, event sourcing, CQRS, distributed transactions, or active-active multi-region operation without further evidence.

## Decisions Required

| Severity | Decision |
|---|---|
| SIGNIFICANT | Refresh requirement status to match the proposed ADR and current engineering phase. |
| SIGNIFICANT | Assign owners and provenance to quantitative targets; define workload and measurement criteria before production sizing. |
| SIGNIFICANT | Define tenant-isolation acceptance evidence and privileged-access requirements before production implementation. |
| SIGNIFICANT | Establish regulatory/contractual validation ownership and regional onboarding gates. |
| SIGNIFICANT | Bound legacy backup support and specify recovery/deletion acceptance criteria before migration rollout. |
| MINOR | Define baseline methodology for cost, provisioning, schema rollout, and intervention-reduction goals. |
| MINOR | Define tenant telemetry access, retention, and cardinality requirements before operational rollout. |

## Recommendation

```text
PROCEED WITH CONDITIONS
```

The requirements provide a sufficient directional baseline for detailed design, supported by the prior Grill's accepted prototype assumptions. They are not yet a complete production acceptance contract. Update the stale status and resolve the significant decisions at the stated design and rollout gates; validate unverified figures before using them as production capacity or service commitments.

## Conditions

1. Update the requirements' current phase and next activity to reflect ADR-0001 as a proposed, not yet accepted, direction.
2. Preserve prototype targets as assumptions until their source, owner, workload profile, and measurement method are established.
3. Define tenant-isolation and recovery proof obligations before production implementation.
4. Validate the applicable regulatory and contractual scope before onboarding tenants in each region.
5. Bound legacy backup support and verify deletion-safe restore behavior before migration rollout.
6. Establish baselines for the cost and operational-effort success criteria before claiming those outcomes.

## Resolved During Grill

- The earlier Grill recorded a working tenant scale and workload profile, availability objectives, EU/EEA prototype scope, tenant-level recovery objective, migration downtime target, deletion target, and backup-retention assumption.
- The earlier Grill established the working migration point-of-no-return rule: rollback is permitted before target writes; after the target accepts a committed write, recovery must reconcile or move forward rather than blindly route back.
- These values and rules are carried forward as review history; they have not been independently revalidated in this review.

## Remaining Follow-Up

- Confirm source data and owners for scale, workload, latency, and availability objectives.
- Define workload acceptance, shard/failure-domain limits, and placement thresholds during detailed architecture design.
- Specify directory behavior, migration fencing/consistency, shared-schema isolation enforcement, and tenant-level recovery in the relevant follow-up decisions.
- Confirm regional/commercial obligations and legacy-backup support boundaries before production rollout.

## Next Engineering Activity

Update the requirements status and traceability for the accepted/proposed architecture direction, then continue the follow-up detailed design and validation work identified in ADR-0001. Keep prototype values visibly separate from approved production SLOs.

## Suggested Skill Handoff

```text
grill — requirements
    ↓
update requirements status and target traceability
    ↓
architecture-review / detailed architecture decisions
    ↓
grill — implementation plan
    ↓
security-review and production-readiness before production adoption
```

## Evidence

This document records the completed Grill review and may be referenced as architecture-governance evidence.

Execution semantics are defined by Review Execution Protocol v1 and the recorded canonical execution mode.

This review records analysis of the requirements; it does not replace an ADR.
