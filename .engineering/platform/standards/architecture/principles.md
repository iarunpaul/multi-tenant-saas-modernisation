# Architecture Principles

## Purpose

Define durable architectural principles for software built using the Agentic Engineering Platform.

These principles guide architecture decisions but do not prescribe a particular technology stack.

## 1. Architecture Follows Business Drivers

Architecture must be driven by:

- business outcomes
- functional requirements
- quality attributes
- regulatory obligations
- operational constraints
- organisational capabilities

Do not introduce architectural complexity without a material driver.

## 2. Prefer the Simplest Viable Architecture

Prefer the least complex architecture that satisfies current known requirements while preserving reasonable evolution paths.

Complexity requires justification.

Examples requiring explicit justification include:

- microservices
- event-driven architectures
- event sourcing
- CQRS
- distributed transactions
- multiple databases
- orchestration engines
- custom frameworks
- multi-agent architectures

Do not solve hypothetical future problems without evidence that they are likely to materialise.

## 3. Make Boundaries Explicit

Systems should have clear:

- domain boundaries
- service responsibilities
- data ownership
- trust boundaries
- deployment boundaries
- integration contracts

Avoid shared ownership of critical responsibilities.

## 4. Data Has an Owner

Every important dataset must have a clearly identifiable owner or source of truth.

Avoid multiple systems independently owning the same business state.

Replication is allowed where justified, but ownership must remain clear.

## 5. Design for Failure

Distributed dependencies can fail.

Architectures must consider relevant failure scenarios such as:

- dependency unavailable
- dependency slow
- network interruption
- duplicate message
- delayed message
- out-of-order message
- partial failure
- expired credentials
- capacity exhaustion

Do not assume infrastructure or external services are always available.

## 6. Explicit Consistency

Consistency requirements must be deliberate.

Where strong consistency is required, state why.

Where eventual consistency is used, define:

- acceptable delay
- failure behaviour
- reconciliation approach
- duplicate handling

Do not use eventual consistency merely because asynchronous messaging is fashionable.

## 7. APIs and Events Are Contracts

Public APIs, integration APIs and events must be treated as contracts.

Changes must consider:

- compatibility
- versioning
- consumers
- migration
- failure semantics

Breaking changes require explicit review and approval.

## 8. Security by Design

Security must be considered during architecture rather than added after implementation.

Architectures should identify:

- identities
- trust boundaries
- sensitive assets
- authorisation boundaries
- secrets
- external exposure
- tenant boundaries

Least privilege should be the default.

## 9. Observability by Design

Systems must provide sufficient evidence to understand:

- whether they are healthy
- whether important operations succeed
- why failures occur
- where latency is introduced

Logging, metrics and tracing should be designed around operational questions rather than collected without purpose.

## 10. Operability Is an Architectural Concern

Architecture decisions must consider:

- deployment
- configuration
- rollback
- recovery
- monitoring
- support
- failure isolation
- capacity

A system that is difficult to operate is not production-ready merely because its functional behaviour is correct.

## 11. Automate Repeatable Operations

Repeatable engineering activities should be automated where reliable automation is practical.

Examples include:

- builds
- tests
- deployment
- security scanning
- dependency checks
- infrastructure validation
- policy verification

Prefer deterministic automation over undocumented manual processes.

## 12. Evolution Over Replacement

Prefer evolutionary architecture where practical.

Design changes so that systems can be migrated incrementally rather than requiring unnecessary large-scale replacements.

Use techniques such as:

- backward-compatible contracts
- staged migrations
- feature flags
- parallel operation

when justified by risk.

## 13. Record Consequential Decisions

Significant architecture decisions should be recorded when they:

- create long-term constraints
- introduce significant technology
- change a system boundary
- change data ownership
- change a security boundary
- involve meaningful trade-offs

Do not create architecture decision records for routine implementation details.

## 14. Portability Where It Matters

Avoid unnecessary lock-in to a particular:

- AI coding agent
- development environment
- proprietary workflow format

Vendor-specific technology may be used when it provides sufficient value.

The goal is deliberate dependency, not vendor avoidance.

## 15. Architecture Must Be Verifiable

Where possible, architectural requirements should have corresponding automated controls.

Examples include:

- architecture tests
- contract tests
- security controls
- policy checks
- dependency rules

Architecture documentation alone is not enforcement.
