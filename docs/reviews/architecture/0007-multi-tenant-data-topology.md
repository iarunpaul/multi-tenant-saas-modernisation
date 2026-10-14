# REVIEW-ARC-0007 — Multi-Tenant Data Topology

## Metadata

```yaml
id: REVIEW-ARC-0007
type: architecture
skill: architecture-review
status: completed
date: 2026-10-14
reviewed-artifact: docs/architecture/ADRs/0001-multi-tenant-data-topology.md
platform-version: v0.2.1
protocol-version: "1"
execution-mode: canonical
target-sha256: 81ee0abeea883b5fd4cbf55926ac7765adbab253dd7329aee953c32e97b14c00
input-fingerprint: 5a14dfb337387b4692138a54bc6a5e78baee38327a5379492cf0384a9847d927
rerun-of: REVIEW-ARC-0006
```

## Review Context

### Requirements

`docs/architecture/requirements.md`

### Requirements Review

`docs/reviews/grill/requirements/0001-multi-tenant-requirements.md`

### Parent Decisions

None identified. No separate parent ADR materially constrains the topology decision.

### Previous Architecture Reviews

- `docs/reviews/architecture/0001-multi-tenant-data-topology.md`
- `docs/reviews/architecture/0002-multi-tenant-data-topology.md`
- `docs/reviews/architecture/0003-multi-tenant-data-topology.md`
- `docs/reviews/architecture/0004-multi-tenant-data-topology.md`
- `docs/reviews/architecture/0005-multi-tenant-data-topology.md`
- `docs/reviews/architecture/0006-multi-tenant-data-topology.md`

Same-target reviews are lineage and finding-history evidence, not fingerprint inputs.

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

Canonical execution used `.engineering/platform/scripts/review_execution.py` and Review Execution Protocol v1. The target and material context are unchanged from #0006. This is an explicitly requested fresh assessment, not a review of changed architecture inputs.

## Prior Finding Resolution

The ADR is unchanged since #0006. The prior significant and minor findings remain unresolved; no target changes close them. The rerun independently confirms the same overall recommendation and conditions.

| Prior Finding | Source | Resolution |
|---|---|---|
| Tenant-directory availability, cache consistency, and outage/stale-route behavior are unspecified. | `docs/reviews/architecture/0006-multi-tenant-data-topology.md` | DOES NOT RESOLVE |
| Shard capacity and failure-domain limits are unspecified. | `docs/reviews/architecture/0006-multi-tenant-data-topology.md` | DOES NOT RESOLVE |
| Tenant-level recovery and deletion safety are unproven. | `docs/reviews/architecture/0006-multi-tenant-data-topology.md` | DOES NOT RESOLVE |
| Migration fencing and authoritative-writer transition are undefined. | `docs/reviews/architecture/0006-multi-tenant-data-topology.md` | DOES NOT RESOLVE |
| Online copy/catch-up consistency behavior is unspecified. | `docs/reviews/architecture/0006-multi-tenant-data-topology.md` | DOES NOT RESOLVE |
| Placement thresholds and repeatable performance profile are absent. | `docs/reviews/architecture/0006-multi-tenant-data-topology.md` | DOES NOT RESOLVE |
| Shared-schema isolation enforcement and privileged access boundaries are deferred. | `docs/reviews/architecture/0006-multi-tenant-data-topology.md` | DOES NOT RESOLVE |
| Legacy backup scope and retirement criteria are unspecified. | `docs/reviews/architecture/0006-multi-tenant-data-topology.md` | DOES NOT RESOLVE |
| Tenant telemetry access, retention, and cardinality controls are undefined. | `docs/reviews/architecture/0006-multi-tenant-data-topology.md` | DOES NOT RESOLVE |

## Purpose

Reassess whether the proposed hybrid tenancy topology is appropriate for the documented business and quality drivers, and whether the ADR is sufficiently defined to progress to detailed design.

## Architecture Summary

The ADR adopts shared-schema tenant shards or database pools as the default for standard tenants, with dedicated shards or databases for exceptional workload, regulatory, or contractual requirements. A tenant directory resolves authoritative placement. Tenant context is validated and propagated across request, persistence, cache, messaging, background processing, and telemetry paths. The ADR outlines tenant-specific migration, restore, deletion reconciliation, and regional placement, while explicitly deferring detailed enforcement and operational designs.

## Architectural Drivers

