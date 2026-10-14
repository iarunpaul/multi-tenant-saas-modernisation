# Review Execution Standard

## Purpose

Define common execution semantics for AI-assisted engineering reviews.

This standard applies to review workflows such as:

- Grill
- architecture review
- security review
- production-readiness review
- other future engineering review skills

The reasoning performed by a review may be probabilistic.

The execution envelope around that reasoning must be as deterministic, repeatable and auditable as practical.

## Protocol Version

```text
1
```

The protocol version identifies the execution semantics used to:

- normalize review inputs
- calculate fingerprints
- detect equivalent reviews
- establish review lineage
- allocate review sequence numbers

Fingerprints generated under different protocol versions must not be treated as equivalent unless a future protocol explicitly defines compatibility.

## Core Principle

> Review reasoning may vary; review inputs, identity, evidence and persistence must not be ambiguous.

## 1. Explicit Review Target

Every review must have an explicit target.

Examples:

```text
requirements document
ADR
architecture document
implementation plan
production change plan
source-code change
```

If the user explicitly supplies a target, use it.

If no target is supplied:

1. inspect candidate artifacts
2. if exactly one credible active target exists, state it before proceeding
3. if multiple credible targets exist, ask the user to choose
4. do not silently perform a repository-wide review

Repository-wide review is a separate explicit mode.

## 2. Review Context

A review target must not be evaluated in isolation where relevant upstream evidence exists.

Resolve only context materially relevant to the target.

Typical context includes:

```text
requirements
    ↓
requirement review / Grill
    ↓
parent decisions
    ↓
reviews of parent decisions
    ↓
current review target
```

Applicable standards and policies also form review context.

Do not load unrelated repository documents merely because they exist.

### Review History Is Not Automatically Input Context

Previous reviews of the **same target** are review lineage.

They must not automatically become fingerprinted input context merely because they exist.

Otherwise creation of a review would itself change the inputs of the next invocation and destroy idempotency.

For example:

```text
ADR-0001
    ↓
REVIEW-ARC-0003
```

A subsequent review of unchanged `ADR-0001` must not include `REVIEW-ARC-0003` in its fingerprint merely because that review now exists.

Previous reviews of the same target may still be inspected for:

- prior findings
- outcome comparison
- review lineage
- supersession
- deliberate rerun history

but they are not material fingerprint context solely by virtue of being predecessors.

Reviews of different upstream artifacts may be material context.

Example:

```text
requirements
    ↓
requirements Grill
    ↓
ADR-0001
    ↓
architecture review of ADR-0001
    ↓
ADR-0002
```

When reviewing `ADR-0002`, the review of `ADR-0001` may be legitimate upstream context because it constrains the new decision.

## 3. Context Precedence

Prefer context in this order:

1. explicit user-supplied context
2. artifact references contained in the review target
3. directly related upstream requirements
4. directly related requirement reviews
5. directly related parent ADRs or decisions
6. reviews of those parent decisions
7. applicable standards and policies

Previous reviews of the same target are handled as lineage rather than ordinary fingerprint context.

## 4. Review Execution Tool

Deterministic review bookkeeping should use repository automation where available.

Resolve the review-execution tool in this order:

```text
scripts/review_execution.py
.engineering/platform/scripts/review_execution.py
```

The first path supports repositories that own the tooling directly.

The second path is the normal location for a versioned platform installation.

If either path exists, use it.

Do not manually reproduce deterministic fingerprint or sequence-allocation logic when the tool is available.

## 5. Review Input Manifest

Before final review execution, establish an input manifest containing:

```text
review type
skill
target path
target content hash
material context paths
material context content hashes
platform version
protocol version
```

Context paths must be normalized and sorted deterministically before fingerprinting.

Previous reviews of the same target must be excluded from the normalized fingerprint context.

## 6. Input Fingerprint

A review fingerprint must be derived from the normalized input manifest.

The fingerprint identifies the material evidence against which the review was performed.

It must not depend on:

- file modification timestamps
- local absolute paths
- chat session identifiers
- model-generated prose
- sequence numbers
- existence of a previous review of the same target

