# Architecture Review

## Purpose

Evaluate whether a proposed or implemented architecture is appropriate for its architectural drivers, constraints and organisational standards.

Architecture Review is evidence-based.

It does not reward architectural complexity.

## When to Use

Use for:

- new services or systems
- significant architectural changes
- new integration patterns
- major data-boundary changes
- new infrastructure patterns
- significant migration designs
- technology adoption decisions

Do not require a full architecture review for routine implementation changes with no meaningful architectural impact.

## Inputs

Review available:

- requirements
- Grill findings
- architecture diagrams or descriptions
- source code where relevant
- architectural decisions
- applicable standards
- policies
- operational constraints

## Workflow

### 1. Identify Architectural Drivers

Determine which requirements materially shape the architecture.

Examples:

- security
- availability
- performance
- scalability
- consistency
- recovery
- regulatory requirements
- maintainability
- operability
- cost
- portability

Do not treat all quality attributes as equally important.

### 2. Understand Boundaries

Review:

- system boundaries
- domain boundaries
- trust boundaries
- deployment boundaries
- ownership boundaries
- data ownership

Identify ambiguous or overlapping responsibility.

### 3. Examine Interactions

Review:

- synchronous communication
- asynchronous communication
- APIs
- events
- external integrations
- failure propagation
- consistency requirements

Determine whether interaction patterns are justified.

### 4. Review Data Architecture

Determine:

- source of truth
- ownership
- transaction boundaries
- consistency model
- replication
- retention
- privacy implications
- migration concerns

### 5. Review Operational Architecture

Evaluate:

- deployment model
- observability
- scalability
- failure isolation
- recovery
- configuration
- secrets
- dependency management

### 6. Evaluate Alternatives

For consequential decisions, ask whether a materially simpler or safer alternative exists.

Do not generate alternatives merely to increase the number of options.

### 7. Evaluate Standards Compliance

Identify relevant repository standards and determine:

```text
COMPLIANT
PARTIALLY COMPLIANT
NON-COMPLIANT
NOT APPLICABLE
```

Explain meaningful deviations.

### 8. Identify Decisions

Determine whether architectural decisions should be recorded under:

```text
docs/decisions/
```

Record only significant and durable decisions.

## Output

### Architecture Summary

Briefly describe the proposed architecture.

### Architectural Drivers

List the requirements materially shaping it.

### Strengths

Identify aspects that appropriately satisfy those drivers.

### Findings

For each material finding:

```text
Severity:
Finding:
Why it matters:
Recommendation:
```

Use:

```text
BLOCKER
SIGNIFICANT
MINOR
```

### Standards Compliance

Identify important applicable standards and material deviations.

### Alternatives Worth Considering

Include only credible alternatives.

### Required Decisions

List unresolved decisions.

### Recommendation

Conclude with:

```text
APPROVE
APPROVE WITH CONDITIONS
REWORK REQUIRED
INSUFFICIENT INFORMATION
```

## Behaviour Rules

Do not:

- prefer microservices by default
- equate cloud-native with distributed
- require new technologies without architectural drivers
- reject pragmatic solutions merely because they are imperfect
- turn implementation details into architecture decisions

Prefer architecture that is:

- understandable
- operable
- secure
- appropriately simple
- evolvable


