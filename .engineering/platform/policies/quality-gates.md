# Quality Gates Policy

## Purpose

Define mandatory expectations for automated engineering verification.

## Principle

Instructions guide behaviour.

Quality gates verify compliance.

## 1. Required Gates

Repositories must define applicable automated quality gates based on their technology and risk.

Typical gates include:

- build or compilation
- automated tests
- formatting or linting
- static analysis
- secret scanning
- dependency vulnerability scanning

Additional gates may include:

- SAST
- API contract validation
- architecture tests
- container scanning
- infrastructure scanning
- licence checks
- deployment validation

## 2. Risk Proportionality

Not every repository requires identical controls.

Controls should reflect:

- system criticality
- exposure
- technology
- data sensitivity
- deployment environment

However, reduced risk does not justify removing basic build and security hygiene.

## 3. Gate Failure

Required quality gates must block promotion or merge where configured as mandatory.

Failures must not be ignored simply because:

- the change appears small
- the code was AI-generated
- the developer believes the failure is unrelated

The cause should be investigated.

## 4. Bypass

Mandatory gates may only be bypassed through an explicitly authorised exception mechanism.

An exception should identify:

- failed control
- reason
- risk
- approver
- remediation plan where applicable

Agents must never independently bypass mandatory quality gates.

## 5. False Positives

False-positive findings should be addressed through:

- appropriate configuration
- targeted suppression
- tool improvement

Do not broadly disable controls because one finding is incorrect.

Suppressions should be specific and reviewable.

## 6. Verification Evidence

CI output is the preferred source of evidence for automated gates.

Agents and developers must not claim a gate passed when it was not executed.

## 7. Local Verification

Developers and agents should run relevant verification locally where practical before submitting changes.

CI remains authoritative for merge and release controls.

## 8. Evolution

Quality gates should evolve as recurring engineering failures are discovered.

When a preventable defect repeatedly occurs, consider whether an automated control can detect it earlier.

## 9. Separation of Guidance and Enforcement

A rule belongs in automated quality gates when it can be reliably and objectively verified.

Examples:

```text
"Do not commit secrets"
    → secret scanner

"Code must compile"
    → build gate

"Dependencies must not contain known critical vulnerabilities"
    → vulnerability scanner

"API contract must remain compatible"
    → contract compatibility check
