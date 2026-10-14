# GRILL-0004 — Multi-Tenant SaaS Modernisation Requirements

## Metadata

```yaml
id: REVIEW-REQ-0004
type: requirement
skill: grill
status: completed
date: 2026-10-14
reviewed-artifact: docs/architecture/requirements.md
platform-version: v0.2.3
protocol-version: "1"
execution-mode: canonical
target-sha256: f5912d5217c136493a4eda96883ba14f1cc2dab94368da029bbcce48cca982f1
input-fingerprint: 79ade31a03172b09dba3b52edfe9138a8b143a311a3e4140246bbb3607ff37f9
supersedes: REVIEW-REQ-0003
```

## Execution Manifest

```json
{
  "context": [
    {
      "path": ".engineering/platform/policies/human-approval.md",
      "sha256": "865d8256afe5e4da4cb247dc32abbbe5634550f450c69fa83f6ae663a6807275"
    },
    {
      "path": ".engineering/platform/policies/quality-gates.md",
      "sha256": "bc3fd92345063f9624e2ce3faf70795c1a130b644506906ce03a2766b19d7ff6"
    },
    {
      "path": ".engineering/platform/policies/secrets.md",
      "sha256": "d142dc13f0bd1421138a50fc204a2bcf92171336172f5efbc36824d0d0a3cab0"
    },
    {
      "path": ".engineering/platform/standards/api/api-standard.md",
      "sha256": "aadd13b63d000ec87e30b9b131040d9e971b7a36e49dffa9b3b6940849a527cd"
    },
    {
      "path": ".engineering/platform/standards/architecture/principles.md",
      "sha256": "5473d2ecf20d97b25d68ccd1862d1dadea0370e540c2884f33e291fd3de6bef8"
    },
    {
      "path": ".engineering/platform/standards/engineering/development.md",
      "sha256": "65480fff94d341bbbf43710af3c84a32d073b030a4003aabb93d7bd03e3d76ac"
    },
    {
      "path": ".engineering/platform/standards/observability/observability-standard.md",
      "sha256": "e151fc6923392328de23ae71ee34413e41de823e615fe7e1fd24a0606174d66b"
    },
    {
      "path": ".engineering/platform/standards/security/secure-engineering.md",
      "sha256": "aeff6be83acc3fe8d4532433addf04afc9e6448a31aa7c616cab0a11933d4cb2"
    },
    {
      "path": ".engineering/platform/standards/testing/testing-standard.md",
      "sha256": "6ba4df428100b1402bac900846b845e7e3b7541976a3f1f05f46753f42407f57"
    },
    {
      "path": "docs/architecture/ADRs/0001-multi-tenant-data-topology.md",
      "sha256": "81ee0abeea883b5fd4cbf55926ac7765adbab253dd7329aee953c32e97b14c00"
    }
  ],
  "platformVersion": "v0.2.3",
  "protocolVersion": "1",
  "reviewType": "requirement",
  "skill": "grill",
  "target": {
    "path": "docs/architecture/requirements.md",
    "sha256": "f5912d5217c136493a4eda96883ba14f1cc2dab94368da029bbcce48cca982f1"
  }
}
```

## Review Context

### Review Target

`docs/architecture/requirements.md`

### Material Context

- `docs/architecture/ADRs/0001-multi-tenant-data-topology.md`
- `.engineering/platform/standards/architecture/principles.md`
- `.engineering/platform/standards/engineering/development.md`
- `.engineering/platform/standards/security/secure-engineering.md`
- `.engineering/platform/standards/testing/testing-standard.md`
- `.engineering/platform/standards/observability/observability-standard.md`
- `.engineering/platform/standards/api/api-standard.md`
- `.engineering/platform/policies/quality-gates.md`
- `.engineering/platform/policies/secrets.md`
- `.engineering/platform/policies/human-approval.md`

Previous reviews of this same requirements target were consulted as finding history, not fingerprint context:

- `docs/reviews/grill/requirements/0001-multi-tenant-requirements.md`
- `docs/reviews/grill/requirements/0002-multi-tenant-requirements.md`
- `docs/reviews/grill/requirements/0003-multi-tenant-requirements.md`

The user clarified during discovery that independent tenant restore is required for this review. The user also accepted EU/EEA as the prototype baseline, with customer-specific regulatory and contractual validation deferred to tenant or regional onboarding. These clarifications do not change the reviewed requirements file.

## Purpose

Challenge whether the requirements for modernising the database-per-tenant SaaS platform are clear, testable, and current enough to guide detailed architecture and eventual implementation without prematurely prescribing technology.

## Outcome

