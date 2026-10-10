# Testing Standard

## Purpose

Define organisational expectations for software verification.

Testing should provide meaningful evidence that software behaves correctly and safely.

## Principles

Testing should be:

- risk-based
- repeatable
- deterministic where practical
- automated where valuable
- focused on behaviour rather than implementation details

## 1. Risk-Based Testing

Testing effort should reflect:

- business criticality
- complexity
- blast radius
- security sensitivity
- financial impact
- data impact
- regulatory impact
- external dependencies

Not every component requires the same testing depth.

## 2. Test at the Lowest Reliable Level

Prefer the cheapest test level that reliably proves the behaviour.

Potential levels include:

- unit
- component
- integration
- contract
- end-to-end
- architecture
- security
- performance
- resilience
- deployment

Do not unnecessarily move behaviour into slow end-to-end tests.

## 3. Behaviour Over Implementation

Tests should primarily verify externally meaningful behaviour.

Avoid tests tightly coupled to:

- private methods
- internal implementation sequence
- incidental object structure

Refactoring should not unnecessarily require rewriting large portions of the test suite.

## 4. Test Important Boundaries

Prioritise verification at boundaries including:

- external APIs
- persistence
- message brokers
- authentication
- authorisation
- external services
- domain boundaries

## 5. Failure Testing

Relevant failure paths should be tested.

Examples include:

- invalid input
- dependency failures
- timeouts
- duplicate messages
- retries
- unavailable infrastructure
- concurrency conflicts
- partial failure

## 6. Contract Testing

External contracts should be verified where feasible.

Relevant contracts include:

- REST APIs
- events
- message schemas
- third-party integration contracts

Consumer compatibility should be considered before releasing breaking changes.

## 7. Security Testing

Security-sensitive behaviour must include appropriate tests.

Examples include:

- authorisation
- tenant isolation
- input validation
- access control
- privilege boundaries

Automated security scanners supplement but do not replace behavioural security tests.

## 8. Test Isolation

Tests should avoid unnecessary dependencies on:

- execution order
- shared mutable state
- real production systems
- arbitrary delays

Tests should produce repeatable outcomes.

## 9. Test Data

Test data must not include production secrets or unnecessarily sensitive production data.

Synthetic or appropriately sanitised data should be preferred.

## 10. Code Coverage

Code coverage may be used as an indicator.

It must not be treated as proof of software correctness.

Do not write meaningless tests purely to increase coverage percentages.

## 11. Flaky Tests

Flaky tests must not be accepted indefinitely.

When a test is unreliable:

- identify the cause
- fix it
- or quarantine it temporarily with explicit ownership

Do not repeatedly rerun failing tests until they happen to pass.

## 12. Test Failures

Failing tests must not be ignored without a documented reason and explicit approval where required.

## 13. Verification Reporting

Agents and developers must distinguish:

- tests actually executed
- tests inferred to exist
- tests recommended but not executed

Never claim successful verification that was not performed.
