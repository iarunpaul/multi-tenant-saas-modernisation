# Grill

## Purpose

`grill` is an adversarial engineering challenge workflow.

Its purpose is to expose weak assumptions, missing requirements, architectural risks and unresolved decisions before engineering effort is committed.

Grill should challenge a proposal, not merely expand it.

The goal is not to create more documentation. The goal is to improve decisions.

## When to Use

Use Grill before substantial implementation when reviewing:

- a new requirement
- a feature proposal
- an architecture or system design
- an implementation plan
- an integration approach
- a data model
- a security-sensitive change
- a production change
- a migration
- a major refactoring
- adoption of a new technology

Grill is normally unnecessary for small, obvious, low-risk changes.

## Modes

Grill supports four primary modes:

```text
requirement
architecture
implementation-plan
production-change
```

If no mode is specified, infer the most appropriate mode from the supplied context.

### requirement

Challenge whether the proposed requirement is understood well enough to design or implement.

Focus on:

- business outcome
- users and actors
- scope
- assumptions
- acceptance criteria
- edge cases
- non-functional requirements
- dependencies
- constraints
- regulatory or security concerns

### architecture

Challenge a proposed architecture or design.

Focus on:

- architectural drivers
- boundaries and responsibilities
- coupling
- data ownership
- consistency
- scalability
- resilience
- security
- operability
- deployment
- migration
- cost
- unnecessary complexity

### implementation-plan

Challenge whether an implementation approach can safely deliver the intended architecture.

Focus on:

- sequencing
- dependencies
- test strategy
- deployment strategy
- compatibility
- migration
- observability
- rollback
- quality gates
- hidden implementation risks

### production-change

Challenge the operational safety of a proposed production change.

Focus on:

- blast radius
- rollout strategy
- rollback
- data safety
- compatibility
- monitoring
- failure detection
- recovery
- security implications
- required human approval

## Operating Principles

Grill must:

- challenge assumptions instead of accepting them by default
- distinguish facts from assumptions
- prioritise material issues over theoretical ones
- consider both functional and non-functional requirements
- consider security and operations from the beginning
- favour the simplest architecture that satisfies the drivers
- identify unnecessary distributed-system complexity
- identify irreversible decisions
- surface missing evidence
- avoid inventing requirements
- ask the user when material information is genuinely unknown
- avoid answering unresolved business or architecture questions on the user's behalf

Grill should be constructively adversarial.

Do not reject a design merely because another design is possible.

---

# Review Execution Protocol

Grill follows:

```text
standards/ai/review-execution.md
```

or the installed platform equivalent:

```text
.engineering/platform/standards/ai/review-execution.md
```

The Interactive Discovery Gate governs how material unknowns are resolved.

The Review Execution Protocol governs:

- target identity
- material review context
- input fingerprinting
- protocol compatibility
- idempotency
- review lineage
- sequence allocation
- persistence evidence

## Review Tool Resolution

Resolve deterministic review automation in this order:

```text
scripts/review_execution.py
.engineering/platform/scripts/review_execution.py
```

If either exists, use it.

The tool result is authoritative for:

- protocol version
- execution mode
- input fingerprint
- equivalent-review detection
- next sequence
- rerun lineage
- supersession lineage
- legacy predecessor lineage

Do not manually recreate deterministic review bookkeeping when canonical tooling succeeds.

## Same-Target Review History

Previous reviews of the same target may be inspected for:

- prior findings
- unresolved conditions
- outcome comparison
- lineage

but they must not be added to fingerprint context merely because they exist.

## Idempotency

If canonical tooling reports an equivalent completed Grill review:

```text
shouldExecute: false
```

do not repeat the completed Grill assessment.

Report the existing review.

Interactive discovery should not be restarted merely to reproduce an already equivalent completed review.

## Fallback

If deterministic review tooling is unavailable:

- state that canonical review execution is unavailable
- do not claim canonical idempotency
- do not invent a canonical protocol fingerprint
- mark any persisted review as fallback execution

---

# Interactive Discovery Gate

Grill is interactive by default.

For `requirement`, `architecture`, and `implementation-plan` modes, do not produce a final Grill assessment until the Discovery Gate has been satisfied.

For `production-change`, the same rule applies whenever missing information could materially affect production safety, rollback, security, data integrity or approval requirements.

## Discovery Gate Process

Before producing findings or a recommendation:

1. inspect the supplied repository context
2. identify the intended outcome
3. classify important information as:

```text
FACT        confirmed information
ASSUMPTION  currently believed but not validated
DECISION    deliberate choice already made
UNKNOWN     information required but not yet available
```

4. identify UNKNOWN items that could materially change:
   - architecture
   - security boundaries
   - data model
   - external contracts
   - reliability model
   - migration strategy
   - deployment strategy
   - compliance treatment
   - scalability assumptions
   - cost model

5. if any material UNKNOWN exists:
   - ask the user focused questions
   - stop the current response after those questions
   - wait for the user's answers

6. incorporate the answers into the classification

7. repeat discovery where material uncertainty remains

8. proceed to the full Grill assessment only when:
   - material unknowns are resolved, or
   - the user explicitly accepts them as assumptions for the current decision

## Mandatory Stop Rule

If material information is missing, Grill must stop after asking the discovery questions.

Do not continue to:

- final findings
- Decisions Required
- architecture selection
- PROCEED
- PROCEED WITH CONDITIONS
- REWORK REQUIRED
- INSUFFICIENT INFORMATION

in the same response.

The purpose of the discovery round is to gather information, not to prematurely conclude the review.

## Do Not Answer for the User

Do not invent answers to material unknowns.

Do not silently convert an UNKNOWN into an ASSUMPTION.

Do not infer business requirements merely because a common industry pattern exists.

Do not select a requirement because it would make an architecture easier to justify.

For example, if tenant scale is unknown, ask for tenant scale.

Do not invent:

```text
100,000 tenants
```

simply to continue the architecture exercise.

If the user does not know the answer, help establish a reasonable explicit assumption, but make clear that it is an assumption.

## Question Behaviour

Ask focused questions in small logical groups.

Prefer approximately 3–5 questions per discovery round.

Do not present a large questionnaire unless the user explicitly asks for one.

Prioritise questions according to architectural impact.

Questions that could change the following normally come first:

```text
security boundary
data ownership
tenant isolation
architecture topology
consistency model
availability model
migration strategy
regulatory treatment
blast radius
scalability model
```

Avoid spending early discovery rounds on details that can safely be decided during implementation.

## Discovery Round Output

When the Discovery Gate is not satisfied, use this structure:

### Current Understanding

Briefly summarise what is known.

### Material Unknowns

Identify only the unknowns that could materially affect the decision.

### Discovery Questions

Ask the next focused set of questions.

### Waiting For

State what information is needed before continuing the Grill.

Then stop.

Example:

```text
### Current Understanding

The platform currently uses database-per-tenant persistence and the
modernisation aims to reduce operational overhead without weakening
tenant isolation.

### Material Unknowns

Tenant scale, workload distribution and restore requirements could
materially change the target tenancy model.

### Discovery Questions

1. Approximately how many tenants exist today and what growth is expected?
2. Is workload distribution mostly small tenants with a few large tenants?
3. Is physical database isolation required for any tenant category?
4. Must a single tenant be independently restorable?
5. What migration downtime is acceptable per tenant?

### Waiting For

These answers are required before comparing tenancy models.

```

Do not add a final recommendation after this section.

---

# Review Process

## 1. Establish the Intended Outcome

Determine:

- what problem is being solved
- who benefits
- what success looks like
- what constraints are already known

If the intended outcome itself is unclear, treat this as Discovery Gate information and ask the user before continuing.

## 2. Separate Facts, Assumptions, Decisions and Unknowns

Classify important statements as:

```text
FACT        confirmed information
ASSUMPTION  currently believed but not validated
DECISION    deliberate design or delivery choice
UNKNOWN     information required but not yet available
```

Pay particular attention to assumptions presented as facts.

Material UNKNOWN items trigger the Interactive Discovery Gate.

## 3. Identify Architectural Drivers

Determine which quality attributes materially influence the solution.

Examples include:

- availability
- scalability
- latency
- throughput
- consistency
- security
- privacy
- auditability
- maintainability
- operability
- portability
- cost
- recovery objectives
- regulatory compliance

Do not assume every quality attribute is equally important.

Where possible, seek measurable constraints rather than vague statements.

Prefer:

```text
P95 API latency < 300 ms
```

over:

```text
the system must be fast
```

Prefer:

```text
tenant migration downtime < 5 minutes
```

over:

```text
migration should minimise downtime
```

Do not invent measurements when they are unknown.

Ask for them through discovery.

## 4. Challenge the Proposal

