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
## Review Persistence

A completed architecture review should produce a durable review artifact when operating in a writable repository.

The chat response is temporary interaction state.

The completed architecture review is an engineering record.

### Default Review Location

Store completed architecture reviews under:

```text
docs/reviews/architecture/
```

Use the naming convention:

```text
NNNN-short-descriptive-name.md
```

Examples:

```text
docs/reviews/architecture/0001-multi-tenant-data-topology.md
docs/reviews/architecture/0002-tenant-directory-control-plane.md
docs/reviews/architecture/0003-tenant-recovery-architecture.md
```

Sequence numbers should be monotonically increasing within the architecture review category.

### Review Template

Where available, use:

```text
templates/reviews/architecture-review-template.md
```

or the installed platform equivalent:

```text
.engineering/platform/templates/reviews/architecture-review-template.md
```

The template defines the durable structure of the architecture review.

Do not persist the complete chat transcript.

Capture only engineering-relevant information including:

- reviewed artifact
- architectural drivers
- architecture summary
- strengths
- material findings
- standards compliance
- alternatives
- required decisions
- conditions
- recommendation
- remaining risks
- next engineering activity
- suggested skill handoff

### Persistence Behaviour

After the architecture review has reached a final recommendation:

1. determine the next architecture review sequence number
2. generate the review document using the architecture-review template
3. save it under:

```text
docs/reviews/architecture/
```

4. report the created file path to the user

If the runtime cannot write repository files:

1. generate the complete review document
2. state the intended file path
3. provide the document ready for the user to save

Do not claim that the review was saved when no repository write occurred.

### User Control

If the user explicitly requests:

```text
do not save
```

or equivalent, do not create the artifact.

If the user requests a different output location or format, follow that instruction unless it conflicts with repository policy.

### Incomplete Reviews

Do not persist a completed architecture review while material findings are still being discovered and no final recommendation has been reached.

A partial review may be saved as a draft only when explicitly requested.

Draft reviews must use:

```text
status: draft
```

and must not be treated as completed architecture-review evidence.

### Evidence Semantics

The existence of an architecture review artifact does not mean all findings are resolved.

The artifact must preserve:

- blockers
- significant findings
- conditions
- unresolved decisions
- recommendation

An `APPROVE WITH CONDITIONS` review remains conditional until those conditions are resolved or explicitly accepted by the appropriate decision authority.

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


