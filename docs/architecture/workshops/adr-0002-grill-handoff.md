# Grill Handoff — ADR-0002 Scope and Critical Assumptions

**Purpose:** Run a challenge session **before** drafting ADR-0002. This is a working prompt, not a canonical review artifact.

## Instruction to the coding agent

Use the repository's existing `/grill` skill and **Review Execution Protocol v1**. First inspect the skill's local instructions and the platform's canonical-review conventions. Do not invent a review schema, outcome labels, or artifact path. Do not directly edit any managed file under `.engineering/platform/`.

### Inputs to read

1. `docs/architecture/requirements.md`
2. `docs/reviews/grill/requirements/0007-multi-tenant-requirements.md`
3. `docs/architecture/ADRs/0001-multi-tenant-data-topology.md`
4. The accompanying `docs/architecture/workshops/adr-0002-scope-brief.md`.

### Task

Grill the **scope, decision boundary and safety assumptions** for the proposed `docs/architecture/ADRs/0002-tenant-directory-and-placement-control-plane.md`.

**Do not draft ADR-0002 or implement code in this session.** Do not reopen requirements discovery without a demonstrated material gap; do not assume ADR-0001 is accepted.

Work through these concerns, prioritizing high-consequence unknowns:

1. Who is authoritative for tenant placement, and what prevents independent services from changing it?
2. What is the minimum placement record needed to support correct routing, versions/epochs, approved geography, and movement state?
3. Can cached routes be safe during partition or directory outage? Distinguish reads, writes and in-flight operations; identify the actual enforcement point.
4. What happens if the directory switches a tenant from shard S1 to dedicated D1 while an application instance still targets S1?
5. How are concurrent placement-change requests handled, and what does “one active serving placement” mean during transition?
6. Which control-plane guarantees must the later migration/fencing ADR provide before an activation can be committed?
7. What happens on directory outage, partial regional failure, stale replicas, or conflicting metadata observations?
8. What authorization, residency checks, operator approvals and audit evidence must be guaranteed at the architecture level?
9. Which unresolved topics belong in subsequent ADRs rather than ADR-0002?

### Mandatory scenario to challenge

Tenant A has been approved to move from S1 to D1. Directory authority now says D1 is active; one application instance holds cached route S1; the directory is unavailable; that instance receives a **write**.

Compare: **A** use cached S1 until TTL; **B** reject until authority can be checked; **C** permit a cached route only with provable fencing/validity guarantees, otherwise reject. Do not select C merely because it sounds balanced: require a credible enforcement contract and explain the performance/availability trade-offs.

### Interaction rule

Ask only the consequential questions needed to resolve architectural decisions. State a recommendation, alternatives, risks and consequences, but mark unvalidated propositions as assumptions. Avoid detailed schema/API/vendor decisions.

### Output and persistence

- Use the platform's normal Grill workflow to create and verify the canonical review and Execution Manifest, if that workflow supports this type of pre-ADR scope review. If its protocol does not support a scope review, identify the compliant way to capture the result without improvising a canonical record.
- Produce a concise decision log of what is resolved, conditional and deferred.
- State whether scope is ready to become a **Proposed** ADR-0002, what conditions remain, and what later ADRs own the open issues.
- Do not run `/architecture-review` yet; that comes **after** ADR-0002 has been drafted.
- Do not mutate requirements, ADR-0001, or managed platform files as a side effect of this challenge.