- Growth to 250,000–300,000 tenants.
- Skewed workloads, with 500–1,000 TPS peaks for the largest tenants and aggregate bursts near 30,000 TPS.
- Interactive latency and tiered availability targets.
- Tenant isolation across application, data, recovery, and operations.
- Tenant-specific recovery with prototype RPO/RTO of 15 minutes/four hours.
- EU/EEA residency for primary data, replicas, backups, and recovery copies.
- Tenant-by-tenant incremental migration and a five-minute final write-quiesce target.
- Infrastructure cost and operational-effort reduction without unacceptable noisy-neighbor risk or failure blast radius.

## What Looks Sound

- The selected topology balances shared-platform cost and scale with dedicated placement for workload and regulatory exceptions.
- The ADR compares plausible alternatives and identifies why global shared-database and schema-per-tenant designs are unsuitable defaults.
- The tenant directory is explicitly limited to placement metadata rather than tenant business state.
- Client-supplied tenant identifiers are not authoritative without validation, and loss of tenant context fails closed.
- Shared-schema isolation requires more than application filters and calls for defense in depth.
- Residency requirements cover backups and recovery copies in addition to primary data.
- Migration explicitly rejects blind rollback after the target accepts a committed write.
- The ADR distinguishes a topology decision from proof of the stated production targets.

## Findings

### Finding 1

**Severity:** SIGNIFICANT  
**Finding:** Directory availability objectives and routing behavior during outage, stale cache, or concurrent placement change are not defined.  
**Why it matters:** The directory is on the tenant request path; outage threatens availability, and stale placement can misroute tenant operations.  
**Recommendation:** Define availability/recovery objectives, routing versions, cache invalidation, outage behavior, and safe rejection of stale routes.

### Finding 2

**Severity:** SIGNIFICANT  
**Finding:** Shard capacity and maximum failure blast radius are not measurable in the ADR.  
**Why it matters:** The stated benefits of bounded failure domains and horizontal scaling cannot be verified without capacity and affected-tenant limits.  
**Recommendation:** Set storage, throughput, connection, recovery, and tenant-count limits per shard, and validate them under load and failure tests.

### Finding 3

**Severity:** SIGNIFICANT  
**Finding:** Tenant-level restore, deletion replay, and residency are required but no evidence demonstrates their behavior or achievement of the prototype RPO/RTO.  
**Why it matters:** Shared-shard recovery may affect neighboring tenants, resurrect deleted data, violate residency, or miss recovery objectives.  
**Recommendation:** Test recovery for shared and dedicated placements, including deletion reconciliation and regional constraints; capture measured RPO/RTO and tenant-isolation evidence.

### Finding 4

**Severity:** SIGNIFICANT  
**Finding:** Migration cutover lacks a defined write-fencing and authoritative-writer protocol.  
**Why it matters:** In-flight work, workers, or stale routes may continue writing to the legacy store after target activation, causing divergent state.  
**Recommendation:** Define request draining/fencing, route-generation transitions, old-writer rejection, and the point at which the target is the only writable authority.

### Finding 5

**Severity:** SIGNIFICANT  
**Finding:** Online copy and catch-up lack explicit ordering, checkpoint, duplicate/retry, reconciliation, and cutover-validation semantics.  
**Why it matters:** The destination can diverge before cutover even if final writes are fenced.  
**Recommendation:** Define the change-capture consistency contract and verify it under retries, duplicates, out-of-order events, and partial failures.

### Finding 6

**Severity:** SIGNIFICANT  
**Finding:** Placement thresholds and repeatable workload acceptance criteria are not defined.  
**Why it matters:** Aggregate TPS and latency goals do not establish transaction mix, burst duration, concurrency, tenant distribution, or when promotion/throttling is required.  
**Recommendation:** Define measurable promotion/demotion criteria and a representative workload profile before production sizing or automated placement.

### Finding 7

**Severity:** SIGNIFICANT  
**Finding:** Concrete shared-schema isolation enforcement and privileged administrative access controls remain deferred.  
**Why it matters:** Application abstractions alone do not prove that cross-tenant reads and writes are prevented.  
**Recommendation:** Select enforceable database/data-access and authorization controls, define privileged access, and require automated negative isolation tests before production.

### Finding 8

**Severity:** MINOR  
**Finding:** Supported legacy backup versions, import acceptance criteria, and retirement conditions are unspecified.  
**Why it matters:** Transitional compatibility can become an indefinite maintenance/security burden or fail to support required restores.  
**Recommendation:** Define the version window, integrity checks, import criteria, and retirement trigger before migration rollout.

