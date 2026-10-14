# REVIEW-ARC-0002 — Multi-Tenant Data Topology

## Metadata

```yaml
id: REVIEW-ARC-0002
type: architecture
skill: architecture-review
status: completed
date: 2026-10-13
reviewed-artifact: docs/architecture/ADRs/0001-multi-tenant-data-topology.md
platform-version: v0.2.0
protocol-version: unversioned-review-execution-standard
target-sha256: 1850215454054dc8cb97e8544772372f607005516e1945013948ac8584b71f5d
input-fingerprint: 50d2e237124e1c1bdcddfe969b227276dc372eabdfbb5787d0efe802c70bb7d0
```

## Review Context

### Requirements

`docs/architecture/requirements.md`

### Requirements Review

`docs/reviews/grill/requirements/0001-multi-tenant-requirements.md`

### Parent Decisions

None identified. The reviewed ADR is the current topology decision; no separate parent ADR materially constrains it.

### Previous Architecture Reviews

`docs/reviews/architecture/0001-multi-tenant-data-topology.md`

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

No repository review-execution script was available, so the normalized input fingerprint was calculated from the sorted repository-relative input paths and their content hashes, together with the review type, skill, platform version, and protocol identifier. The review-execution standard does not currently declare a protocol version.

## Prior Finding Resolution

| Prior Finding | Source | Resolution |
|---|---|---|
| Tenant directory availability, cache consistency, and unavailable/stale behavior are undefined. | `docs/reviews/architecture/0001-multi-tenant-data-topology.md` | PARTIALLY RESOLVES — the ADR makes the directory authoritative and identifies its criticality, but leaves availability objectives and stale-route/cache behavior to later design. |
| Shard capacity and failure-domain limits are undefined. | `docs/reviews/architecture/0001-multi-tenant-data-topology.md` | PARTIALLY RESOLVES — bounded shards and sizing validation are called out, but no measurable capacity or blast-radius limits are set. |
| Tenant-level recovery is conceptual and unproven against the recovery/deletion requirements. | `docs/reviews/architecture/0001-multi-tenant-data-topology.md` | PARTIALLY RESOLVES — the restore and deletion-reconciliation workflow is more explicit, but the RPO/RTO, isolation, residency, and deletion guarantees remain unvalidated. |
| Placement thresholds and the performance acceptance profile are undefined. | `docs/reviews/architecture/0001-multi-tenant-data-topology.md` | PARTIALLY RESOLVES — placement factors and validation objectives are listed, but thresholds and a repeatable workload profile are not defined. |
| Cutover write fencing and the single-writer guarantee are unspecified. | `docs/reviews/architecture/0001-multi-tenant-data-topology.md` | PARTIALLY RESOLVES — the point of no return and write-quiesce phase are explicit, but fencing, request draining, and stale-route rejection are not. |
| Legacy backup import scope and retirement conditions are unspecified. | `docs/reviews/architecture/0001-multi-tenant-data-topology.md` | PARTIALLY RESOLVES — the ADR marks this support as transitional and records the need for supported versions and retirement criteria, but does not define them. |
| Tenant-identifier telemetry/cardinality controls are unspecified. | `docs/reviews/architecture/0001-multi-tenant-data-topology.md` | PARTIALLY RESOLVES — telemetry propagation and aggregate/de-identified analytics are addressed, but access, retention, and high-cardinality controls are not. |

## Purpose

Assess whether the proposed hybrid topology is appropriate for the stated scale, workload skew, tenant isolation, migration, recovery, residency, availability, and cost drivers, and whether the ADR is sufficiently defined to proceed to detailed design.

## Architecture Summary

The ADR selects a hybrid topology: shared-schema tenant shards or pools for standard tenants, with dedicated shards or databases for exceptional workload, regulatory, or contractual needs. An authoritative tenant directory resolves placement. Tenant context must be validated and propagated across application and data paths. Tenant migration is incremental, with a stated point after which recovery must use forward reconciliation rather than unsafe routing rollback. Tenant-scoped restore, deletion reconciliation, regional placement, and legacy-backup import are identified as required capabilities.

## Architectural Drivers

- Growth from approximately 100,000 tenants to 250,000–300,000.
- Highly skewed workloads, including largest tenants peaking at 500–1,000 TPS and aggregate bursts near 30,000 TPS.
- Interactive latency and tiered availability targets.
- Isolation across all tenant-scoped data paths, with dedicated placement for justified cases.
- Independent tenant recovery, with prototype RPO/RTO targets of 15 minutes/four hours.
- EU/EEA residency for primary, replica, backup, and recovery data.
- Incremental tenant migration with a five-minute final write-quiesce target.
- Reduced infrastructure cost and operational effort without unacceptable failure blast radius or noisy-neighbor impact.

