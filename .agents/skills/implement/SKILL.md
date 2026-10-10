# Implement

## Purpose

Implement an approved change safely and consistently with repository architecture, standards and policies.

The objective is not to generate the largest amount of code.

The objective is to make the smallest coherent production-quality change that satisfies the requirement.

## When to Use

Use after requirements and consequential design questions are sufficiently resolved.

For substantial work, implementation should normally follow Grill and any required architecture review.

## Before Implementation

Inspect:

- task requirements
- relevant source code
- existing tests
- applicable standards
- applicable policies
- relevant architectural decisions

Understand existing patterns before introducing new ones.

## Workflow

### 1. Confirm Scope

Determine:

- desired behaviour
- affected components
- constraints
- compatibility expectations
- relevant acceptance criteria

Avoid unrelated cleanup unless necessary for the change.

### 2. Plan the Change

For non-trivial work, identify:

- files/components affected
- contract changes
- data changes
- test changes
- migration concerns
- deployment implications

Prefer incremental changes.

### 3. Follow Existing Architecture

Reuse repository conventions unless there is a justified reason to change them.

Do not introduce:

- frameworks
- architectural layers
- libraries
- services
- abstractions

without a material need.

### 4. Implement

Implementation should consider:

- correctness
- failure handling
- validation
- security
- observability
- maintainability
- compatibility
- testability

Avoid speculative generalisation.

### 5. Handle Contracts Carefully

When modifying:

- APIs
- messages
- schemas
- persisted data
- configuration contracts

consider compatibility and migration.

Breaking changes must be explicit.

### 6. Validate Locally

Run applicable:

- compilation/build
- formatting
- static analysis
- unit tests
- focused integration tests

Do not claim tests passed unless executed.

### 7. Inspect the Diff

Before completion:

- remove accidental changes
- remove debugging code
- remove unused code
- check for secrets
- verify configuration changes
- verify error handling
- ensure tests cover material behaviour

## Output

Report:

### Implemented

What changed.

### Important Decisions

Only consequential implementation decisions.

### Verification

What was actually executed and its result.

### Remaining Risks

Anything not fully validated.

### Follow-Up

Only necessary next actions.

## Behaviour Rules

Do not:

- silently change scope
- bypass failing tests
- weaken security controls to make implementation easier
- remove validation without justification
- fake external dependencies in production code purely to satisfy tests
- claim production readiness from successful compilation alone

Stop and surface the issue if implementation reveals a previously hidden architectural blocker.
