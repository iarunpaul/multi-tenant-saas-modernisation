# ADR-0002 — Tenant Directory and Placement Control Plane: Scope Brief

**Status:** Working input for Grill; not an accepted ADR or canonical review.
**Target ADR:** `docs/architecture/ADRs/0002-tenant-directory-and-placement-control-plane.md`
**Project:** Multi-Tenant SaaS Modernisation
**Platform:** Agentic Engineering Platform v0.2.3
**Design phase:** Detailed Architecture Design

## 1. Baseline and dependencies

Read these repository documents before the review:

- `docs/architecture/requirements.md`
- `docs/reviews/grill/requirements/0007-multi-tenant-requirements.md`
- `docs/architecture/ADRs/0001-multi-tenant-data-topology.md`

Treat the latest requirements Grill outcome as **PROCEED WITH CONDITIONS**. ADR-0001 remains **Proposed**. Do not restart requirements discovery unless this review identifies a material requirement gap.

Established design constraints:

- Shared/sharded tenant storage is the default topology; dedicated placement is permitted for justified exceptions.
- An authoritative tenant directory is required for placement resolution.
- Tenant movement between placement tiers must be supportable.
- Independent tenant restore is required.
- EU/EEA is the prototype data-residency baseline.
- Workload, capacity, RPO, and RTO figures remain assumptions until validated.

## 2. Design problem

The data topology requires an authoritative means to identify and control where each tenant's data is served. Directory lookup, cached routing, placement changes and failures can cause unavailability, stale-route writes, cross-tenant isolation failures, or violations of regional placement constraints unless their contracts are explicit.

**Decision boundary:** ADR-0002 determines the logical authority, minimum placement metadata, lookup and cache safety contract, placement versioning and concurrency guarantees, transition-state contract, directory failure behaviour, and placement authorization/audit obligations. It does **not** implement the control plane or fully specify downstream migration and recovery workflows.

## 3. Architecture drivers

1. Correct tenant isolation and prevention of unauthorized data access.
2. Safe routing during steady state, failure, and tenant movement.
3. Availability without treating stale cache entries as intrinsically safe.
4. Controlled placement changes with unambiguous authority and concurrency.
5. EU/EEA residency and approved placement exceptions.
6. Traceable administrative changes and operational evidence.
7. Compatibility with independent tenant recovery and future shard-capacity management.
8. Portability: define architectural contracts before cloud-specific products.

## 4. In-scope decision questions

| ID | Decision area | Question |
| --- | --- | --- |
| D1 | Authority | What is the single logical authority for tenant placement, and who may change it? |
| D2 | Metadata | What minimum attributes identify tenant, approved storage location, version and transition status? |
| D3 | Lookup and caching | Under what conditions may a service use cached placement to serve reads and writes? |
| D4 | Concurrency | How are conflicting updates, stale readers and placement epochs/versions handled? |
| D5 | Transition contract | Which states and safety preconditions govern activation of a new placement? |
| D6 | Failure handling | What must fail closed, what may continue safely, and how is recovery achieved after directory outage? |
| D7 | Governance | Which placement changes require authorization, policy checks and durable evidence? |

## 5. Candidate safety invariants to challenge (not pre-approved)

- Each tenant has no more than one authoritative **active serving placement** at a time; source and target data copies may coexist during migration.
- An operation must resolve to a placement authorized for its tenant and operation type.
- Placement mutations are versioned, concurrency-controlled and auditable.
- A directory metadata update **alone** cannot guarantee safe cutover: the data plane must enforce fencing or an equivalent safety mechanism.
- TTL expiration alone is not proof that a cached route remains safe.
- Residency and isolation constraints apply to placement, transitions and recovery.
- If correctness cannot be established, unsafe operations are blocked rather than silently routed.

## 6. Explicit exclusions and follow-up ownership

- **Tenant migration ADR:** transfer protocol, write fencing implementation, synchronization, rollback and reconciliation; ADR-0002 defines necessary handoff/activation conditions.
- **Tenant recovery ADR:** tenant-scoped backups, restore workflow, PITR and RPO/RTO validation; ADR-0002 defines the placement-control integration contract.
- **Shard/capacity ADR:** sizing, balancing, hotspot management, blast-radius limits and resharding algorithms.
- **Placement policy decision:** promotion/demotion criteria, thresholds and detailed commercial/regulatory eligibility.
- **Security design:** fine-grained IAM mechanisms and enforcement technology; ADR-0002 still defines authorization obligations.
- **Implementation design:** vendors, specific services, database schema, endpoints, IaC and deployment topology.

## 7. First high-impact Grill scenario

Tenant A is currently served from shared shard **S1**. An approved change moves it to dedicated database **D1**. The directory records D1 as active, but some application instances hold S1 in cache. During a directory outage, an instance receives a write for Tenant A.

Challenge these options:

- **A — Availability-first:** continue using cached S1 until TTL expiry.
- **B — Strict verification:** reject the write unless current authority can be verified.
- **C — Conditional cached routing:** allow cached routing only if the system can establish enforceable route validity/fencing; otherwise block the write.

**Initial recommendation for challenge, not decision:** C. Distinguish read from write semantics; do not assume a lease, version, TTL or token is adequate without verifying the enforcing party and its failure behaviour.

## 8. Required review output

The Grill should yield: (1) an explicit decision boundary; (2) selected or conditionally recommended approach and rejected alternatives; (3) challenged assumptions; (4) safety invariants; (5) open questions and evidence needed; (6) downstream ADR dependencies; and (7) a clear proceed/revise/escalate recommendation **using the platform's actual review conventions**.

Do not silently promote ADR-0001 or ADR-0002 to Accepted.
