# Security Review

## Purpose

Identify security risks introduced or exposed by a proposed or implemented change.

Security Review supplements automated security controls.

It does not replace them.

## When to Use

Apply to changes involving:

- authentication
- authorisation
- public APIs
- sensitive data
- secrets
- cryptography
- external integrations
- tenancy
- infrastructure
- privileged operations
- dependency changes
- user-controlled input

Apply proportionately elsewhere.

## Workflow

### 1. Identify Assets

Determine what requires protection:

- credentials
- personal data
- financial data
- business data
- administrative capabilities
- infrastructure
- service identities

### 2. Identify Trust Boundaries

Understand where data or control crosses:

- user/system boundaries
- service boundaries
- tenant boundaries
- network boundaries
- external-provider boundaries
- privilege boundaries

### 3. Review Identity

Evaluate:

- authentication
- identity validation
- credential handling
- service identity
- token handling
- session handling where applicable

### 4. Review Authorisation

Determine:

- who may perform each sensitive action
- where enforcement occurs
- whether least privilege applies
- whether tenant or resource ownership is verified

Authentication does not imply authorisation.

### 5. Review Input and Output

Consider:

- input validation
- injection
- unsafe deserialisation
- output encoding
- file handling
- SSRF
- unexpected payload size
- sensitive information exposure

Apply only relevant threat categories.

### 6. Review Data Protection

Assess:

- data classification
- storage
- transport
- logging
- retention
- deletion
- encryption
- access controls

### 7. Review Secrets

Verify secrets are not:

- hard-coded
- committed
- logged
- exposed through configuration output

Prefer managed secret mechanisms.

### 8. Review Dependencies

Consider:

- vulnerable dependencies
- unnecessary packages
- supply-chain exposure
- untrusted execution

Automated dependency and vulnerability scanning should verify where available.

### 9. Consider Abuse and Failure

Ask how the feature could be:

- abused
- replayed
- automated maliciously
- escalated
- used across tenant boundaries
- used for data exfiltration

### 10. Review Automated Evidence

Inspect available:

- SAST
- dependency scans
- secret scans
- container scans
- IaC scans

Do not mark findings resolved without evidence.

## Output

### Security Scope

State what was reviewed.

### Trust Boundaries

Identify important boundaries.

### Findings

For each finding:

```text
Severity:
Risk:
Evidence:
Recommendation:
```

Use:

```text
CRITICAL
HIGH
MEDIUM
LOW
```

### Automated Security Evidence

State which controls were executed.

### Residual Risk

Identify risks remaining after controls.

### Recommendation

Conclude:

```text
ACCEPTABLE
ACCEPTABLE WITH CONDITIONS
REMEDIATION REQUIRED
SECURITY BLOCKER
```

## Behaviour Rules

Do not:

- invent vulnerabilities without evidence
- treat every theoretical attack as equally probable
- expose real credentials in reports
- weaken controls to simplify development
- claim security because tests pass

Prioritise exploitable and consequential risk.