The requirements establish useful business outcomes and system-wide drivers for isolation, scalability, migration safety, recovery, and operational simplicity. Together with proposed ADR-0001, they provide sufficient directional input to continue detailed architecture work under explicit prototype assumptions.

They are not a validated production acceptance baseline. The requirements still contain stale workflow status and an unresolved statement about per-tenant restore, despite the user's clarification during this review and the ADR's explicit restore requirement. The document must be reconciled before it is used as authoritative governance or acceptance evidence.

## Confirmed Facts

- The requirements identify the current database-per-tenant model and its operational, cost, schema-management, connection, and observability burdens.
- They require tenant boundaries across identity, APIs, persistence, caches, messaging, background work, telemetry, restore, and administration.
- They call for incremental migration and identify consistency, validation, reconciliation, rollback, and observability as concerns.
- They require comparing multiple tenancy models and explicitly avoid prescribing unnecessary distributed-system patterns.
- ADR-0001 proposes shared-schema tenant shards or database pools as the standard-tenant default, with dedicated placement for exceptional workload, regulatory, or contractual cases; its status is Proposed.
- The source requirements say individual tenant recovery is unresolved, while ADR-0001 and prior review records state it is required.
- No files under `docs/decisions/` were identified as additional decisions governing this review.

## Accepted Assumptions

- The scale, throughput, latency, availability, RPO/RTO, migration, cost, provisioning, and operations figures are prototype/planning targets. Their provenance, accountable owners, workload profile, and measurement methodology have not been independently validated.
- Workload is materially skewed; high-volume or exceptional tenants may need throttling, promotion, or dedicated placement.
- EU/EEA residency is the prototype baseline. Other customer-specific obligations will be validated before onboarding an affected tenant or region.
- Independent tenant restore is required for the directional architecture under review; the requirements document itself has not yet been updated to record this consistently.
- ADR-0001 is a proposed direction, not evidence of authorized decision-owner acceptance.
- The migration point-of-no-return rule recorded in prior Grill reviews is a working design assumption: after a committed target write, recovery must reconcile or move forward rather than blindly route back to the legacy store.

## Material Unknowns

The following are explicitly deferred from deciding the current direction, but must be resolved at the stated gates:

- Target-metric sources, owners, workload shape, measurement windows, and contractual status remain open before production sizing or SLO approval.
- Exact customer and jurisdiction-specific obligations remain open before affected tenant or regional onboarding.
- Isolation and tenant-restore proof, including privileged operations, deletion replay, residency, and measured recovery objectives, remains open before production implementation.
- Legacy backup compatibility windows, integrity criteria, deletion handling, and retirement ownership remain open before migration rollout.
- Shard capacity/blast-radius limits, tenant-directory availability and stale-routing behavior, and migration write fencing/catch-up consistency remain open for detailed architecture.

No unanswered discovery question blocks the current directional assessment: independent restore and the prototype residency assumption were clarified during discovery, while the remaining evidence is explicitly deferred to later design or rollout gates.

## What Looks Sound

- The requirements frame business outcomes and quality attributes without prematurely binding the system to a technology.
- They treat tenant context and isolation as end-to-end concerns rather than a persistence-only filter.
- They recognize workload skew, noisy neighbors, tenant mobility, and differentiated placement.
- They require incremental migration, validation, reconciliation, partial-failure handling, and operational visibility.
- They include residency and deletion concerns for replicas, backup, and recovery copies.
- Their non-assumptions and the architecture principles favor the simplest viable architecture and require complexity to be justified.

## Critical Challenges

### 1. Requirements status and decision traceability are stale

**Issue:** The status section still identifies requirements Grill as the next activity and says an architecture decision has not been made. ADR-0001 now exists as a proposed direction and several reviews have been completed.
**Why it matters:** The current document does not distinguish completed discovery, proposed architecture, and authorized acceptance.
**Question or evidence required:** Refresh phase, status, next activity, and links to the ADR and reviews; explicitly state that the topology remains proposed pending authorized acceptance.
**Potential consequence:** Teams may repeat completed work or mistake a proposal for an approved implementation direction.

### 2. Independent tenant restore is inconsistent in the source requirements

**Issue:** The backup section says per-tenant restore is unresolved, while the ADR and the user's discovery clarification treat it as required.
**Why it matters:** Restore granularity affects isolation, backup design, shard topology, deletion reconciliation, residency, and recovery testing.
**Question or evidence required:** Update the requirements to state the requirement and its acceptance boundary, or record a named owner and decision gate if the user's clarification is not the authorized product decision.
**Potential consequence:** Design and acceptance work could proceed against contradictory recovery expectations.

