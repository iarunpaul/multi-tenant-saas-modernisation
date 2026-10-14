# REVIEW-ARC-{{sequence}} — {{title}}

## Metadata

```yaml
id: REVIEW-ARC-{{sequence}}
type: architecture
skill: architecture-review
status: completed
date: {{date}}
reviewed-artifact: {{reviewed_artifact}}
platform-version: {{platform_version}}
protocol-version: {{protocol_version}}
execution-mode: {{execution_mode}}
target-sha256: {{target_sha256}}
input-fingerprint: {{input_fingerprint}}
{{lineage_metadata}}
```
## Execution Manifest

```yaml
protocol-version: {{protocol_version}}
platform-version: {{platform_version}}
target:
  path: {{reviewed_artifact}}
  sha256: {{target_sha256}}
context:
{{execution_context}}
```

## Review Context

### Requirements

{{requirements}}

### Requirements Review

{{requirements_review}}

### Parent Decisions

{{parent_decisions}}

### Previous Architecture Reviews

{{previous_architecture_reviews}}

### Review Target

{{reviewed_artifact}}

### Applicable Standards and Policies

{{standards_and_policies}}

## Prior Finding Resolution

{{prior_finding_resolution}}

## Purpose

{{purpose}}

## Architecture Summary

{{architecture_summary}}

## Architectural Drivers

{{architectural_drivers}}

## What Looks Sound

{{strengths}}

## Findings

{{findings}}

Each material finding should use:

```text
Severity:
Finding:
Why it matters:
Recommendation:
```

Supported severities:

```text
BLOCKER
SIGNIFICANT
MINOR
```

## Standards Compliance

{{standards_compliance}}

Use:

```text
COMPLIANT
PARTIALLY COMPLIANT
NON-COMPLIANT
NOT APPLICABLE
```

## Alternatives Worth Considering

{{alternatives}}

## Required Decisions

{{required_decisions}}

## Conditions

{{conditions}}

## Recommendation

```text
{{recommendation}}
```

{{recommendation_reasoning}}

Supported recommendations:

```text
APPROVE
APPROVE WITH CONDITIONS
REWORK REQUIRED
INSUFFICIENT INFORMATION
```

## Remaining Risks

{{remaining_risks}}

## Next Engineering Activity

{{next_activity}}

## Suggested Skill Handoff

```text
{{skill_handoff}}
```

## Evidence

This document records the completed architecture review and may be referenced as evidence for architecture-governance controls.

Execution semantics are defined by the recorded Review Execution Protocol version and execution mode.

This review does not replace an ADR.

The ADR records the architecture decision.

This document records the independent review of that decision.