Evaluate the proposal across the relevant dimensions below.

### Business and Requirements

Ask:

- Is the actual business problem clear?
- Is the proposed solution solving the correct problem?
- What is explicitly out of scope?
- Are acceptance criteria measurable?
- Are important user journeys missing?
- Are edge cases known?
- Which outcomes are mandatory versus desirable?
- Are business constraints being mistaken for implementation preferences?

### Architecture

Ask:

- Are system boundaries clear?
- Does each component have a justified responsibility?
- Is coupling appropriate?
- Is the architecture more distributed than necessary?
- Are synchronous and asynchronous interactions justified?
- Who owns each important piece of data?
- Are consistency requirements understood?
- Is state management explicit?
- Are isolation and failure boundaries explicit?
- Can the architecture evolve incrementally?

### Data

Ask:

- What is the source of truth?
- Who owns the data?
- What are the transaction boundaries?
- What consistency model is required?
- What happens during partial failure?
- Is migration required?
- Are retention and deletion requirements understood?
- Is sensitive data identified?
- What are backup and restore requirements?
- Is data partitioning required?
- Can data ownership be enforced rather than merely documented?

### API and Integration

Ask:

- Are contracts explicit?
- Is versioning required?
- Are consumers known?
- Is idempotency required?
- What are retry semantics?
- What happens if dependencies are unavailable?
- Are timeouts and failure boundaries defined?
- Is backward compatibility required?
- Are integration ownership and lifecycle responsibilities clear?

### Security

Ask:

- What are the trust boundaries?
- How are identities established?
- How is authorisation enforced?
- Where are secrets stored?
- What sensitive data crosses boundaries?
- Is encryption required?
- Are abuse cases considered?
- Is least privilege being applied?
- Can security boundaries be tested or automatically enforced?

### Reliability

Ask:

- What can fail?
- How is failure detected?
- What happens when a dependency is slow?
- What happens during partial outages?
- Are retries safe?
- Is duplicate processing possible?
- Is graceful degradation required?
- What recovery objectives matter?
- What is the acceptable blast radius?

### Scalability and Performance

Ask:

- What workload is expected?
- Which dimensions scale?
- Where are likely bottlenecks?
- Are performance requirements measurable?
- Is horizontal scaling actually required?
- Are assumptions based on evidence or speculation?
- Are workload distributions uniform or highly skewed?
- Is noisy-neighbour behaviour relevant?

### Observability

Ask:

- How will operators know the system is healthy?
- Which metrics matter?
- What should be logged?
- How will distributed operations be traced?
- What alerts require action?
- Can failures be diagnosed without reproducing them locally?
- Can telemetry support relevant business, tenant or workload dimensions safely?

### Delivery and Operations

Ask:

- How will this be deployed?
- Can it be rolled back?
- Are database changes backward compatible?
- Is a migration or transition period required?
- What happens during deployment failure?
- Are feature flags appropriate?
- What manual operations remain?
- Can deployment and migration state be observed?

### Governance

Ask:

- Which engineering standards apply?
- Which policies apply?
- Which controls can be automated?
- Which actions require human approval?
- Is an architectural decision record warranted?
- What evidence demonstrates that the relevant controls passed?

### Cost and Complexity

Ask:

- Is each technology necessary?
- Could the same outcome be achieved more simply?
- What operational burden is being introduced?
- Is complexity justified by current requirements?
- Are we solving a hypothetical future problem?
- Is complexity being moved rather than removed?

## 5. Identify Failure Scenarios

For material systems, explicitly consider scenarios such as:

```text
dependency unavailable
dependency slow
duplicate message
out-of-order message
partial transaction
network partition
authentication failure
authorisation failure
expired credential
deployment failure
schema mismatch
capacity exhaustion
data corruption
operator mistake
tenant-context loss
cross-tenant access
partial migration
rollback failure
```

Use only scenarios relevant to the proposal.

Do not generate generic failure scenarios merely to make the review appear comprehensive.

## 6. Look for Premature Complexity

Challenge proposed:

- microservices
- event-driven architecture
- CQRS
- event sourcing
- distributed transactions
- custom frameworks
- additional databases
- caching layers
- message brokers
- orchestration engines
- Kubernetes
- service mesh
- multi-agent systems

unless architectural drivers clearly justify them.

Complexity requires evidence.

## 7. Identify Decisions Required Before Implementation

Separate findings into:

```text
BLOCKER
SIGNIFICANT
MINOR
```

A blocker is an unresolved issue that could materially change:

- architecture
- security model
- data model
- external contract
- migration approach
- production safety
- delivery strategy

Do not classify ordinary implementation details as blockers.

---

# Final Assessment Gate

The final assessment may only be produced after the Interactive Discovery Gate has been satisfied.

Before producing the final assessment, confirm internally that:

```text
material unknowns resolved or explicitly accepted
architectural drivers understood
important constraints understood
major assumptions visible
relevant failure scenarios considered
major design alternatives challenged
```

If this is not true, return to discovery.

---

# Final Output Format

When discovery is complete, return the review using the following structure.

## Outcome

Briefly state what the proposal appears to be trying to achieve.

## Confirmed Facts

Summarise the important confirmed information.

## Accepted Assumptions

List assumptions explicitly being used for the current decision.

Do not present them as facts.

## What Looks Sound

Identify important aspects that are already well considered.

Do not add praise merely for balance.

## Critical Challenges

For each important issue include:

```text
Issue:
Why it matters:
Question or evidence required:
Potential consequence:
```

## Hidden Assumptions

List assumptions that still require later validation.

## Missing Non-Functional Requirements

List only NFRs that are materially relevant and currently unclear.

## Failure Scenarios

Identify the most important failure scenarios that have not been addressed.

## Complexity Check

State whether the design appears:

```text
too simple
appropriately simple
unnecessarily complex
```

Explain why.

## Decisions Required

List decisions that should be made before implementation.

Classify each as:

```text
BLOCKER
SIGNIFICANT
MINOR
```

## Recommendation

Conclude with exactly one of:

```text
PROCEED
PROCEED WITH CONDITIONS
REWORK REQUIRED
INSUFFICIENT INFORMATION
```

Explain the reasoning briefly.

`INSUFFICIENT INFORMATION` is appropriate only when the user cannot currently resolve material unknowns and does not want to proceed using explicit assumptions.

It must not be used as a substitute for conducting the interactive discovery process.

---

# Next Steps

Every completed Grill assessment must end with concrete next steps.

Next steps should be proportional to the result.

## If PROCEED

Identify the immediate engineering activity.

Examples:

```text
create ADR
run architecture-review
prepare implementation plan
begin implementation
```

## If PROCEED WITH CONDITIONS

List:

1. conditions that must be satisfied
2. which conditions must be resolved before implementation
3. which may be resolved during implementation
4. the next appropriate skill or engineering activity

## If REWORK REQUIRED

Identify:

1. what must be reconsidered
2. why the current direction should not proceed
3. what evidence or alternative design is needed
4. when Grill should be rerun

## If INSUFFICIENT INFORMATION

Identify:

1. the unresolved material information
2. who or what is likely to provide it
3. whether explicit assumptions could safely unblock further design
4. when Grill should resume

## Skill Handoff

Where appropriate, explicitly recommend the next platform skill.

Typical flow:

```text
requirement Grill
    ↓
architecture options / ADR
    ↓
architecture-review
    ↓
implementation-plan Grill
    ↓
implement
    ↓
test
    ↓
security-review
    ↓
production-readiness
```

Do not invoke another skill automatically unless the user has requested that workflow or the agent runtime explicitly supports approved orchestration.

The purpose of the handoff is to make the next engineering action clear.

---

# Behaviour Rules

Do not:

- redesign the entire system unless the existing approach is fundamentally flawed
- create hypothetical requirements to justify complexity
- recommend technology without connecting it to an architectural driver
- turn every uncertainty into a blocker
- generate large generic checklists unrelated to the proposal
- demand perfect information before useful engineering can begin
- confuse personal preference with architectural necessity
- answer material business questions on behalf of the user
- issue a final recommendation while Discovery Gate questions remain unanswered
- silently convert UNKNOWN information into FACT
- continue past a discovery question round in the same response

Prefer targeted questions that could materially change the design.

---

# Repository Integration

Before completing a Grill review:

1. identify applicable files under the repository's installed platform standards
2. identify applicable platform policies
3. identify relevant existing decisions under `docs/decisions/`
4. inspect relevant project requirements and architecture documents
5. reference those constraints in the review when relevant

Platform assets may be installed under locations such as:

```text
.engineering/platform/
.agents/skills/
```

Do not assume a single vendor-specific repository layout when equivalent platform guidance is available elsewhere.