## What Looks Sound

- The selected hybrid topology addresses the documented workload skew and exception cases without imposing dedicated databases on every tenant.
- The ADR compares plausible alternatives and gives specific reasons not to use a global shared database or schema-per-tenant as the default.
- The tenant directory is identified as placement metadata rather than a store for tenant business state.
- Tenant identity is not trusted merely because it was supplied by a client; missing tenant context fails closed.
- Application filtering alone is explicitly insufficient, and the ADR calls for defense in depth for shared-schema isolation.
- Regional placement includes replicas, backups, and recovery copies, not just primary data.
- The migration point of no return avoids an unsafe post-write rollback to the legacy store.
- The ADR distinguishes architecture direction from validation evidence and defers technology choices that are not yet justified.

## Findings

### Finding 1

**Severity:** SIGNIFICANT  
**Finding:** The tenant directory is a critical routing dependency, but its availability target and behavior under outage, stale cache, or concurrent placement change remain unspecified.  
**Why it matters:** Directory unavailability can impair the whole data plane; stale placement can send operations to an obsolete location or undermine tenant isolation during movement.  
**Recommendation:** In the directory/control-plane design, define availability and recovery objectives, routing-version semantics, cache lifetime and invalidation, behavior when the directory is unreachable, and how stale routes are rejected safely.

### Finding 2

**Severity:** SIGNIFICANT  
**Finding:** Shards are described as bounded failure domains, but the ADR does not define capacity limits or the maximum tenant population/workload exposed to one shard failure.  
**Why it matters:** Without explicit limits, shard-level failure and overload may affect more tenants than intended, and the stated scaling and isolation benefits cannot be sized or tested.  
**Recommendation:** Establish measurable shard capacity and blast-radius limits, including storage, throughput, connection, and recovery constraints, and validate them with representative load and failure tests.

### Finding 3

**Severity:** SIGNIFICANT  
**Finding:** Tenant-level recovery and deletion safety have a plausible workflow but no demonstrated isolation or measured recovery evidence.  
**Why it matters:** A shared-shard restore can affect neighboring tenants, exceed the prototype RPO/RTO, reintroduce deleted data, or violate residency constraints.  
**Recommendation:** Exercise tenant restore for shared and dedicated placements, including deletion-state reconciliation and residency enforcement; record measured RPO/RTO and prove no neighboring tenant data is exposed or changed.

### Finding 4

**Severity:** SIGNIFICANT  
**Finding:** Migration defines quiescing and a point of no return, but not the write-fencing mechanism that ensures only one authoritative writer during cutover.  
**Why it matters:** In-flight requests, workers, or stale routes can still write to the legacy store after target activation, causing divergent state despite the stated rollback rule.  
**Recommendation:** Define how in-flight work is drained or fenced, how route generations are advanced, how old writers are rejected, and when the target is guaranteed to be the sole writer before accepting writes.

### Finding 5

**Severity:** SIGNIFICANT  
**Finding:** Workload-based promotion and shard sizing cannot yet be validated because placement thresholds and the performance acceptance workload are not specified.  
**Why it matters:** TPS totals and latency objectives alone do not define transaction mix, burst duration, concurrency, tenant distribution, or the point at which a tenant is promoted or throttled.  
**Recommendation:** Define a repeatable workload profile and measurable promotion/demotion criteria before production sizing or automated placement; test aggregate load and hot-tenant interference against those criteria.

### Finding 6

**Severity:** SIGNIFICANT  
**Finding:** The ADR requires defense in depth for shared-schema isolation but leaves the enforcement mechanisms and administrative access boundaries to subsequent design.  
**Why it matters:** Tenant isolation is a core security requirement; a tenant-aware query abstraction without enforceable controls and verification can leave cross-tenant access dependent on application correctness.  
**Recommendation:** Before production implementation, select and verify the applicable database, data-access, authorization, and administrative controls, and require automated negative tests that demonstrate cross-tenant reads and writes are denied.

### Finding 7

**Severity:** MINOR  
**Finding:** Legacy backup compatibility is called transitional, but supported backup versions, validation/import acceptance criteria, and retirement conditions remain undecided.  
**Why it matters:** An unbounded compatibility path can become a permanent maintenance and security obligation or fail to support the intended migration population.  
**Recommendation:** Set the supported-version window, integrity checks, import acceptance criteria, and retirement trigger before migration rollout.

### Finding 8

