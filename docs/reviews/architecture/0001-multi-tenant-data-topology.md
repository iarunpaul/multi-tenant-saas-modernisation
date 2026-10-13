# REVIEW-ARC-0001 — Multi-Tenant Data Topology

## Metadata

```yaml
id: REVIEW-ARC-0001
type: architecture
skill: architecture-review
status: completed
date: 2026-10-11
reviewed-artifact: docs/architecture/ADRs/0001-multi-tenant-data-topology.md
platform-version: v0.1.3
```

## Purpose

Assess whether the proposed hybrid data topology is appropriate for the
modernization requirements, platform standards, and known operational
constraints.

## Architecture Summary

The proposal uses shared-schema tenant shards or database pools for standard
tenants, with dedicated shards or databases for exceptional workload,
regulatory, or contractual requirements. A tenant directory provides
authoritative placement metadata. Tenant context must be validated throughout
the request and processing paths. Tenant migrations are incremental, with a
defined point after which recovery proceeds forward rather than routing writes
back to the legacy store.

## Architectural Drivers

- Growth from approximately 100,000 to 250,000–300,000 tenants.
- Highly skewed tenant load, including largest tenants peaking at 500–1,000 TPS.
- Aggregate throughput target of 10,000–20,000 TPS with short bursts near
  30,000 TPS and interactive latency targets of P95 below 300 ms / P99 below
  750 ms.
- Strong tenant isolation, with dedicated databases for regulated or
  contractually isolated tenants and workload-based exceptional placement.
- Independent tenant recovery with prototype targets of 15-minute RPO and
  4-hour RTO for standard tenants.
- EU/EEA residency, including replicas, backups, and recovery copies.
- Incremental tenant migration with a five-minute maximum final write-quiesce
  target.
- Cost and operational-effort reduction without unacceptable availability,
  recovery, or noisy-neighbor risks.

## What Looks Sound

- The ADR evaluates credible topology alternatives and rejects a single global
  shared database and schema-per-tenant as defaults for stated reasons.
- Hybrid placement is tied to workload skew and explicit regulatory,
  contractual, and service-tier requirements.
- Tenant placement is metadata-driven, and the directory is explicitly not a
  store for tenant business data.
- Tenant context is required to be validated and propagated; application
  filtering alone is not considered sufficient isolation.
- The migration section defines a point of no return and avoids unsafe
  post-write routing rollback.
- Tenant-level restore, deletion replay, residency, and legacy backup import
  are recognized as capabilities requiring operational validation.
- The proposal avoids prescribing unrelated technologies or unnecessary
  distributed-system patterns.

## Findings

### Finding 1

**Severity:** SIGNIFICANT  
**Finding:** The tenant directory is a critical routing dependency, but its
availability, cache consistency, and behavior when unavailable or stale are
deferred.  
**Why it matters:** Directory failure can affect platform availability;
incorrect or stale placement can also route tenant operations to the wrong
data boundary.  
**Recommendation:** Define directory availability objectives, placement
versioning and cache invalidation, safe failure behavior, and recovery before
production adoption.

### Finding 2

**Severity:** SIGNIFICANT  
**Finding:** Shard capacity and failure-domain limits are not defined.  
**Why it matters:** Sharding bounds blast radius only when shard size and
failure handling are deliberately constrained. Unbounded placement can put
many tenants at risk from one shard failure or overload.  
**Recommendation:** Define a capacity and failure-containment model, then
validate it with representative load, noisy-neighbor, and resilience tests.

### Finding 3

**Severity:** SIGNIFICANT  
**Finding:** The tenant recovery workflow is conceptual and has not demonstrated
the stated RPO/RTO or deletion-safety requirements.  
**Why it matters:** Shared-shard restore is substantially more complex than
restoring a dedicated database and can affect neighboring tenants or reintroduce
erased data.  
**Recommendation:** Exercise tenant-level recovery from representative shared
and dedicated placements, including deletion replay, residency controls, and
measured recovery objectives.

### Finding 4

**Severity:** SIGNIFICANT  
**Finding:** Tenant promotion thresholds and the performance acceptance profile
remain undefined.  
**Why it matters:** Without transaction mix, burst duration, concurrency, and
workload-based placement thresholds, shard sizing and hot-tenant isolation
cannot be validated objectively.  
**Recommendation:** Define a repeatable workload model and measurable
promotion/demotion rules before production sizing or placement automation.

### Finding 5

