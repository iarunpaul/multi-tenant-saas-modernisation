# ADR-0001 — Multi-Tenant Data Topology

## Status

Proposed

## Context

The existing SaaS platform uses a database-per-tenant persistence model.

The tenant estate is expected to grow from approximately 100,000 tenants to 250,000–300,000 tenants over the next 3–5 years.

The current database-per-tenant model provides strong isolation and simple tenant-level recovery, but creates increasing operational and engineering overhead as the estate grows.

The modernization aims to reduce operational complexity and cost while preserving tenant isolation, recoverability, migration safety, availability and regulatory constraints.

The requirements discovery established the following working targets and constraints:

```text
Tenant population:
~100,000 current
250,000–300,000 target over 3–5 years

Workload:
10,000–20,000 aggregate TPS sustained
~30,000 TPS short burst
500–1,000 TPS peak for largest tenants

Interactive API latency:
P95 < 300 ms
P99 < 750 ms

Availability:
99.95% standard tenants
99.99% for higher service tiers where justified

Recovery:
tenant-level restore required
RPO 15 minutes
RTO 4 hours for standard tenants

Migration:
tenant-by-tenant
online copy/catch-up where practical
maximum final write-quiesce target: 5 minutes

Residency:
GDPR baseline
EU/EEA data residency by default
tenant-specific regional placement must be supported

Dedicated tenancy:
required for some regulatory or contractual cases
may also be used for tenants exceeding shared-platform workload thresholds

Modernization outcomes:
>= 40% reduction in infrastructure/database operating cost per tenant
new tenant provisioning under 5 minutes
shared/sharded schema rollout under 2 hours
>= 60% reduction in manual tenant-database operational interventions
```

These values are prototype targets and must be validated against production baselines before real adoption.

The platform must also preserve customer-visible backup and restore behavior while allowing the internal backup implementation to change.

Legacy database-per-tenant backup formats are transitional migration inputs rather than permanent platform contracts.

## Decision Drivers

The target data topology must balance:

- tenant isolation
- operational scalability
- cost efficiency
- tenant-level recovery
- workload isolation
- data residency
- incremental migration
- failure blast radius
- schema-management complexity
- observability
- tenant mobility
- platform evolution

No single driver should dominate without considering its impact on the others.

## Migration Safety Constraint

Migration rollback semantics are defined as follows:

```text
Before cutover:
rollback to the legacy database is permitted.

During final quiesce:
writes are not accepted.

After routing switches to the target store:
the target store becomes the candidate system of record.

After the first committed write is accepted by the target store:
routing back to the legacy database is not considered a safe rollback.

Recovery after this point must use reconciliation,
forward recovery or controlled corrective migration.
```

This creates an explicit point of no return and avoids silently losing acknowledged writes during rollback.

## Considered Options

### Option A — Database Per Tenant

Each tenant continues to use a dedicated physical database.

#### Advantages

- strongest database-level isolation
- simple tenant-specific backup and restore
- small tenant-specific blast radius
- straightforward tenant-level migration
- independent database-level maintenance where needed

#### Disadvantages

- very large database count
- high provisioning and lifecycle-management overhead
- schema upgrade complexity
- large connection-management footprint
- expensive monitoring and operational tooling
- difficult fleet-wide maintenance
- cost scales poorly with tenant count
- many operational processes remain proportional to the number of tenants

#### Assessment

This model preserves several useful properties but does not sufficiently address the principal modernization drivers.

It remains appropriate for exceptional tenants but should not remain the default topology for the full tenant estate.

---

### Option B — Shared Database / Shared Schema

Multiple tenants share the same database and tables.

Tenant ownership is represented by an explicit tenant identifier such as:

```text
TenantId
```

#### Advantages

- significantly reduced database count
- efficient infrastructure utilization
- simplified schema management
- fast platform-wide upgrades
- simpler connection management
- lower provisioning overhead
- potentially strong cost efficiency

#### Disadvantages

- increased consequence of tenant-isolation defects
- tenant-level restore becomes substantially more complex
- large-table and index growth
- greater noisy-neighbor risk
- potentially large failure blast radius
- hot tenants can distort shared-resource usage
- tenant migration and relocation become more difficult
- regional placement flexibility may be constrained

#### Assessment

This model may be appropriate within bounded tenant pools, but a single shared database for the entire platform creates excessive recovery, workload-isolation and blast-radius concerns.

