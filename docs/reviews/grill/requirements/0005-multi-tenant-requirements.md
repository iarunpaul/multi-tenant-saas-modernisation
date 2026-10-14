# GRILL-0005 — Multi-Tenant SaaS Modernisation Requirements

## Metadata

```yaml
id: REVIEW-REQ-0005
type: requirement
skill: grill
status: completed
date: 2026-10-14
reviewed-artifact: docs/architecture/requirements.md
platform-version: v0.2.3
protocol-version: "1"
execution-mode: canonical
target-sha256: 8ff38e1bbe05238a404b36911dc8bfdf6806618f3cbe5502ab787c6ce61373ea
input-fingerprint: f5fd357e9139ae54f39437f95476c090aa2643ca5ee809a778adf79cae69bd01
supersedes: REVIEW-REQ-0004
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
    "sha256": "8ff38e1bbe05238a404b36911dc8bfdf6806618f3cbe5502ab787c6ce61373ea"
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
- `docs/reviews/grill/requirements/0004-multi-tenant-requirements.md`

The reviewed requirements now incorporate the prior discovery clarifications that independent tenant restore is required and EU/EEA is the prototype residency baseline. No additional user clarification was required to assess whether the remaining validation work can be gated to detailed design or rollout.

## Purpose

Challenge whether the requirements for modernising the database-per-tenant SaaS platform are clear, testable, and current enough to guide detailed architecture and eventual implementation without prematurely prescribing technology.

## Outcome

The requirements now align more closely with the active architecture workflow: their status places the work in detailed design, records the proposed (not authorized) status of ADR-0001, establishes independent tenant restore as required, and makes the EU/EEA prototype residency baseline explicit. The document remains a problem and outcome baseline rather than selecting the target topology.

The requirements are suitable for continuing detailed architecture design, but not for production acceptance or implementation approval. Quantitative targets, testable security/recovery evidence, shard and directory limits, and legacy-backup migration boundaries remain to be validated at explicit gates. A duplicated forward-looking Grill statement in the purpose section should also be clarified to avoid implying that the initial requirements Grill is still pending.

## Confirmed Facts

- The requirements identify the current database-per-tenant model and its operational, cost, schema-management, connection, and observability burdens.
- Tenant isolation is required across identity, APIs, application services, persistence, caches, messaging, background work, telemetry, recovery, and administration.
- Independent tenant restore is explicitly required, with isolation, deletion, residency, neighboring-tenant, and data-integrity protections.
- EU/EEA is the prototype residency baseline for tenant data, replicas, backups, and recovery copies; stricter tenant obligations are to be validated before onboarding the affected tenant or region.
- The requirements call for incremental, observable migration and consider consistency, validation, reconciliation, rollback, partial failure, and operational visibility.
- The updated status records the phase as detailed architecture design and ADR-0001 as proposed, not an authorized production decision.
- ADR-0001 proposes shared-schema shards/database pools as the standard-tenant default, with dedicated placement for justified exceptions.

## Accepted Assumptions

- The scale, throughput, latency, availability, recovery, migration, cost, provisioning, and operational-effort targets in ADR-0001 are prototype/planning inputs, not validated production limits or contractual commitments.
- Workload is materially skewed; high-volume tenants may need throttling, promotion, or dedicated placement.
- EU/EEA is sufficient for the initial prototype, while customer-specific legal, regulatory, and contractual obligations will be checked before affected onboarding.
- The migration point-of-no-return rule recorded in prior reviews is a working design assumption: after a committed target write, recovery must reconcile or move forward rather than blindly route back to the legacy store.
- ADR-0001 is a proposed direction; authorized decision-owner acceptance remains outstanding.

## Material Unknowns

These are explicitly deferred from selecting or validating the current direction, but must be resolved before the indicated gates:

- Target metric provenance, accountable owners, representative workload profiles, measurement windows, and contractual status before production sizing or SLO approval.
- Exact regulatory and contractual obligations before onboarding affected tenants or regions.
- Isolation and tenant-restore proof—including privileged operations, deletion replay, residency, and measured RPO/RTO—before production implementation.
- Legacy backup compatibility versions, import integrity, deletion handling, support duration, and retirement ownership before migration rollout.
- Per-shard capacity and blast-radius limits, tenant-directory availability and stale-routing behavior, and migration write fencing/catch-up consistency during detailed architecture.

These do not prevent the requirements-level direction from proceeding to detailed architecture: the requirement is clear enough to identify the design work and its gates, and the document does not present unvalidated production targets as accepted commitments.

## What Looks Sound

- The purpose section maintains a distinction between requirements, assumptions, and later validation.
- Residency and recovery requirements now express the prototype baseline, restore requirement, and high-level protection constraints clearly.
- The architecture questions ask for restore and residency enforcement/evidence without prematurely prescribing mechanisms.
- Tenant isolation is treated as an end-to-end property, and loss/corruption of tenant context must fail safely.
- Workload skew, performance isolation, tenant mobility, and differentiated tenancy are recognized as material architecture drivers.
- The stated non-assumptions and applicable architecture principles discourage complexity without a specific driver.

## Critical Challenges

### 1. Purpose section still describes the initial Grill as future work

**Issue:** The introduction says requirements have been challenged through Grill, then later says they “will be challenged” before significant architecture or implementation decisions.
**Why it matters:** That wording conflicts with the completed review and the current detailed-design status.
**Question or evidence required:** Reword the latter sentence to describe when future material requirement changes or implementation plans should be grilled, or remove it if redundant.
**Potential consequence:** Teams may misread governance state or duplicate completed requirements discovery.

### 2. Quantitative targets are not a requirements-level acceptance baseline

**Issue:** The requirements describe scale and performance drivers qualitatively; detailed numeric targets currently appear in ADR-0001 as prototype values without recorded source, owner, workload definition, or measurement method.
**Why it matters:** Detailed architecture can explore against provisional inputs, but production sizing and acceptance cannot rely on unverified figures.
**Question or evidence required:** For each target, record provenance, accountable owner, representative workload, measurement window, and whether it is a prototype objective, launch criterion, or contractual SLO.
**Potential consequence:** Shard sizing, capacity forecasts, or service commitments may be based on unrepresentative or unapproved numbers.

### 3. Independent restore is required, but its acceptance evidence is not yet testable

**Issue:** The requirements state what restore must not compromise but leave production RPO/RTO, retention, service tiers, and validation evidence subject to later validation and approval.
**Why it matters:** A shared or sharded store makes tenant recovery and deletion-safe restoration central properties that must be demonstrated, not inferred from topology.
**Question or evidence required:** Define tenant-isolated restore tests, deletion replay, residency proof, integrity checks, measured RPO/RTO, and named approval gates before production adoption.
**Potential consequence:** Recovery could affect neighboring tenants, resurrect deleted data, violate residency, or miss an unapproved but expected objective.

### 4. Isolation and performance boundaries require measurable controls

**Issue:** The requirements identify tenant-context propagation, fail-safe behavior, and noisy-neighbor control, but do not define acceptance tests, privileged support boundaries, per-shard limits, or maximum affected-tenant blast radius.
**Why it matters:** These are essential security and resilience properties for the proposed shared/sharded default.
**Question or evidence required:** Define boundary and negative tests across persistence, cache, messaging, background jobs, restore, and administrative/support paths; establish shard capacity, directory failure, stale-route, and placement criteria in detailed architecture.
**Potential consequence:** Cross-tenant access or shared-resource failures may escape detection until production.

### 5. Legacy backup compatibility needs bounded migration criteria

**Issue:** The requirements call for legacy backup compatibility during migration but do not specify supported formats, import-integrity criteria, deletion behavior, support duration, or retirement ownership.
**Why it matters:** Compatibility affects migration/recovery design, and indefinite format support would create continuing security and operational obligations.
**Question or evidence required:** Set the supported version window, import verification criteria, deletion-safe recovery behavior, and retirement gate before migration rollout.
**Potential consequence:** Legacy tenants may be unrecoverable, deleted data may return, or transitional support may become indefinite.

## Inherited Finding Traceability

| Prior finding from GRILL-0004 | Resolution |
|---|---|
| Requirements phase/status and traceability were stale. | RESOLVES — phase and status now reflect detailed architecture and explicitly retain ADR-0001's proposed state. |
| Independent tenant restore conflicted with the requirements text. | RESOLVES — restore is explicitly required, with protection constraints; detailed production objectives remain open. |
| Quantitative targets lacked provenance, owners, workload, and measurement criteria. | DOES NOT RESOLVE |
| Isolation and recovery lacked verifiable evidence. | PARTIALLY RESOLVES — high-level restore protections are stated; testable evidence and objectives remain open. |
| Regulatory/contractual scope needed a baseline and onboarding gate. | PARTIALLY RESOLVES — EU/EEA baseline and pre-onboarding validation are explicit; accountable owner and evidence criteria remain unspecified. |
| Legacy backup support and deletion behavior were unbounded. | DOES NOT RESOLVE |
| Operational/performance limits and migration controls were not measurable. | DOES NOT RESOLVE |

## Hidden Assumptions

- Aggregate load and largest-tenant peaks can be combined into a representative test profile.
- A five-minute final write-quiesce target recorded in ADR-0001 is achievable for large tenants and high change rates.
- Customer-visible backup/restore behavior can be preserved while formats and tenancy tiers change.
- Stricter placement or isolation can be applied without compromising operational support or migration safety.
- Cost and intervention-reduction outcomes can be compared consistently with a current-state baseline.
- Dedicated shard, dedicated database, and dedicated infrastructure are distinct placement tiers with governed eligibility.

## Missing Non-Functional Requirements

- Reproducible workload profiles and measurement windows for throughput, latency, concurrency, bursts, and noisy-neighbor behavior.
- Per-shard capacity, storage, connection, and maximum tenant/blast-radius limits.
- Tenant-directory availability, recovery, stale-routing, and concurrent placement-change objectives.
- Automated and measurable isolation/recovery tests, including privileged operations, deletion replay, and residency.
- Approved RPO/RTO, retention, and service-tier objectives.
- Legacy backup version support, integrity, migration duration, and retirement criteria.
- Telemetry access, retention, redaction, and cardinality requirements for tenant dimensions.
- Baselines and calculation methods for cost, provisioning, schema rollout, and operational-effort outcomes.

## Failure Scenarios

- Stale placement or tenant context routes a request or background job to the wrong tenant store.
- A hot tenant exceeds shard capacity and degrades neighboring tenants.
- Directory outage or stale cache prevents safe resolution or routes operations to an obsolete placement.
- Migration copy/catch-up loses or duplicates writes, or old workers continue writing after target activation.
- Tenant restore modifies neighboring data, violates residency, misses recovery objectives, or resurrects deleted data.
- Privileged support access bypasses tenant-context enforcement.
- A legacy backup cannot be imported or cannot be proven complete and deletion-safe.
- Tenant telemetry exposes sensitive identifiers or becomes operationally unusable due to uncontrolled cardinality.

## Complexity Assessment

```text
appropriately simple
```

The requirements justify evaluating shared/sharded and dedicated placement because of tenant scale, workload skew, isolation, recovery, and residency. They do not independently justify microservices, Kubernetes, event sourcing, CQRS, distributed transactions, or active-active multi-region operation.

## Decisions Required

| Severity | Decision |
|---|---|
| SIGNIFICANT | Clarify the duplicated Grill timing language in the purpose section. |
| SIGNIFICANT | Establish metric provenance, owners, workload profiles, and measurement criteria before production sizing or SLO approval. |
| SIGNIFICANT | Define and verify tenant-isolated restore, deletion, residency, RPO/RTO, and privileged-access evidence before production adoption. |
| SIGNIFICANT | Establish tenant-isolation tests, directory and shard failure behavior, placement thresholds, and migration fencing/consistency during detailed design. |
| SIGNIFICANT | Bound legacy-backup support and validate import/deletion safety before migration rollout. |
| MINOR | Establish current-state baselines for cost, provisioning, schema rollout, and operational-effort goals. |
| MINOR | Define tenant telemetry access, retention, redaction, and cardinality before operational rollout. |

## Recommendation

```text
PROCEED WITH CONDITIONS
```

The requirements are directionally adequate for continued detailed architecture design. Their updates materially improve status clarity, restore intent, and residency assumptions. They remain insufficient as a production acceptance baseline; numeric targets and security, recovery, capacity, and migration proof must be established at explicit gates. ADR-0001 remains proposed, and this recommendation does not authorize production implementation.

## Conditions

1. Clarify the duplicate Grill timing statement in the requirements purpose section.
2. Keep ADR-0001 clearly proposed until authorized decision-owner acceptance.
3. Record target provenance, owner, workload, and measurement criteria before production sizing or SLO commitments.
4. Define and verify tenant isolation, privileged-access, restore, deletion, residency, RPO, and RTO evidence before production adoption.
5. Define directory availability/stale-routing behavior, shard limits/blast radius, placement thresholds, and migration fencing/catch-up consistency during detailed architecture.
6. Bound legacy backup versions, import integrity, deletion-safe recovery, support duration, and retirement criteria before migration rollout.
7. Establish current-state baselines before claiming cost or operational-effort reductions.

## Resolved During Grill

- Independent tenant restore is now explicit and includes high-level isolation, deletion, residency, neighboring-tenant, and integrity protections.
- EU/EEA is now explicit as the prototype baseline for tenant data and recovery copies; stricter obligations are to be validated before affected onboarding.
- The status now reflects detailed architecture design, identifies ADR-0001 as proposed, and names the tenant directory/placement control plane as the next design area.
- Prior Grill records and ADR-0001 provide prototype planning values and a migration point-of-no-return rule; neither has been independently validated against production evidence here.

## Remaining Follow-Up

- Clarify the redundant purpose-section Grill statement.
- Validate scale, workload, latency, availability, recovery, migration, cost, and operational-effort targets with accountable owners and repeatable methods.
- Define directory behavior, shard limits, tenant placement thresholds, migration fencing, and consistency handling.
- Produce test evidence for cross-tenant isolation, privileged operations, tenant restore, deletion safety, residency, and measured recovery objectives.
- Bound legacy backup support before migration rollout and customer-specific obligations before affected onboarding.

## Next Engineering Activity

Continue detailed architecture decisions and validation, beginning with tenant-directory and placement-control-plane design. Use the explicit prototype targets as provisional inputs, not approved production commitments. Update the purpose wording during requirements maintenance; return to Grill if materially changed requirements alter architecture drivers.

## Suggested Skill Handoff

```text
clarify requirements purpose wording
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
