# Multi-Tenant SaaS Modernisation — Architecture Requirements

## Purpose

Define the architectural requirements, constraints, assumptions and unresolved questions for modernising a large-scale database-per-tenant SaaS platform into a more scalable multi-tenant architecture.

This document is intentionally focused on the problem and required outcomes.

It must not prematurely prescribe the target architecture.

The requirements defined here will be challenged through the platform `grill` workflow before significant architecture or implementation decisions are made.

---

## Business Context

The existing SaaS platform has evolved around a database-per-customer model.

As the tenant estate has grown, this architecture has created increasing operational and engineering challenges, including:

- database provisioning overhead
- schema-upgrade complexity
- operational burden across a very large database estate
- infrastructure cost
- connection and resource management complexity
- difficult platform-wide maintenance
- increased observability complexity
- slow rollout of platform-level changes
- operational difficulty performing cross-tenant analysis
- increasing difficulty scaling engineering and support processes

The modernisation must reduce these constraints without weakening tenant isolation, security, reliability or recoverability.

---

## Business Outcomes

The modernised platform should:

1. support continued growth in the tenant estate
2. reduce infrastructure and database-management overhead
3. reduce the operational cost of platform-wide schema and application changes
4. improve deployment and upgrade velocity
5. maintain strong tenant isolation
6. be backwards compatible including taking and restoring backups
7. maintain or improve platform availability
8. provide safe migration from the existing architecture
9. improve operational visibility across the platform
10. enable differentiated tenancy models where justified
11. support future evolution without requiring another large-scale redesign

---

## Current-State Assumptions

The following are assumptions and must be validated.

### ASSUMPTION-001 — Database Per Tenant

Each tenant currently has a logically independent database.

### ASSUMPTION-002 — Large Tenant Estate

The existing platform operates a sufficiently large number of tenant databases for database lifecycle management to create material operational complexity.

### ASSUMPTION-003 — Shared Application Platform

Multiple tenants are served by a common application platform even though their persistence is isolated.

### ASSUMPTION-004 — Heterogeneous Tenant Workloads

Tenants may differ significantly in:

- data volume
- transaction rate
- concurrency
- integration usage
- retention requirements
- performance characteristics

### ASSUMPTION-005 — Incremental Migration

Migration cannot reasonably be performed as a single platform-wide cutover.

### ASSUMPTION-006 — Backwards Compatibility Matters

Existing APIs, integrations and client behaviour cannot be broken casually during migration.

### ASSUMPTION-007 — Tenant Isolation Is Mandatory

A tenant must not gain unauthorised access to another tenant's data or operations.

---

## Architecture Drivers

The following drivers are expected to materially influence the target architecture.

### Tenant Isolation

Tenant identity and boundaries must remain explicit throughout the system.

Isolation must be considered across:

- authentication
- authorisation
- APIs
- application services
- persistence
- caches
- messaging
- background processing
- telemetry
- backup and restore
- administrative tooling

Tenant isolation must not depend solely on developers remembering to include a tenant filter.

---

### Scalability

The architecture must scale to a large tenant population without requiring operational effort proportional to the number of tenants.

Scaling must consider:

- tenant count
- request volume
- data volume
- concurrent users
- database connections
- background processing
- messaging throughput
- cache usage

---

### Operational Simplicity

Routine platform operations should become easier rather than merely shifting complexity elsewhere.

Examples include:

- tenant provisioning
- schema changes
- deployments
- monitoring
- backups
- incident response
- tenant migration
- capacity management

---

### Cost Efficiency

The target architecture should reduce unnecessary infrastructure and operational cost.

Cost optimisation must not compromise:

- security
- reliability
- recoverability
- performance isolation

---

### Migration Safety

Migration from the current architecture must support controlled, incremental rollout.

The migration design should consider:

- tenant-by-tenant migration
- compatibility during transition
- validation and reconciliation
- rollback
- partial failure
- data consistency
- migration observability

---

### Availability and Resilience

Failure of an individual tenant, workload or infrastructure component should not unnecessarily affect unrelated tenants.

The architecture should consider:

- fault containment
- retry behaviour
- transient failures
- dependency failures
- regional or infrastructure failures
- noisy-neighbour scenarios

---

### Security

The architecture must provide clear trust and isolation boundaries.

Security requirements include:

- authenticated tenant identity
- authorised tenant access
- protection from cross-tenant data access
- secure service-to-service communication
- secrets management
- auditability
- least privilege

---

### Observability

Operations must support both platform-wide and tenant-specific diagnostics.

Telemetry should support:

- request correlation
- tenant correlation
- latency analysis
- dependency failures
- error rates
- capacity analysis
- tenant-specific incident investigation

Tenant identifiers used in telemetry must comply with security and privacy requirements.

---

### Maintainability

The target architecture should reduce unnecessary complexity and support evolutionary change.

The architecture should avoid introducing distributed-system complexity unless justified by measurable requirements.

---

### Performance Isolation

A high-volume or poorly behaving tenant should not be able to materially degrade the service experienced by unrelated tenants.

Potential mechanisms may include:

- resource quotas
- throttling
- workload isolation
- database partitioning
- queue isolation
- dedicated infrastructure tiers

The correct mechanisms have not yet been selected.

---

### Data Residency and Compliance

The architecture must be capable of supporting applicable regulatory and contractual requirements.

Potential requirements may include:

- geographical data placement
- retention
- deletion
- auditability
- encryption
- tenant-specific contractual constraints
- region specific customer data laws and regulations

Exact requirements remain to be confirmed.

---

### Backup and Recovery

The target architecture must provide a clear recovery model.

The architecture must determine whether recovery is required at:

- platform level
- database or shard level
- tenant level
- individual dataset level

