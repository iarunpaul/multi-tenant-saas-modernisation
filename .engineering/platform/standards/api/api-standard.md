# API Standard

## Purpose

Define baseline expectations for service APIs.

This standard is protocol-neutral where practical, with additional emphasis on HTTP APIs.

## 1. APIs Are Contracts

An API represents an agreement between provider and consumers.

API design must consider:

- consumers
- compatibility
- versioning
- failure behaviour
- security
- lifecycle

## 2. Resource and Operation Design

APIs should express business capabilities clearly.

Avoid exposing internal persistence structures directly unless they intentionally represent the external contract.

Use naming that communicates domain intent.

## 3. Compatibility

Existing consumers should not be broken unintentionally.

Potential breaking changes include:

- removing fields
- renaming fields
- changing field meaning
- changing required fields
- changing response semantics
- removing operations
- changing authentication

Breaking changes require explicit review.

## 4. Versioning

Version APIs where necessary to manage incompatible contract evolution.

Do not create new versions for every implementation change.

Versioning strategy should be consistent within a product or platform.

## 5. Validation

Requests must be validated.

Validation errors should provide useful but safe information.

Avoid exposing internal implementation details.

## 6. HTTP Semantics

HTTP APIs should use HTTP methods and status codes consistently with their intended semantics.

Avoid returning successful status codes for operations that failed.

## 7. Idempotency

Operations that may be retried should consider idempotency.

Particular care is required for:

- payments
- order creation
- provisioning
- asynchronous requests
- external callbacks

## 8. Pagination

Endpoints returning potentially large collections should support bounded retrieval.

Avoid unbounded result sets.

## 9. Filtering and Sorting

Filtering and sorting should be explicit and constrained.

Avoid exposing unrestricted query behaviour that can create security or performance risks.

## 10. Error Responses

Error contracts should be predictable.

They should distinguish where useful between:

- invalid input
- authentication failure
- authorisation failure
- missing resource
- conflict
- dependency failure
- internal failure

Avoid leaking sensitive internal details.

## 11. Correlation

Requests should support sufficient correlation to diagnose distributed operations.

Correlation identifiers should not expose sensitive data.

## 12. Security

APIs must follow:

`standards/security/secure-engineering.md`

Protected operations must enforce appropriate authentication and authorisation.

## 13. Documentation

Externally consumed APIs should have machine-readable contracts where practical.

Examples include:

- OpenAPI
- AsyncAPI
- schema definitions

Contract definitions should be validated during CI where practical.

## 14. Deprecation

Deprecated contracts should have a migration strategy.

Consumers should receive sufficient notice for consequential removals.

## 15. API Governance

Where possible, API standards should be enforced through automated linting or contract checks rather than review alone.