It should not be used as a single global persistence topology.

---

### Option C — Shared Database / Schema Per Tenant

Multiple tenants share a database while each tenant has a separate logical database schema.

#### Advantages

- stronger logical separation than shared tables
- fewer physical databases than database-per-tenant
- some tenant-level operational separation
- potentially easier tenant extraction than fully shared tables

#### Disadvantages

- very large schema counts at the target tenant population
- schema migration remains proportional to tenant count
- ORM and tooling complexity
- operational metadata overhead
- limited reduction in lifecycle-management complexity
- does not sufficiently eliminate the scaling problem of tenant-specific schema management

#### Assessment

At hundreds of thousands of tenants, schema-per-tenant moves the current scaling problem rather than removing it.

This option is rejected as the strategic default.

---

### Option D — Tenant Shards / Database Pools

Tenants are grouped into bounded databases or database pools.

A tenant-placement directory resolves each tenant to its current shard.

Example:

```text
Tenant
   ↓
Tenant Directory
   ↓
Shard / Pool
   ↓
Shared tenant-aware schema
```

#### Advantages

- significantly reduces database count
- bounds failure blast radius
- supports horizontal data-plane scaling
- provides better workload isolation than one global database
- enables tenant movement between shards
- allows capacity to be added incrementally
- simplifies schema management compared with database-per-tenant
- supports regional shard placement
- can support hot-tenant detection and relocation

#### Disadvantages

- requires tenant-routing metadata
- requires shard placement and rebalance logic
- tenant movement becomes an operational capability
- cross-shard queries are more complex
- tenant-level restore requires explicit recovery tooling
- incorrect routing could create severe tenant-isolation failures
- shard capacity management becomes a platform responsibility

#### Assessment

This model addresses the majority of modernization drivers while retaining bounded failure domains.

It provides a strong default topology for standard tenants.

---

### Option E — Hybrid Tenancy

The platform supports multiple placement models based on tenant characteristics.

Example:

```text
Standard tenants
    ↓
Shared shard / database pool

High-workload tenants
    ↓
Dedicated shard or database

Regulated / contractual tenants
    ↓
Dedicated database
    or approved dedicated infrastructure where required
```

Tenant placement is governed by platform metadata and policy.

#### Advantages

- cost-efficient default for most tenants
- supports heterogeneous workloads
- preserves stronger isolation where justified
- allows large tenants to avoid noisy-neighbor constraints
- allows regulatory or contractual placement
- supports gradual migration from database-per-tenant
- avoids forcing every tenant into the same physical topology
- allows tenancy models to evolve independently

#### Disadvantages

- platform must operate multiple placement models
- tenant-routing logic becomes critical infrastructure
- promotion and demotion criteria must be governed
- migration between placement models requires reliable tooling
- recovery procedures may differ between placement models
- operational tooling becomes more sophisticated than a single-topology design

#### Assessment

The additional complexity is justified by the highly skewed workload profile, regulatory constraints and need for incremental modernization.

## Decision

Adopt a **hybrid multi-tenant data topology**, with **sharded / pooled databases as the default model for standard tenants**.

The target logical model is:

```text
                    Tenant Request
                          │
                          ▼
                   Tenant Resolution
                          │
                          ▼
                   Tenant Directory
                          │
             ┌────────────┴─────────────┐
             │                          │
             ▼                          ▼
      Shared Tenant Shard        Dedicated Database
             │                          │
      standard tenants           exceptional tenants
```

The default placement model is:

```text
Standard tenants
    → shared tenant-aware shard

Large / hot tenants
    → dedicated shard or database where thresholds justify it

Regulated / contractually isolated tenants
    → dedicated database

Future exceptional cases
    → dedicated infrastructure only when explicitly justified
```

A single global shared database is not selected.

Schema-per-tenant is not selected as a strategic target.

Database-per-tenant remains supported as a transitional and exceptional placement model rather than the platform default.

## Tenant Directory

The architecture requires a tenant directory as authoritative placement metadata.

The directory must resolve at least:

```text
TenantId
PlacementType
Region
ShardOrDatabase
ServiceTier
ResidencyPolicy
MigrationState
```

Potential additional metadata may include:

```text
RecoveryTier
WorkloadClass
IsolationClass
PlacementVersion
```

The tenant directory is control-plane metadata.

It must not become a new location for tenant business data.

## Tenant Context

Every tenant-scoped operation must operate with a validated tenant context.

