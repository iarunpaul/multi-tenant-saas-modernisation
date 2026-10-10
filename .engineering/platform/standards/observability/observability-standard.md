# Observability Standard

## Purpose

Define baseline expectations for making software understandable in production.

Observability should help teams detect, diagnose and understand meaningful system behaviour.

## 1. Operational Questions First

Instrumentation should answer useful questions such as:

- Is the service healthy?
- Are users succeeding?
- Which operations are failing?
- Where is latency introduced?
- Which dependency is causing failure?
- Is capacity approaching a limit?

Avoid telemetry without a clear operational purpose.

## 2. Logs

Logs should be structured where practical.

Logs should provide context such as:

- operation
- correlation
- relevant resource
- result
- error category

Logs must not expose secrets.

## 3. Metrics

Metrics should represent important system behaviour.

Examples include:

- request volume
- failure rate
- latency
- resource utilisation
- queue depth
- dependency health

Avoid excessive high-cardinality dimensions without justification.

## 4. Distributed Tracing

Distributed systems should support tracing where it materially improves diagnosis.

Trace context should propagate across relevant service and messaging boundaries where practical.

## 5. Correlation

Related operations should be correlatable across system boundaries.

Correlation identifiers should be safe to expose in operational telemetry.

## 6. Health Signals

Services should expose appropriate health information.

Differentiate where useful between:

- process health
- readiness
- critical dependency health

Avoid declaring a service healthy when it cannot serve meaningful workloads.

## 7. Alerts

Alerts should require meaningful action.

Avoid alerts that:

- trigger continuously without response
- report non-actionable information
- duplicate existing signals

Alert severity should reflect operational impact.

## 8. Sensitive Data

Telemetry must comply with data-protection and security requirements.

Do not log credentials or authentication tokens.

## 9. Failure Visibility

Material failures must not be silently swallowed.

Failures should produce sufficient signals for operators to understand what occurred.

## 10. Production Validation

Important telemetry should be validated during production-readiness activities.

Instrumentation that exists only in source code but cannot be queried operationally should not be considered fully validated.
