# Engineering Development Standard

## Purpose

Define minimum expectations for production-quality software development.

## Scope

This standard applies to source code, configuration, infrastructure code and automation developed within projects using this platform.

## 1. Understand Before Changing

Before implementing a material change:

- understand the intended outcome
- inspect relevant existing code
- identify applicable standards
- identify applicable policies
- identify relevant architectural decisions
- understand compatibility requirements

Do not introduce a new pattern without first determining whether an established repository pattern already exists.

## 2. Keep Changes Focused

Changes should address the requested outcome without unnecessary unrelated modification.

Avoid:

- opportunistic large refactoring
- speculative abstractions
- unnecessary dependencies
- premature framework creation

Separate unrelated changes where practical.

## 3. Prefer Readability

Code should optimise for maintainability and clarity.

Prefer:

- explicit intent
- meaningful names
- small cohesive units
- predictable behaviour

Avoid clever implementations when a simpler implementation communicates intent more clearly.

## 4. Handle Errors Deliberately

Expected failure modes should be handled intentionally.

Do not:

- silently suppress errors
- return misleading success responses
- expose sensitive internal errors
- rely on unbounded retry behaviour

Failures should provide sufficient diagnostic information without exposing sensitive data.

## 5. Validate External Input

Input crossing a trust boundary must be validated appropriately.

Examples include:

- HTTP requests
- messages
- files
- configuration
- external service responses
- user-generated content

Validation must occur at an appropriate boundary.

## 6. Configuration

Environment-specific values should not require source-code modification.

Configuration must:

- have safe defaults where appropriate
- be validated when practical
- avoid containing secrets in source control
- fail clearly when required configuration is missing

## 7. Dependencies

New dependencies require a legitimate engineering need.

Before introducing a dependency consider:

- existing platform functionality
- maintenance status
- security exposure
- licensing
- operational impact
- long-term ownership

Avoid dependencies for trivial functionality.

## 8. Compatibility

Changes affecting existing consumers must consider backward compatibility.

Particular attention is required for:

- APIs
- events
- persisted data
- configuration
- command-line interfaces
- shared libraries

Breaking changes require explicit approval.

## 9. Concurrency and Idempotency

Where operations can be repeated or processed concurrently, behaviour must be deliberate.

Consider:

- duplicate requests
- duplicate events
- retries
- race conditions
- optimistic concurrency
- idempotency

Do not assume operations are executed exactly once.

## 10. Observability

Meaningful operations should produce appropriate operational evidence.

Avoid excessive or meaningless logging.

Logs must not contain:

- credentials
- secrets
- authentication tokens
- unnecessarily sensitive personal data

## 11. Testing

Material changes must include appropriate verification.

Testing should follow:

`standards/testing/testing-standard.md`

## 12. Security

Implementation must follow:

`standards/security/secure-engineering.md`

Security controls must not be disabled merely to simplify development.

## 13. Generated Code

Generated code must be clearly identifiable where applicable.

Avoid manually modifying generated files unless the generation mechanism explicitly supports doing so.

Generated output remains subject to security and quality controls.

## 14. Documentation

Documentation should exist where it reduces future engineering ambiguity.

Prefer:

- code that explains itself
- concise READMEs
- architecture decisions for significant trade-offs
- operational instructions where needed

Avoid documentation that merely duplicates the implementation.

## 15. Definition of Done

A change is not complete merely because code has been generated.

Completion requires applicable:

- build success
- tests
- static analysis
- security controls
- review
- documentation updates
- migration validation

Any unverified element must be explicitly stated.