Tenant context must propagate across:

```text
request
  ↓
authentication
  ↓
tenant resolution
  ↓
authorisation
  ↓
application logic
  ↓
database access
  ↓
cache
  ↓
events / messages
  ↓
background processing
  ↓
telemetry
```

Tenant identifiers supplied directly by untrusted clients must not become authoritative without validation.

Loss of tenant context must fail closed.

## Shared-Schema Isolation

Where multiple tenants share a shard, tenant ownership must be explicit in tenant-scoped data.

Example:

```text
TenantId
```

Application-level filtering alone must not be treated as sufficient evidence of tenant isolation.

The implementation should seek defence-in-depth through mechanisms such as:

- tenant-aware repository/data-access abstractions
- database-level constraints where practical
- tenant-aware indexing
- tenant-aware test suites
- architecture tests
- controlled administrative access
- tenant-bound cache keys
- tenant-aware message contracts

The exact database enforcement mechanism remains an implementation decision.

## Tenant Placement

Tenant placement must be policy-driven rather than ad hoc.

Placement criteria should eventually consider:

```text
regulatory requirement
contractual isolation requirement
region / residency
storage volume
transaction throughput
latency profile
burst behaviour
operational risk
commercial service tier
```

The following principle applies:

> Customer preference alone does not imply dedicated placement unless the commercial service tier explicitly includes that capability.

Exact promotion and demotion thresholds remain to be defined and validated through workload testing.

## Hot-Tenant Handling

The architecture must assume that tenant workloads are highly skewed.

A small number of tenants may generate a disproportionate amount of:

- transactions
- storage
- background processing
- integration traffic
- database load

The platform must support:

```text
detect
  ↓
classify
  ↓
throttle or isolate
  ↓
move tenant when justified
```

Tenant movement between shards or from shared to dedicated placement is therefore an architectural capability, not merely an operational edge case.

## Regional Placement

Shards and dedicated databases must be deployable within approved geographic regions.

Tenant placement metadata must control region assignment.

For the initial prototype:

```text
EU/EEA tenants
    → approved EU/EEA region

other regions
    → later-validation item
```

Primary data, replicas, backups and recovery copies must respect the tenant's approved residency policy.

Cross-region tenant movement requires an explicit controlled migration.

## Tenant-Level Recovery

Independent tenant recovery remains a mandatory requirement.

The target architecture must demonstrate that a single tenant can be restored without reverting or exposing neighboring tenants.

For shared shards, tenant restore may use a workflow such as:

```text
restore shard backup to isolated recovery environment
        ↓
identify tenant-scoped data
        ↓
extract tenant data
        ↓
reconcile deletion state
        ↓
validate integrity
        ↓
restore into target placement
        ↓
verify
        ↓
reactivate tenant
```

The architecture must preserve:

```text
RPO: 15 minutes
RTO: 4 hours
```

for standard tenants as a prototype target.

These targets must be proven through recovery testing rather than documentation alone.

## Deletion and Restore Safety

Deleted tenant data may remain temporarily in immutable backups until backup expiry.

Standard backup retention is assumed to be 35 days.

Active production deletion must complete within 30 days unless another legal or contractual rule applies.

A restore must not resurrect data that was deleted after the backup was created.

The recovery process must therefore preserve or replay durable deletion state.

The exact deletion-ledger or tombstone mechanism will be determined during implementation design.

## Migration Model

Migration remains tenant-specific and incremental.

A conceptual migration state model is:

```text
Not Migrated
    ↓
Preparing
    ↓
Copying
    ↓
Catching Up
    ↓
Quiesced
    ↓
Final Validation
    ↓
Cutover
    ↓
Activated
    ↓
Post-Cutover Verification
```

Failure and recovery states must also be represented explicitly.

Bulk copy and catch-up should occur while the tenant remains active where practical.

Final cutover may quiesce writes for up to five minutes.

Before `Activated`, rollback to the legacy database is permitted.

After the first successful committed write on the target system, migration recovery must use forward reconciliation rather than routing blindly back to the legacy database.

## Legacy Backup Compatibility

Customer-visible backup and restore behavior must remain available.

The modernized platform is not required to use the legacy backup format internally.

During migration, legacy database-per-tenant backups must have a supported import or recovery path.

Conceptually:

```text
legacy backup
    ↓
isolated restore
    ↓
validation
    ↓
transformation / migration
    ↓
target tenant placement
    ↓
integrity verification
```