The same normalized review inputs under the same protocol and platform version must produce the same fingerprint.

## 7. Protocol Compatibility

An existing review is equivalent only when:

```text
status = completed
protocol-version = current protocol version
input-fingerprint = current input fingerprint
```

A review with:

- no protocol version
- no fingerprint
- a different protocol version
- a non-canonical fallback fingerprint

must not be treated as canonically equivalent.

## 8. Idempotency

Before executing or persisting a completed review:

1. compute the review input fingerprint
2. inspect completed reviews of the same review category
3. determine whether an equivalent completed review exists

If an equivalent completed review exists:

```text
do not create a duplicate completed review
```

Instead, report the existing review.

A new review may be forced only when explicitly requested.

## 9. Review Lineage

Review lineage has three distinct meanings.

### Equivalent Review Reuse

Same canonical fingerprint and no explicit rerun request:

```text
reuse existing review
```

No new review artifact is created.

### Deliberate Rerun

Same canonical fingerprint and the user explicitly requests a new assessment:

```yaml
rerun-of: REVIEW-ARC-0003
```

A rerun:

- retains the same canonical fingerprint
- receives a new review ID
- preserves the previous review
- records the equivalent predecessor

`rerun-of` must not be used when equivalence cannot be proven.

### Superseding Review

If material target or context input changes under the same compatible protocol:

```yaml
supersedes: REVIEW-ARC-0003
```

The resulting review is new evidence for the changed inputs.

The previous completed review remains immutable historical evidence.

### Legacy Predecessor

If a previous review of the same target exists but cannot be canonically compared because it:

- predates the protocol
- has no canonical fingerprint
- uses an incompatible protocol version

record:

```yaml
legacy-predecessor: REVIEW-ARC-0002
```

Do not describe such a relationship as `rerun-of`.

## 10. Sequence Allocation

Review sequence numbers are scoped to the review category.

Examples:

```text
docs/reviews/requirements/
docs/reviews/architecture/
docs/reviews/implementation/
docs/reviews/security/
docs/reviews/production-readiness/
```

Allocate:

```text
max(existing sequence) + 1
```

Sequence allocation is an identifier concern.

It must not affect the input fingerprint.

### Lineage Metadata Emission

Review templates use a generic placeholder:

```text
{{lineage_metadata}}
```

The review workflow must replace this placeholder with **zero or one** lineage field.

Allowed canonical lineage fields are:

```yaml
rerun-of: REVIEW-...
```

```yaml
supersedes: REVIEW-...
```

```yaml
legacy-predecessor: REVIEW-...
```

Only one lineage relationship may be emitted for a completed review.

Do not emit:

```yaml
rerun-of:
supersedes:
legacy-predecessor:
```

with empty values.

Do not emit multiple lineage fields for the same review.

Use:

```text
rerun-of
```

only when:

- an equivalent completed review exists
- protocol version is compatible
- the canonical input fingerprint is identical
- the user explicitly requested a rerun

Use:

```text
supersedes
```

only when:

- a previous completed review exists for the same target
- that review uses a compatible protocol
- the current canonical fingerprint differs because material target or context inputs changed

Use:

```text
legacy-predecessor
```

only when:

- a previous completed review exists for the same target
- canonical equivalence cannot be established because the predecessor:
  - predates the Review Execution Protocol
  - has no canonical fingerprint
  - has no protocol version
  - uses an incompatible protocol version
  - was produced using non-canonical fallback fingerprinting

If none of these relationships applies, replace:

```text
{{lineage_metadata}}
```

with no output.

Review templates must not contain explanatory lineage rules.

The rules in this standard are authoritative.

## 11. Stable Review Metadata

Completed canonical review artifacts should record:

```yaml
id:
type:
skill:
status:
date:
reviewed-artifact:
platform-version:
protocol-version:
execution-mode:
target-sha256:
input-fingerprint:
```

Where applicable, record exactly the relevant lineage relationship:

```yaml
rerun-of:
```

or:

```yaml
supersedes:
```

or:

```yaml
legacy-predecessor:
```