### Finding 9

**Severity:** MINOR  
**Finding:** Telemetry controls for tenant identifiers, including access, retention, and metric cardinality, are unspecified.  
**Why it matters:** Tenant-level telemetry can expose sensitive context and high-cardinality metrics can increase cost and reduce operational usefulness.  
**Recommendation:** Set access, redaction, retention, and cardinality rules; use controlled correlation for tenant-specific diagnosis.

## Standards Compliance

- **Architecture principles — PARTIALLY COMPLIANT:** The direction is driven by documented scale and isolation requirements and acknowledges complexity, but important failure, capacity, consistency, and recovery details remain open.
- **Secure engineering — PARTIALLY COMPLIANT:** Tenant identity validation and fail-closed context are stated; isolation enforcement and privileged controls remain undecided.
- **Testing standard — PARTIALLY COMPLIANT:** Relevant tenant-isolation, migration, resilience, performance, and recovery testing is recognized but not defined with complete acceptance criteria or evidence.
- **Observability standard — PARTIALLY COMPLIANT:** Tenant context and migration visibility are considered; directory/shard health goals and tenant telemetry controls remain open.
- **API standard — PARTIALLY COMPLIANT:** Compatibility is a requirement, but the ADR does not define contract inventory or automated compatibility checks.
- **Quality gates policy — PARTIALLY COMPLIANT:** Tenant isolation tests are expected, but the ADR does not map them and other controls to mandatory gates.
- **Secrets policy — COMPLIANT:** No secret material is specified.
- **Human approval policy — COMPLIANT:** The ADR remains proposed and does not authorize production or destructive migration.

## Alternatives Worth Considering

The hybrid topology with a bounded shard/pool default and dedicated exceptions remains the strongest fit for the documented workload skew, scale, isolation, recovery, and residency needs. A single global shared database and schema-per-tenant remain poor defaults for the stated failure-domain and lifecycle concerns. No materially simpler topology is evident that satisfies the combined drivers.

## Required Decisions

- Directory availability, cache/version consistency, and stale-route semantics.
- Shard capacity and failure-blast-radius limits.
- Workload profile and tenant placement/promotion thresholds.
- Shared-schema isolation enforcement and privileged-access boundaries.
- Migration copy/catch-up consistency and cutover fencing.
- Tenant recovery proof, deletion reconciliation, residency, RPO, and RTO.
- Legacy backup version support and retirement.
- Tenant telemetry access, retention, and cardinality controls.

## Conditions

1. Keep the ADR proposed until accepted by the authorized decision owner.
2. Resolve directory failure/stale-route behavior, shared-schema isolation controls, and migration fencing before production implementation or migration.
3. Define and test shard capacity, placement thresholds, and workload acceptance criteria.
4. Define and test copy/catch-up consistency, retries, partial-failure recovery, and cutover validation.
5. Demonstrate tenant-level recovery, deletion safety, residency compliance, and measured RPO/RTO for shared and dedicated placements.
6. Define legacy backup support scope and tenant telemetry privacy/cardinality controls before operational rollout.
7. Validate the cost and operational-reduction assumptions against current baselines.

## Recommendation

```text
APPROVE WITH CONDITIONS
```

The architecture direction remains appropriate to advance into detailed design. This is not production approval. The significant findings and conditions must be resolved or evidenced at the relevant design and production-readiness gates.

This fresh assessment confirms the prior recommendation; it does not represent new architecture evidence because the target and material context have not changed.

## Remaining Risks

- Directory unavailability or stale placement may interrupt service or misroute tenant operations.
- Unbounded shard size may undermine failure containment.
- Inadequate migration consistency or fencing may leave competing or divergent data stores.
- Tenant recovery may violate isolation, deletion, residency, or recovery-time objectives.
- Unverified isolation enforcement may permit cross-tenant access.
- Cost and operational benefits remain unproven until measured.

## Next Engineering Activity

Continue detailed design for the tenant directory, shared-shard enforcement, migration consistency/fencing, and tenant-level recovery. Define repeatable workload and resilience tests, then update the ADR with decisions and evidence before production implementation.

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

Execution semantics are defined by Review Execution Protocol v1 and the recorded canonical execution mode.

This review does not replace an ADR. The ADR records the architecture decision; this document records the independent review of that decision.
