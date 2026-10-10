# Test

## Purpose

Provide risk-based evidence that a change behaves correctly and does not introduce unacceptable regressions.

Testing exists to build confidence, not maximise test count.

## When to Use

Use for:

- new functionality
- defect fixes
- refactoring
- contract changes
- integration changes
- security-sensitive behaviour
- infrastructure changes where verification is possible

## Workflow

### 1. Identify Behaviour

Determine what behaviour must be proven.

Include:

- expected paths
- important edge cases
- failure paths
- security-relevant behaviour
- compatibility behaviour where applicable

### 2. Assess Risk

Consider:

- business impact
- change complexity
- blast radius
- external integrations
- state mutation
- security sensitivity
- concurrency
- financial impact
- regulatory impact

Higher-risk behaviour requires stronger evidence.

### 3. Choose Appropriate Test Level

Use the cheapest reliable level.

Possible levels:

```text
unit
component
integration
contract
end-to-end
architecture
performance
security
resilience
deployment
```

Do not push behaviour to end-to-end tests when a lower level can verify it reliably.

### 4. Test Boundaries

Prioritise tests around:

- domain boundaries
- API contracts
- persistence
- external integrations
- asynchronous messaging
- authorisation
- concurrency
- failure handling

### 5. Test Failure Behaviour

Where relevant verify:

- dependency failure
- timeouts
- retries
- duplicates
- malformed input
- invalid state
- unavailable infrastructure
- partial failure

### 6. Avoid Fragile Tests

Tests should not depend unnecessarily on:

- implementation details
- timing assumptions
- test execution order
- mutable shared state
- arbitrary delays

### 7. Execute Applicable Verification

Run applicable tests and report actual outcomes.

Never state that a test suite passes if it was not executed.

## Output

### Coverage of Behaviour

Describe what important behaviour is tested.

### Tests Added or Changed

Summarise meaningful additions.

### Verification Results

Report commands or validation performed and result.

### Gaps

Identify important behaviour that remains unverified.

### Assessment

Conclude with:

```text
SUFFICIENT EVIDENCE
SUFFICIENT WITH KNOWN GAPS
INSUFFICIENT EVIDENCE
```

## Behaviour Rules

Do not optimise for code coverage percentage alone.

Do not test trivial implementation details solely to increase metrics.

Prefer meaningful behavioural evidence.