Do not populate lineage fields merely because a previous review exists.

## 12. Execution Modes

### Canonical

When `review_execution.py` successfully prepares the review:

```yaml
execution-mode: canonical
```

The review may use the generated canonical fingerprint for idempotency.

### Fallback

If review automation is expected but unavailable or fails:

```yaml
execution-mode: fallback
```

The agent must:

- report that deterministic review automation is unavailable
- not claim canonical idempotency
- not invent a canonical protocol fingerprint
- not claim equivalence with previous canonical reviews

Fallback review reasoning may continue when appropriate, but the resulting artifact is not canonical Review Execution Protocol evidence.

A fallback artifact should use:

```yaml
protocol-version: none
input-fingerprint: none
```

unless another repository-defined mechanism explicitly provides canonical execution evidence.

## 13. Review Outcome Consistency

Repeated model reasoning is not guaranteed to generate byte-identical prose.

Consistency must therefore be established through:

- stable target selection
- stable context resolution
- stable severity vocabulary
- stable recommendation vocabulary
- fixed output schema
- explicit evidence references

Material outcome changes across deliberate reruns should remain visible rather than being hidden.

## 14. Immutable Completed Reviews

A completed review used as engineering evidence should be treated as immutable history.

If the reviewed artifact or material context changes:

```text
create a new review
```

Do not rewrite the old review to make it appear to have reviewed later evidence.

Corrections to metadata may be made only where they do not alter the substantive historical review outcome.

## 15. Incomplete Reviews

Interactive discovery or partially completed review activity must not be treated as completed evidence.

Drafts must use:

```yaml
status: draft
```

Drafts do not satisfy completed review controls.

## 16. Prior Finding Traceability

Where an upstream review produced findings relevant to the current target, the current review should classify each relevant inherited finding as:

```text
RESOLVES
PARTIALLY RESOLVES
DOES NOT RESOLVE
NOT APPLICABLE
```

Review workflows must not silently discard unresolved upstream findings.

Previous findings may be inspected for comparison without automatically making a same-target predecessor part of the canonical fingerprint.

## 17. Persistence

Completed reviews must use the applicable review template and repository review location.

Canonical completed reviews must contain the fingerprint returned by the review-execution tool.

If the runtime cannot persist the artifact, it must not claim that persistence occurred.

### Execution Manifest Persistence

Every canonical completed review must persist the normalized review input manifest used to calculate its fingerprint.

The persisted manifest must include:

```text
protocol version
platform version
target path
target SHA-256
context paths
context SHA-256 values
```

The persisted manifest must be derived directly from canonical review-execution tooling.

Do not reconstruct it from the human-readable Review Context section.

The two sections serve different purposes:

```text
Review Context
→ human-readable explanation of relevant engineering evidence

Execution Manifest
→ exact machine-verifiable fingerprint inputs
```

### Manifest Verification

Canonical review verification must validate the persisted execution manifest against the normalized manifest calculated from the supplied review inputs.

A canonical review must fail verification when:

```text
Execution Manifest is absent
Execution Manifest is malformed
Execution Manifest differs from the normalized canonical manifest
target SHA-256 differs
input fingerprint differs
```

The persisted manifest must use the canonical machine-readable representation produced by review-execution tooling.

Current canonical representation:

```text
JSON
```

Human-readable Review Context must not be used as a substitute for the execution manifest.

A review workflow must not report:

```text
canonical verification passed
```

unless deterministic verification succeeds for both the fingerprint and the persisted execution manifest.

Failure to persist or verify the manifest means the artifact is not complete canonical Review Execution Protocol evidence.

## 18. Automation Boundary

Deterministic operations should be performed by repository tooling where practical.

Examples:

- file hashing
- normalized manifest generation
- fingerprint generation
- protocol compatibility checking
- equivalent-review detection
- review lineage classification
- sequence allocation

AI agents should not manually reproduce deterministic bookkeeping when repository tooling exists.

## 19. Human Accountability

Review automation does not change approval authority.

A review recommendation is engineering evidence.

It is not permission to perform a high-risk action unless repository policy explicitly grants that authority.