### 3. Quantitative targets are not yet acceptance criteria

**Issue:** Precise tenant, workload, performance, availability, recovery, and migration figures lack recorded provenance, accountable owners, workload definitions, and measurement windows.
**Why it matters:** These figures cannot safely determine shard sizing, capacity limits, or production acceptance until their relationship and test profile are understood.
**Question or evidence required:** For each target, record its source, owner, measurement method, representative workload, and whether it is a prototype objective, launch criterion, or contractual SLO.
**Potential consequence:** The design may be sized or accepted against unrepresentative or unapproved targets.

### 4. Isolation and recovery need verifiable acceptance evidence

**Issue:** Isolation spans the appropriate system surfaces, but required negative/boundary tests and privileged-access evidence are unspecified. Independent tenant restore is now a clarified requirement, but its proof obligations are not defined.
**Why it matters:** Shared-schema tenancy increases the consequence of a missed tenant boundary; documented intent alone does not prove safe isolation or recovery.
**Question or evidence required:** Define tests for data access, cache, messages, background work, restore, deletion replay, support/admin access, and residency; specify measurable RPO/RTO evidence.
**Potential consequence:** Production could proceed without objective evidence for core security and data-integrity constraints.

### 5. Regulatory scope and legacy backup obligations need rollout gates

**Issue:** EU/EEA is accepted as the prototype baseline, but exact customer obligations and legacy backup support bounds are not specified.
**Why it matters:** Residency, support access, retention, recovery copies, deletion, and import compatibility can change placement and operational obligations.
**Question or evidence required:** Identify the validation owner and evidence required before each cohort/region; define supported backup versions, import integrity, deletion handling, compatibility duration, and retirement owner.
**Potential consequence:** A tenant may be placed or restored contrary to contract or regulation, or legacy recovery promises may become unbounded.

### 6. Operational and performance limits remain qualitative

**Issue:** The requirements name directory routing, hot tenants, noisy neighbors, workload movement, and failure isolation, but do not bound directory availability, stale routes, per-shard capacity, or affected-tenant blast radius.
**Why it matters:** These are central to the proposed shard topology's availability and scale claims.
**Question or evidence required:** In detailed architecture, define testable routing and directory failure behavior, shard capacity and tenant limits, placement thresholds, and performance-isolation criteria.
**Potential consequence:** The solution may reproduce fleet-wide failure modes or fail to contain hot-tenant impact.

## Inherited Finding Traceability

| Prior finding from GRILL-0003 | Resolution |
|---|---|
| Requirements phase/status and decision traceability are stale. | DOES NOT RESOLVE |
| Quantitative targets lack owners, provenance, workload, and measurement criteria. | DOES NOT RESOLVE |
| Tenant isolation lacks verifiable acceptance evidence. | DOES NOT RESOLVE |
| Regulatory/contractual scope needs an owner and gate. | PARTIALLY RESOLVES — EU/EEA is explicitly accepted as a prototype baseline and validation is deferred to onboarding; exact obligations and accountable owner remain open. |
| Backup compatibility and deletion obligations are unbounded. | DOES NOT RESOLVE |
| Independent tenant restore was previously treated as required in review context despite unresolved source wording. | PARTIALLY RESOLVES — the user confirmed it is required for this assessment; the requirements file still contradicts that position. |

## Hidden Assumptions

- The stated tenant and workload projections remain representative over the planning horizon.
- Aggregate throughput and largest-tenant peaks can occur together in a defined, testable workload.
- The five-minute final write-quiesce target is feasible for large tenants and high change rates.
- Customer-visible restore behavior can be preserved while backup implementation and tenancy tiers change.
- Cost and operational-reduction outcomes can be compared against a reproducible current-state baseline.
- “Dedicated shard,” “dedicated database,” and “dedicated infrastructure” are distinct placement tiers with explicit eligibility and operational rules.

## Missing Non-Functional Requirements

- Reproducible workload profiles and measurement windows for throughput, latency, concurrency, burst, and noisy-neighbor behavior.
- Per-shard capacity and maximum tenant/workload blast-radius limits.
- Tenant-directory availability, recovery, stale-routing, and concurrent placement-change objectives.
- Measurable isolation and tenant-recovery acceptance across shared and dedicated placement.
- Automated tests and evidence for tenant context, privileged access, restore, deletion replay, and residency.
- Ownership and measurement windows for availability and service-tier objectives.
- Tenant telemetry access, retention, redaction, and cardinality limits.
- Current-state baselines and calculation methods for cost, provisioning, schema rollout, and manual-intervention goals.

## Failure Scenarios