**Severity:** SIGNIFICANT  
**Finding:** The migration point of no return is stated, but write fencing and
the single-writer guarantee around routing changes are not described.  
**Why it matters:** Concurrent writes to legacy and target stores, or requests
using stale routes, could create split-brain data after cutover.  
**Recommendation:** In the migration design, define how writes are quiesced,
in-flight operations drained or fenced, route versions changed, and the target
made the sole writer before activation.

### Finding 6

**Severity:** MINOR  
**Finding:** Transitional legacy-backup import has no supported-version scope
or retirement conditions.  
**Why it matters:** A migration-only compatibility path can become a permanent
maintenance obligation if its boundary is not explicit.  
**Recommendation:** Set supported backup versions, import validation criteria,
and retirement conditions before migration rollout.

## Standards Compliance

- **Architecture principles — COMPLIANT:** The topology is driven by stated
  scale, workload, isolation, recovery, and residency needs. Its additional
  complexity is acknowledged and alternatives are compared.
- **Secure engineering — PARTIALLY COMPLIANT:** Tenant identity trust,
  authorization boundaries, and fail-closed handling are stated. Specific
  routing enforcement, administrative access controls, and automated
  isolation evidence remain for detailed design.
- **Testing standard — PARTIALLY COMPLIANT:** Tenant-boundary and recovery
  testing are recognized, but measurable isolation, migration, resilience, and
  performance acceptance tests remain to be defined.
- **Observability standard — PARTIALLY COMPLIANT:** Migration visibility and
  tenant diagnostics are requirements, but directory/shard health signals,
  operational SLOs, and controls for high-cardinality tenant telemetry are
  not yet specified.
- **API standard — PARTIALLY COMPLIANT:** Compatibility is an accepted
  requirement, but an inventory of existing API/event contracts and explicit
  verification approach remain outstanding.
- **Quality gates policy — PARTIALLY COMPLIANT:** The ADR calls for automated
  tenant-boundary tests, but does not yet specify architecture, contract,
  infrastructure, or security gates that enforce the relevant requirements.

## Alternatives Worth Considering

The ADR's hybrid model is appropriate to carry forward. A simpler shard-pool
default with dedicated exceptions is already included and should be retained
unless evidence shows a need for more placement classes. Neither universal
database-per-tenant nor one global shared database meets the stated balance of
operational scale, isolation, recovery, and residency.

## Required Decisions

- Directory availability, routing-version, cache, and stale-entry behavior.
- Shard capacity limits and acceptable shard-level failure blast radius.
- Tenant placement thresholds and promotion/demotion governance.
- Workload profile and acceptance method for load and noisy-neighbor testing.
- Write fencing, in-flight request handling, and single-writer transition during
  migration cutover.
- Supported legacy backup formats and transitional support retirement.
- Operational metric and trace cardinality/retention rules for tenant-level
  identifiers.

## Conditions

1. Keep ADR-0001 in proposed status until the authorized decision owner accepts
   the topology.
2. Resolve directory and write-fencing designs before production migration.
3. Demonstrate independent tenant recovery, deletion preservation, and
   residency compliance before production adoption.
4. Validate throughput, latency, shard isolation, and placement thresholds
   using a repeatable workload and resilience test profile.
5. Define legacy backup import scope and tenant-identifier telemetry controls
   before operational rollout.

## Recommendation

```text
APPROVE WITH CONDITIONS
```

The hybrid sharded-default direction is justified by the requirements and is
suitable for detailed architecture design. This review approves the direction,
not production readiness. The unresolved conditions above must be addressed
before production adoption.

## Remaining Risks

- Directory unavailability or stale routing can cause broad service impact or
  tenant-boundary violations.
- Shard overload or failure can affect multiple tenants.
- Tenant restore may exceed RPO/RTO or reintroduce deleted data until exercised.
- Cutover without explicit fencing can create divergent authoritative writes.
- Cost, provisioning, schema rollout, and manual-operation improvement targets
  remain assumptions until compared with measured baselines.

## Next Engineering Activity

Continue detailed architecture design for the tenant directory, shard failure
model, shared-schema isolation controls, migration fencing/reconciliation, and
tenant-level recovery. Update ADR-0001 with the resulting decisions and
evidence, then seek decision-owner acceptance before production implementation.

## Suggested Skill Handoff

```text
architecture-review
    ↓
resolve significant findings
    ↓
record/accept ADR-0001
    ↓
implementation-plan
    ↓
grill implementation-plan
```

## Evidence

This document records the completed architecture review and may be referenced
for architecture-governance controls.

This review does not replace an ADR. The ADR records the architecture decision;
this document records an independent review of that decision.