Per-tenant restore requirements are currently unresolved.

---

## Tenant Context Requirements

Every tenant-aware operation must have an explicit and trusted tenant context.

Tenant context may originate from authenticated identity, request routing or trusted internal processing.

The platform must prevent tenant identifiers supplied by an untrusted client from becoming authoritative without validation.

Tenant context must propagate correctly through:

```text
HTTP request
    ↓
authentication
    ↓
tenant resolution
    ↓
authorisation
    ↓
application services
    ↓
persistence
    ↓
cache
    ↓
events / messages
    ↓
background processing
    ↓
telemetry
```

Loss or corruption of tenant context must fail safely.

---

## Data Requirements

The target persistence model must support explicit tenant ownership of tenant-scoped data.

The architecture must evaluate:

- tenant partitioning
- indexing
- query performance
- connection management
- data growth
- hot tenants
- archival
- schema evolution
- tenant migration
- backup and restore
- data residency
- isolation guarantees

The architecture must not assume that one persistence topology is appropriate for every tenant.

---

## Migration Requirements

Migration must be incremental and observable.

A tenant migration should have clearly defined states such as:

```text
Not Migrated
    ↓
Preparing
    ↓
Migrating
    ↓
Validating
    ↓
Cutover
    ↓
Completed
```

Failure states and rollback paths must also be defined.

Migration should support:

- explicit tenant selection
- repeatable execution
- idempotent migration operations where practical
- reconciliation
- validation before cutover
- operational visibility
- safe rollback or recovery

---

## Candidate Tenancy Models

The following models must be evaluated before selecting a target.

### Model A — Database Per Tenant

Each tenant retains a dedicated database.

Potential advantages:

- strong physical isolation
- simple tenant-level backup and restore
- reduced blast radius
- easier tenant-specific customisation

Potential concerns:

- infrastructure overhead
- upgrade complexity
- connection management
- provisioning overhead
- high operational cost at large scale

---

### Model B — Shared Database / Shared Schema

Multiple tenants share the same database and tables.

Tenant ownership is represented using a tenant identifier.

Potential advantages:

- efficient resource utilisation
- simplified schema upgrades
- reduced database count
- easier platform-wide operations

Potential concerns:

- cross-tenant access risk
- noisy-neighbour behaviour
- tenant-level restore complexity
- very large tables and indexes
- blast-radius concerns

---

### Model C — Shared Database / Schema Per Tenant

Tenants share a database while having separate database schemas.

Potential advantages:

- stronger logical separation than shared tables
- fewer physical databases

Potential concerns:

- large schema counts
- schema migration complexity
- tooling and ORM limitations
- continued operational overhead

---

### Model D — Tenant Shards / Database Pools

Multiple tenants are assigned to database shards or pools.

Tenant placement is controlled through metadata or a tenant directory.

Potential advantages:

- reduced database count
- bounded blast radius
- horizontal scaling
- tenant movement between shards
- better workload isolation than a single shared database

Potential concerns:

- shard routing
- tenant placement
- rebalance operations
- shard-aware operational tooling
- cross-shard querying

---

### Model E — Hybrid Tenancy

Different tenant categories use different persistence models.

For example:

```text
standard tenants
    → shared / sharded infrastructure

large tenants
    → dedicated shard or database

regulated tenants
    → dedicated infrastructure where required
```

Potential advantages:

- cost efficiency for normal tenants
- stronger isolation for exceptional tenants
- ability to support heterogeneous workloads

Potential concerns:

- operational complexity
- multiple supported architectures
- tenant placement policy
- migration between tenancy tiers

---

## Architecture Questions to Resolve

The Grill and architecture review must address at least the following questions:

1. What tenant scale must the platform support?
2. What transaction and concurrency scale must be supported?
3. What tenant isolation guarantees are required?
4. Can tenant data share physical storage?
5. Are there regulated or high-value tenants requiring dedicated infrastructure?
6. Is per-tenant backup and restore required?
7. What migration downtime is acceptable?
8. What rollback guarantees are required?
9. What consistency guarantees are required during migration?
10. How should tenant context be established and propagated?
11. How should background jobs retain tenant context?
12. How should messages and events identify tenant ownership?
13. How should cache keys prevent cross-tenant collision?
14. How should tenant-specific throttling work?
15. How should noisy neighbours be controlled?
16. What data residency requirements exist?
17. How should hot tenants be moved between infrastructure partitions?
18. How should cross-tenant analytics operate?
19. What failure blast radius is acceptable?
20. Which operational problems provide the largest business benefit if solved first?

---

## Explicit Non-Assumptions

The following technologies or patterns are not automatically required:

- microservices
- Kubernetes
- service mesh
- CQRS
- event sourcing
- Kafka
- distributed databases
- multi-region active-active architecture
- complex multi-agent development workflows

They may be introduced only where architectural drivers justify them.

---

## Initial Constraints

The first architecture iteration should:

- remain technology-aware but not technology-driven
- prefer evolutionary migration over replacement
- minimise irreversible decisions
- preserve existing tenant behaviour where practical
- make tenant boundaries explicit
- keep operational support realistic
- favour measurable quality attributes over architectural fashion

---

## Success Criteria

The architecture discovery phase is successful when:

- major assumptions have been validated or explicitly retained as assumptions
- tenant-isolation requirements are clear
- target scale is understood
- migration constraints are defined
- tenancy models have been compared
- major risks are identified
- unresolved blockers are explicit
- a preferred architecture direction can be justified
- consequential decisions can be captured in ADRs

---

## Current Status

```text
Phase: Architecture Discovery
Next Activity: Grill — Requirements
Architecture Decision: Not yet made
Implementation Status: Not started
```
