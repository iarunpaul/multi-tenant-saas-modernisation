# REVIEW-ARC-0003 — Multi-Tenant Data Topology

## Metadata

```yaml
id: REVIEW-ARC-0003
type: architecture
skill: architecture-review
status: completed
date: 2026-10-14
reviewed-artifact: docs/architecture/ADRs/0001-multi-tenant-data-topology.md
platform-version: v0.2.0
protocol-version: "1"
target-sha256: 1850215454054dc8cb97e8544772372f607005516e1945013948ac8584b71f5d
input-fingerprint: 73443cf68fbbb6dc34278f0cca3bf51839cc08ac2ac8e2d9cdddd692e6089b63
rerun-of: REVIEW-ARC-0002
```

## Review Context

### Requirements

`docs/architecture/requirements.md`

### Requirements Review

`docs/reviews/grill/requirements/0001-multi-tenant-requirements.md`

### Parent Decisions

None identified. The reviewed ADR is the current topology decision; no separate parent ADR materially constrains it.

### Previous Architecture Reviews

- `docs/reviews/architecture/0001-multi-tenant-data-topology.md`
- `docs/reviews/architecture/0002-multi-tenant-data-topology.md`

### Review Target

`docs/architecture/ADRs/0001-multi-tenant-data-topology.md`

### Applicable Standards and Policies

- `.engineering/platform/standards/architecture/principles.md`
- `.engineering/platform/standards/engineering/development.md`
- `.engineering/platform/standards/security/secure-engineering.md`
- `.engineering/platform/standards/testing/testing-standard.md`
- `.engineering/platform/standards/observability/observability-standard.md`
- `.engineering/platform/standards/api/api-standard.md`
- `.engineering/platform/policies/quality-gates.md`
- `.engineering/platform/policies/secrets.md`
- `.engineering/platform/policies/human-approval.md`

The current review uses review-execution protocol v1 and the repository's `review_execution.py` tooling. The prior review predates that versioned manifest and used a different fingerprint method; the preparation tool therefore found no equivalent completed review. This explicit rerun preserves the prior artifact and links it here.

## Prior Finding Resolution

The target ADR has the same content hash as the target reviewed in `REVIEW-ARC-0002`; none of its findings is resolved by a target change.

| Prior Finding | Source | Resolution |
|---|---|---|
| Tenant directory availability, cache consistency, and unavailable/stale behavior are undefined. | `docs/reviews/architecture/0002-multi-tenant-data-topology.md` | DOES NOT RESOLVE — no target change defines availability objectives, cache/version behavior, or safe handling of unavailable or stale routing metadata. |
| Shard capacity and failure-domain limits are undefined. | `docs/reviews/architecture/0002-multi-tenant-data-topology.md` | DOES NOT RESOLVE — no measurable capacity or blast-radius limits are added. |
| Tenant-level recovery and deletion safety are unproven. | `docs/reviews/architecture/0002-multi-tenant-data-topology.md` | DOES NOT RESOLVE — the recovery workflow and prototype objectives remain unvalidated. |
| Cutover write fencing and the single-writer guarantee are unspecified. | `docs/reviews/architecture/0002-multi-tenant-data-topology.md` | DOES NOT RESOLVE — no fencing, request draining, or stale-route rejection mechanism is specified. |
| Placement thresholds and the performance acceptance profile are undefined. | `docs/reviews/architecture/0002-multi-tenant-data-topology.md` | DOES NOT RESOLVE — measurable promotion/demotion criteria and a repeatable workload profile remain absent. |
| Shared-schema isolation enforcement and administrative access boundaries remain open. | `docs/reviews/architecture/0002-multi-tenant-data-topology.md` | DOES NOT RESOLVE — the ADR still defers the concrete enforcement mechanism and does not define privileged operational controls. |
| Legacy backup scope and retirement conditions are unspecified. | `docs/reviews/architecture/0002-multi-tenant-data-topology.md` | DOES NOT RESOLVE — supported versions, import acceptance criteria, and retirement conditions remain undefined. |
| Tenant-identifier telemetry/cardinality controls are unspecified. | `docs/reviews/architecture/0002-multi-tenant-data-topology.md` | DOES NOT RESOLVE — access, retention, and cardinality controls are not added. |