Legacy backup-format support is transitional.

Its supported versions and retirement date must be explicitly defined later.

## Cross-Tenant Analytics

Operational telemetry may contain tenant identifiers where required for authorised:

- support
- capacity management
- incident investigation
- service health analysis

Cross-tenant business analytics should use aggregated or de-identified data by default.

Direct cross-tenant analytical workloads should not be allowed to compromise the transactional isolation model.

A separate analytics path may be introduced later if justified.

## Consequences

### Positive

The decision:

- substantially reduces the number of databases that must be managed
- maintains bounded failure domains
- supports tenant-level workload differentiation
- preserves dedicated placement where genuinely required
- supports incremental migration
- supports regional placement
- enables tenant mobility
- provides a route to materially lower operating cost
- avoids one global database becoming the entire platform's failure domain
- avoids schema-per-tenant scaling problems

### Negative

The platform must now implement and operate:

- tenant routing
- placement metadata
- shard capacity management
- tenant movement
- tenant-scoped recovery
- migration orchestration
- workload classification
- routing correctness controls
- multiple placement types

These capabilities introduce meaningful control-plane complexity.

The complexity is accepted because the target scale and heterogeneous workload make a single physical tenancy model unsuitable.

## Risks

### Cross-Tenant Data Access

Incorrect tenant resolution, routing or filtering could expose another tenant's data.

Mitigation must include automated tenant-boundary testing and defence-in-depth controls.

### Noisy Neighbours

A large tenant may consume disproportionate shared resources.

Mitigation requires workload monitoring, quotas or throttling, and relocation mechanisms.

### Tenant Directory Failure

The tenant directory becomes critical routing infrastructure.

Its availability, caching and failure semantics must be addressed in subsequent architecture design.

### Recovery Complexity

Tenant-level recovery from a shared shard is more complex than restoring a dedicated database.

Recovery objectives must therefore be proven through automated or regularly exercised recovery tests.

### Migration Complexity

Tenant movement between database topologies introduces risks of:

- missed data
- duplicated data
- stale routing
- partial migration
- rollback ambiguity

Migration state must be explicit and observable.

### Operational Complexity

Hybrid tenancy is more complex to operate than a single shared database.

The architecture must ensure that automation removes more operational burden than the hybrid topology introduces.

## Rejected Directions

### One Global Shared Database

Rejected because the likely blast radius, hot-tenant risk, tenant-level recovery complexity and regional-placement constraints are too large for the target estate.

### Schema Per Tenant

Rejected because hundreds of thousands of schemas would preserve much of the lifecycle-management problem that the modernization is intended to solve.

### Universal Database Per Tenant

Rejected as the default because it does not sufficiently address the operational and cost drivers.

It remains valid for exceptional tenants.

### Dedicated Infrastructure for Every Premium Tenant

Not selected.

Dedicated infrastructure requires stronger justification than a commercial preference alone and may be introduced only where regulatory, contractual, resilience or workload requirements warrant it.

## Validation Required

This ADR establishes an architecture direction, not proof that the design satisfies the requirements.

The following must be validated before production adoption:

1. current tenant estate and growth baseline
2. actual workload distribution
3. shard sizing and capacity model
4. large-tenant promotion thresholds
5. tenant movement performance
6. tenant-level restore against the RPO/RTO target
7. noisy-neighbor isolation
8. migration catch-up and five-minute cutover
9. post-cutover reconciliation behavior
10. regional placement enforcement
11. schema rollout time
12. provisioning time
13. operating-cost reduction
14. manual-operation reduction
15. availability measurement and tier boundaries

## Follow-Up Decisions

The following decisions should be captured separately when sufficient evidence exists:

```text
ADR — Tenant identity and tenant-context propagation
ADR — Tenant directory and placement control plane
ADR — Shared-shard isolation enforcement
ADR — Tenant migration and reconciliation
ADR — Tenant-level backup and recovery
ADR — Regional data placement
```

Do not create all of these ADRs immediately.

Create them when the relevant decision becomes consequential.

## Next Step

Run the platform architecture review against this decision.

Expected workflow:

```text
ADR-0001
    ↓
architecture-review
    ↓
resolve significant findings
    ↓
implementation-plan
    ↓
grill implementation-plan
```

Implementation should not begin until the architecture review confirms that the chosen topology adequately addresses the identified isolation, migration, recovery, residency and scalability drivers.