Grill does not replace engineering standards.

It challenges whether the proposed work satisfies them.

---

# Review Persistence

A completed Grill should produce a durable review artifact when operating in a writable repository.

Interactive discovery responses are temporary conversation state.

The final completed Grill assessment is an engineering record.

### Execution Manifest Persistence

When canonical review tooling succeeds, persist the exact normalized manifest returned by `review_execution.py`.

Use the `renderedManifest` value returned by:

```text
review_execution.py prepare
```

to populate:

```text
{{execution_manifest}}
```

in the Grill review template.

Do not:

- reconstruct the manifest from Review Context
- manually rewrite the manifest
- remove context entries
- add context entries after preparation
- translate the manifest into another structure

The persisted manifest is machine-verifiable execution evidence.

The Review Context section is human-readable engineering context and may be shorter than the canonical execution manifest.

After the completed review artifact is persisted, run:

```text
review_execution.py check
```

using the same target, context, skill, review type, and platform version used during preparation.

A canonical review is not complete evidence unless this check succeeds.

The check must validate both:

```text
input fingerprint
execution manifest
```

If verification fails:

- do not report canonical verification as passed
- do not treat the artifact as completed canonical evidence
- report the verification failure

## Default Review Location

Store completed Grill reviews under a folder that reflects the engineering concern being reviewed.

Use the mapping:

```text
requirement
    → docs/reviews/requirements/

architecture
    → docs/reviews/architecture/

implementation-plan
    → docs/reviews/implementation/

production-change
    → docs/reviews/production-change/
```

Use the naming convention:

```text
NNNN-short-descriptive-name.md
```

Examples:

```text
docs/reviews/requirements/0001-multi-tenant-modernisation.md

docs/reviews/architecture/0001-multi-tenant-data-topology.md

docs/reviews/implementation/0001-tenant-migration-plan.md

docs/reviews/production-change/0001-regional-database-cutover.md
```

Sequence numbers should be monotonically increasing within each review category.

The review folder represents the engineering concern being challenged, not the skill used to perform the review.

## Review Template

Where available, use:

```text
templates/reviews/grill-review-template.md
```

or the installed platform equivalent:

```text
.engineering/platform/templates/reviews/grill-review-template.md
```

The template defines the durable structure of the Grill review.

Do not copy the complete chat transcript into the review.

Capture only information that has engineering value:

- reviewed artifact
- Grill mode
- confirmed facts
- accepted assumptions
- material unknowns
- critical challenges
- failure scenarios
- required decisions
- recommendation
- conditions
- decisions resolved during Grill
- remaining follow-up
- next engineering activity

## Persistence Behaviour

After the Final Assessment Gate has been satisfied:

1. produce the final Grill assessment
2. determine the next review sequence number
3. generate the review document from the Grill review template
4. save the document under the review category selected by the Grill mode:

```text
requirement
    → docs/reviews/requirements/

architecture
    → docs/reviews/architecture/

implementation-plan
    → docs/reviews/implementation/

production-change
    → docs/reviews/production-change/
```
5. report the created file path to the user

If the agent cannot write repository files:

1. generate the complete review document
2. state the intended path
3. provide the document ready for the user to save

Do not claim that a review was saved when no repository write occurred.

## User Control

If the user explicitly asks:

```text
do not save
```

or equivalent, do not create the artifact.

If the user specifies a different review location or format, follow that instruction unless it conflicts with repository policy.

## Incomplete Grill Sessions

Do not persist a completed Grill review while the Interactive Discovery Gate remains open.

A discovery session may optionally be saved as a draft only when explicitly requested.

Draft reviews must be clearly marked:

```text
status: draft
```

and must not be treated as ARC-001 completion evidence.

## Evidence Semantics

Only a completed Grill review may be used as evidence for:

```text
ARC-001 — Grill Review
```

The existence of a review document does not imply that all findings have been resolved.

Recommendation and unresolved conditions must remain visible in the artifact.

# Completion Criteria

A Grill review is complete when:

- the Interactive Discovery Gate has been satisfied
- major assumptions are visible
- facts and assumptions are distinguishable
- important NFRs have been considered
- material unknowns are resolved or explicitly accepted
- significant failure modes have been considered
- unjustified complexity has been challenged
- blockers are distinguishable from ordinary design questions
- the team knows which decisions must be made next
- there is a clear recommendation on whether implementation should proceed
- the next engineering activity is explicit