## Purpose

Reassess whether the hybrid topology remains appropriate for the stated scale, workload skew, tenant isolation, migration, recovery, residency, availability, and cost drivers, and whether the ADR is sufficiently defined to proceed to detailed design.

## Architecture Summary

The ADR selects a hybrid topology: shared-schema tenant shards or pools for standard tenants, with dedicated shards or databases for exceptional workload, regulatory, or contractual needs. An authoritative tenant directory resolves placement. Tenant context must be validated and propagated across application and data paths. Tenant migration is incremental, with a point after which recovery must use forward reconciliation rather than unsafe routing rollback. Tenant-scoped restore, deletion reconciliation, regional placement, and legacy-backup import are identified as required capabilities.

## Architectural Drivers

- Growth from approximately 100,000 tenants to 250,000–300,000.
- Highly skewed workloads, including largest tenants peaking at 500–1,000 TPS and aggregate bursts near 30,000 TPS.
- Interactive latency and tiered availability targets.
- Isolation across tenant-scoped data paths, with dedicated placement for justified cases.
- Independent tenant recovery, with prototype RPO/RTO targets of 15 minutes/four hours.
- EU/EEA residency for primary, replica, backup, and recovery data.
- Incremental tenant migration with a five-minute final write-quiesce target.
- Reduced infrastructure cost and operational effort without unacceptable failure blast radius or noisy-neighbor impact.

## What Looks Sound

- The hybrid sharded-default topology addresses the documented workload skew and exceptional regulatory, contractual, and workload needs without requiring a dedicated database for every tenant.
- The ADR evaluates credible alternatives and gives relevant reasons not to use one global shared database or schema-per-tenant as the strategic default.
- The tenant directory is placement metadata, not a store for tenant business state.
- Tenant identity is not trusted merely because it was supplied by a client; loss of tenant context fails closed.
- Application filtering alone is explicitly insufficient, and defense in depth is required for shared-schema isolation.
- Residency requirements cover primary data, replicas, backups, and recovery copies.
- The migration point of no return rejects unsafe post-write routing rollback.
- The ADR distinguishes architecture direction from proof of production targets and defers unnecessary technology choices.

## Findings

### Finding 1

**Severity:** SIGNIFICANT  
**Finding:** The tenant directory is critical routing infrastructure, but its availability objective and behavior under outage, stale cache, or concurrent placement change remain unspecified.  
**Why it matters:** Directory unavailability can impair the data plane; stale placement can route operations to an obsolete location or undermine isolation during tenant movement.  
**Recommendation:** Define directory availability and recovery objectives, routing-version semantics, cache lifetime and invalidation, behavior when the directory is unreachable, and safe rejection of stale routes.

### Finding 2

**Severity:** SIGNIFICANT  
**Finding:** Shards are described as bounded failure domains, but the ADR does not define capacity limits or the maximum tenant population/workload exposed to one shard failure.  
**Why it matters:** Without measurable limits, shard failure or overload may affect more tenants than intended, and the scaling and isolation benefits cannot be sized or objectively tested.  
**Recommendation:** Establish measurable shard capacity and blast-radius limits, including storage, throughput, connection, and recovery constraints, and validate them with representative load and failure tests.

### Finding 3

**Severity:** SIGNIFICANT  
**Finding:** Tenant-level recovery and deletion safety have a plausible workflow but no demonstrated isolation or measured recovery evidence.  
**Why it matters:** A shared-shard restore can affect neighboring tenants, exceed prototype RPO/RTO targets, reintroduce deleted data, or violate residency constraints.  
**Recommendation:** Exercise tenant restore for shared and dedicated placements, including deletion-state reconciliation and residency enforcement; record measured RPO/RTO and prove neighboring tenant data is neither exposed nor changed.