- Stale tenant placement routes requests or background jobs to the previous shard during migration.
- A hot tenant exhausts shared capacity and degrades unrelated tenants.
- Migration copy/catch-up omits, duplicates, or reorders writes, or legacy writers continue after target activation.
- Tenant restore modifies neighboring tenants, violates residency, misses RPO/RTO, or resurrects deleted data.
- A privileged support path bypasses tenant-context checks.
- A directory or regional failure prevents tenant resolution or recovery within the intended objectives.
- A legacy backup cannot be imported, or its format remains supported indefinitely without ownership or retirement criteria.

## Complexity Assessment

```text
appropriately simple
```

The tenant scale, workload skew, isolation, residency, and recovery drivers justify comparing shared/sharded and dedicated placement. The requirements do not justify microservices, Kubernetes, event sourcing, CQRS, distributed transactions, or active-active multi-region operation without additional evidence.

## Decisions Required

| Severity | Decision |
|---|---|
| SIGNIFICANT | Reconcile the current phase/status and traceability with ADR-0001 and completed reviews, while keeping the ADR's Proposed status clear. |
| SIGNIFICANT | Record independent tenant restore consistently in the requirements and define its acceptance boundary. |
| SIGNIFICANT | Establish target provenance, owners, workload profiles, and measurement methods before production sizing or SLO commitments. |
| SIGNIFICANT | Define isolation, privileged-access, and recovery proof obligations before production implementation. |
| SIGNIFICANT | Establish regulatory/contractual validation ownership and onboarding gates; bound legacy-backup support and deletion-safe recovery before rollout. |
| MINOR | Define baselines for cost, provisioning, schema rollout, and operational-intervention goals. |
| MINOR | Define tenant telemetry access, retention, redaction, and cardinality requirements before operational rollout. |

## Recommendation

```text
PROCEED WITH CONDITIONS
```

The requirements and proposed ADR provide sufficient direction for continued detailed architecture work with explicit prototype assumptions. They are not a production acceptance contract, and the proposed topology is not thereby authorized for implementation. Reconcile the source status and restore requirement; resolve evidence and governance conditions at their stated design and rollout gates.

## Conditions

1. Update the requirements phase/status, next activity, and traceability to ADR-0001 and reviews, preserving the ADR's Proposed status.
2. Make the independent tenant-restore requirement and its acceptance boundary consistent in the requirements and architecture records.
3. Keep prototype figures distinct from validated capacity limits and contractual SLOs; record their source, owner, workload, and measurement method before production sizing.
4. Define and verify tenant-isolation, privileged-access, restore, deletion, residency, RPO, and RTO evidence before production implementation or adoption.
5. Validate applicable regulatory and contractual scope before onboarding affected tenants or regions.
6. Bound legacy-backup support and prove deletion-safe recovery before migration rollout.
7. Set and test shard capacity, blast-radius, directory-failure, placement, and migration-fencing criteria during detailed architecture.
8. Establish current-state baselines before claiming cost or operational-effort reductions.

## Resolved During Grill

- The user confirmed that independent tenant restore is required for this review; the requirements file remains unchanged and must be aligned.
- The user accepted EU/EEA as the prototype residency baseline and deferred customer-specific legal/contractual validation to affected tenant or regional onboarding.
- Prior review records supplied planning figures and a migration point-of-no-return rule. They are carried forward as prototype assumptions and have not been independently validated against operational data.

## Remaining Follow-Up

- Reconcile requirements wording and current workflow status with ADR-0001 and the latest review evidence.
- Confirm source data and accountable owners for scale, workload, latency, availability, recovery, and migration targets.
- Define representative workload acceptance, shard limits, directory behavior, migration fencing/consistency, and placement thresholds during detailed architecture.
- Define automated isolation and recovery evidence, including privileged support access, deletion replay, residency, and measured recovery objectives.
- Confirm customer-specific obligations and bound legacy backup support before production rollout.

## Next Engineering Activity

Update the requirements' status, traceability, and restore statement. Then continue detailed architecture design and validation against the prototype assumptions, keeping ADR-0001 explicitly proposed until authorized acceptance. Follow with an implementation-plan Grill before implementation.

## Suggested Skill Handoff

```text
update requirements status and restore requirement
    ↓
continue detailed architecture / architecture-review
    ↓
grill — implementation plan
    ↓
implement and test
    ↓
security-review and production-readiness before production adoption
```

## Evidence

This document records the completed Grill review and may be referenced as architecture-governance evidence.

Execution semantics are defined by Review Execution Protocol v1 and the recorded canonical execution mode.

This review records analysis of the requirements; it does not replace an ADR or authorize production implementation.