**Severity:** MINOR  
**Finding:** Tenant-aware telemetry is required, but the ADR does not define controls for tenant identifiers in logs/metrics/traces, including access, retention, and metric cardinality.  
**Why it matters:** Tenant-level diagnostics can expose sensitive operational context and high-cardinality dimensions can undermine observability cost and usability.  
**Recommendation:** Define authorized use, redaction, retention, and cardinality rules for tenant identifiers; prefer controlled correlation or support workflows over unrestricted metric dimensions.

## Standards Compliance

- **Architecture principles — PARTIALLY COMPLIANT:** The topology is justified by stated scale, workload skew, isolation, recovery, and residency needs, and its complexity is acknowledged. Some critical failure, capacity, and consistency behavior remains for later decisions.
- **Secure engineering — PARTIALLY COMPLIANT:** Tenant identity validation, fail-closed context handling, and defense in depth are stated. The concrete isolation enforcement and privileged administrative boundaries remain unresolved.
- **Testing standard — PARTIALLY COMPLIANT:** The ADR requires recovery, load, noisy-neighbor, and migration validation, but lacks complete acceptance profiles and evidence.
- **Observability standard — PARTIALLY COMPLIANT:** Tenant-context propagation and migration observability are addressed; directory/shard health objectives and tenant-identifier/cardinality controls remain open.
- **API standard — PARTIALLY COMPLIANT:** Compatibility is an accepted requirement, but no explicit API/event contract inventory or automated compatibility verification is specified in this ADR.
- **Quality gates policy — PARTIALLY COMPLIANT:** Tenant-boundary and other verification needs are identified, but the ADR does not map them to mandatory automated gates.
- **Secrets policy — COMPLIANT:** No secrets are specified; identity and secret-management details remain subject to implementation controls.
- **Human approval policy — COMPLIANT:** The ADR remains proposed and does not claim to authorize production, destructive migration, or external-contract changes.

## Alternatives Worth Considering

The selected hybrid model, with a bounded shard/pool default and dedicated exceptions, is a credible balance for the stated drivers. A single shared database and schema-per-tenant are rejected with relevant recovery, blast-radius, and scale reasoning. No materially simpler topology is evident that meets the same combination of workload isolation, recovery, residency, and tenant-count goals; the simpler sharded-pool default should remain the baseline unless evidence justifies further placement classes.

## Required Decisions

- Directory availability, cache/version consistency, and stale-routing behavior.
- Shard capacity and acceptable failure/overload blast radius.
- Tenant promotion/demotion thresholds and an objective workload acceptance profile.
- Shared-schema isolation enforcement and privileged administrative access.
- Cutover fencing, in-flight operation handling, and the single-writer guarantee.
- Recovery proof for tenant isolation, deletion replay, residency, RPO, and RTO.
- Supported legacy backup versions, validation criteria, and retirement conditions.
- Tenant identifier access, retention, and telemetry cardinality controls.

## Conditions

1. Keep the ADR proposed until the authorized decision owner accepts the topology.
2. Resolve directory failure/stale-route semantics, shared-schema isolation controls, and migration write fencing before production migration or production implementation.
3. Define shard capacity, workload profiles, and tenant placement thresholds, then validate throughput, latency, noisy-neighbor behavior, and failure blast radius.
4. Demonstrate tenant-level recovery for shared and dedicated placements, including deletion safety, residency, and measured RPO/RTO, before production adoption.
5. Define the legacy-backup support window and tenant telemetry privacy/cardinality controls before operational rollout.
6. Treat the cost, provisioning, schema rollout, and manual-intervention targets as hypotheses until measured against current baselines.

## Recommendation

```text
APPROVE WITH CONDITIONS
```

The hybrid sharded-default direction is justified by the requirements and is appropriate to advance into focused detailed design. This approval is limited to the architecture direction; it is not approval for production implementation or migration. The significant findings and conditions above must be resolved or validated at the appropriate design and production-readiness gates.

## Remaining Risks

- Directory outage or stale placement may impair availability or route work incorrectly.
- Unbounded shard sizing may defeat the intended failure containment.
- Recovery may miss RPO/RTO targets, affect neighboring tenants, resurrect deleted data, or breach residency.
- Unfenced cutover may leave competing authoritative writers.
- Unverified isolation controls may permit cross-tenant access.
- Cost and operational-effort targets remain unproven until measured.

## Next Engineering Activity

Continue detailed design in the follow-up decisions identified by the ADR, prioritizing the tenant directory/control plane, shared-shard isolation, migration fencing/reconciliation, and tenant-level recovery. Define a repeatable workload and failure test profile, then update the ADR with decisions and evidence before production implementation.

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