### Finding 4

**Severity:** SIGNIFICANT  
**Finding:** The migration policy identifies quiescing and a point of no return, but does not define write fencing or precisely identify the authoritative writer between route switch and the first committed target write.  
**Why it matters:** In-flight requests, workers, or stale routes may continue writing to the legacy store after activation, causing divergent state or loss of acknowledged writes.  
**Recommendation:** Define how in-flight work is drained or fenced, how route generations advance, how old writers are rejected, and when the target is guaranteed to be the sole writer before accepting writes.

### Finding 5

**Severity:** SIGNIFICANT  
**Finding:** The online copy/catch-up and forward-reconciliation phases lack a consistency contract for ordering, duplicate handling, retry behavior, and validation before cutover.  
**Why it matters:** Even with a correctly fenced final cutover, missing, duplicated, or out-of-order changes during copy and catch-up can leave target data inconsistent with acknowledged source writes.  
**Recommendation:** In the migration design, define the change-capture/catch-up ordering and checkpoint model, idempotency and duplicate handling, reconciliation rules, and cutover validation criteria; test partial failure and retry scenarios.

### Finding 6

**Severity:** SIGNIFICANT  
**Finding:** Workload-based promotion and shard sizing cannot be validated because placement thresholds and the performance acceptance workload are not specified.  
**Why it matters:** Aggregate TPS and latency targets do not define transaction mix, burst duration, concurrency, tenant distribution, or the point at which a tenant is promoted or throttled.  
**Recommendation:** Define a repeatable workload profile and measurable promotion/demotion criteria before production sizing or automated placement; test aggregate load and hot-tenant interference against them.

### Finding 7

**Severity:** SIGNIFICANT  
**Finding:** The ADR requires defense in depth for shared-schema isolation but leaves enforcement mechanisms and administrative access boundaries to subsequent design.  
**Why it matters:** Tenant isolation is a core security requirement; tenant-aware query abstractions without enforceable controls and verification can leave cross-tenant access dependent on application correctness.  
**Recommendation:** Before production implementation, select and verify applicable database, data-access, authorization, and administrative controls, and require automated negative tests that demonstrate cross-tenant reads and writes are denied.

### Finding 8

**Severity:** MINOR  
**Finding:** Legacy backup compatibility is called transitional, but supported backup versions, validation/import acceptance criteria, and retirement conditions remain undecided.  
**Why it matters:** An unbounded compatibility path can become a permanent maintenance and security obligation or fail to support the intended migration population.  
**Recommendation:** Set the supported-version window, integrity checks, import acceptance criteria, and retirement trigger before migration rollout.

### Finding 9

**Severity:** MINOR  
**Finding:** Tenant-aware telemetry is required, but controls for tenant identifiers in logs, metrics, and traces—including access, retention, and metric cardinality—are not defined.  
**Why it matters:** Tenant-level diagnostics can expose sensitive operational context, while high-cardinality dimensions can undermine observability cost and usability.  
**Recommendation:** Define authorized use, redaction, retention, and cardinality rules for tenant identifiers; prefer controlled correlation or support workflows over unrestricted metric dimensions.

## Standards Compliance

- **Architecture principles — PARTIALLY COMPLIANT:** The topology is justified by stated scale, workload skew, isolation, recovery, and residency needs, and its complexity is acknowledged. Critical failure, capacity, consistency, and cutover behavior remain unresolved.
- **Secure engineering — PARTIALLY COMPLIANT:** Tenant identity validation, fail-closed context handling, and defense in depth are stated. Concrete isolation enforcement and privileged administrative boundaries remain unresolved.
- **Testing standard — PARTIALLY COMPLIANT:** Recovery, load, noisy-neighbor, and migration validation are recognized, but complete acceptance profiles and evidence are absent.
- **Observability standard — PARTIALLY COMPLIANT:** Tenant-context propagation and migration observability are addressed; directory/shard health objectives and tenant identifier/cardinality controls remain open.
- **API standard — PARTIALLY COMPLIANT:** Compatibility is an accepted requirement, but an explicit API/event contract inventory and automated compatibility verification are not specified in this ADR.
- **Quality gates policy — PARTIALLY COMPLIANT:** Relevant tenant-boundary and verification needs are identified, but they are not mapped to mandatory automated gates.
- **Secrets policy — COMPLIANT:** No secrets are specified; implementation identity and secret-management details remain subject to applicable controls.
- **Human approval policy — COMPLIANT:** The ADR remains proposed and does not claim to authorize production, destructive migration, or external-contract changes.

