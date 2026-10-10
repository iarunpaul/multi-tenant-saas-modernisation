# Secure Engineering Standard

## Purpose

Define baseline secure engineering expectations.

Security should be built into architecture, implementation and operations.

## 1. Least Privilege

Users, services and automation should receive only the permissions required to perform their intended responsibilities.

Avoid broad permissions for convenience.

## 2. Authentication

Authentication mechanisms should use established identity standards and trusted platforms where practical.

Avoid implementing custom authentication mechanisms without strong justification.

Credentials must be validated appropriately before trust is established.

## 3. Authorisation

Authorisation must be enforced for protected actions and resources.

Authentication alone does not establish permission.

Authorisation should consider:

- role
- scope
- resource ownership
- tenant
- operation

where relevant.

## 4. Trust Boundaries

Systems should explicitly recognise important trust boundaries.

Examples include:

- browser to backend
- service to service
- tenant to tenant
- organisation to external provider
- CI system to cloud environment

Inputs crossing trust boundaries must not be trusted implicitly.

## 5. Input Validation

Externally controlled input must be validated appropriately.

Controls should consider relevant risks such as:

- injection
- path traversal
- unsafe deserialisation
- SSRF
- oversized payloads
- malformed data

Validation should be applied at appropriate boundaries.

## 6. Sensitive Data

Sensitive data must be:

- identified
- protected in transit
- protected at rest where required
- access-controlled
- retained only as required
- excluded from logs unless explicitly justified

## 7. Cryptography

Use established cryptographic libraries and platform capabilities.

Do not design custom cryptographic algorithms.

Encryption keys must be managed separately from encrypted data where practical.

## 8. Secrets

Secrets must follow:

`policies/secrets.md`

Secrets must never be intentionally committed to source control.

## 9. Logging

Logs must not expose:

- passwords
- access tokens
- refresh tokens
- private keys
- API secrets
- complete sensitive authentication credentials

Sensitive personal or financial data should only be logged where justified and protected.

## 10. External Dependencies

Dependencies should be evaluated for:

- known vulnerabilities
- maintenance
- provenance
- unnecessary privilege

Automated vulnerability scanning should be used where practical.

## 11. Supply Chain

Build and deployment pipelines should minimise supply-chain risk.

Prefer:

- pinned or controlled dependency versions where appropriate
- trusted package sources
- reproducible builds where practical
- protected CI credentials
- least-privilege CI identities

## 12. Tenant Isolation

Multi-tenant systems must enforce tenant boundaries consistently.

Tenant identity must not be derived solely from untrusted user input.

Data access must verify tenant context at appropriate boundaries.

## 13. Security Failures

Security-sensitive failures should default to a safe outcome.

Avoid fail-open behaviour unless deliberately designed and approved.

## 14. Security Review

Material security-sensitive changes should use:

`skills/security-review/`

## 15. Automated Controls

Applicable security automation should include:

- secret scanning
- dependency vulnerability scanning
- static application security testing
- infrastructure scanning
- container scanning

where relevant.

Automated controls complement engineering review rather than replace it.