## Alternatives Worth Considering

The hybrid model, with a bounded shard/pool default and dedicated exceptions, remains a credible balance for the stated drivers. A global shared database and schema-per-tenant are rejected with relevant recovery, blast-radius, and scale reasoning. No materially simpler topology is evident that meets the same combination of workload isolation, recovery, residency, and tenant-count goals; retain the simpler sharded-pool default unless evidence justifies additional placement classes.

## Required Decisions

- Directory availability, cache/version consistency, and stale-routing behavior.
- Shard capacity and acceptable failure/overload blast radius.
- Tenant promotion/demotion thresholds and repeatable workload acceptance profile.
- Shared-schema isolation enforcement and privileged administrative access.
- Copy/catch-up ordering, checkpoints, retries, idempotency, reconciliation, and cutover validation.
- Cutover fencing, in-flight operation handling, and the single-writer guarantee.
- Recovery proof for tenant isolation, deletion replay, residency, RPO, and RTO.
- Supported legacy backup versions, validation criteria, and retirement conditions.
- Tenant identifier access, retention, and telemetry cardinality controls.

## Conditions

1. Keep the ADR proposed until the authorized decision owner accepts the topology.
2. Resolve directory failure/stale-route semantics, shared-schema isolation controls, and migration fencing before production migration or implementation.
3. Define shard capacity, workload profiles, and placement thresholds, then validate throughput, latency, noisy-neighbor behavior, and failure blast radius.
4. Define and test the online-copy/catch-up consistency contract, including retry and partial-failure behavior, before production migration.
5. Demonstrate tenant-level recovery for shared and dedicated placements, including deletion safety, residency, and measured RPO/RTO, before production adoption.
6. Define the legacy-backup support window and tenant telemetry privacy/cardinality controls before operational rollout.
7. Treat cost, provisioning, schema rollout, and manual-intervention targets as hypotheses until measured against current baselines.

## Recommendation

```text
APPROVE WITH CONDITIONS
```

The hybrid sharded-default direction is justified by the requirements and remains appropriate to advance into focused detailed design. This approval is limited to the architecture direction; it is not approval for production implementation or migration. The significant findings and conditions above must be resolved or validated at the appropriate design and production-readiness gates.

## Remaining Risks

- Directory outage or stale placement may impair availability or route work incorrectly.
- Unbounded shard sizing may defeat intended failure containment.
- Unproven migration consistency or unfenced cutover may leave divergent authoritative writes.
- Recovery may miss RPO/RTO targets, affect neighboring tenants, resurrect deleted data, or breach residency.
- Unverified isolation controls may permit cross-tenant access.
- Cost and operational-effort targets remain unproven until measured.

## Next Engineering Activity

Continue detailed design for the tenant directory/control plane, shared-shard isolation, migration copy/catch-up and fencing/reconciliation, and tenant-level recovery. Define a repeatable workload and failure-test profile, then update the ADR with decisions and evidence before production implementation.

## Suggested Skill Handoff

```text
architecture-review
    ↓
resolve significant findings in detailed architecture decisions
    ↓
accept ADR-0001 with the authorized decision owner
    ↓
implementation-plan
    ↓
grill implementation-plan
    ↓
security-review and production-readiness before production adoption
```

## Evidence

This document records the completed architecture review and may be referenced as evidence for architecture-governance controls.

This review does not replace an ADR. The ADR records the architecture decision; this document records the independent review of that decision.
