# AI-Assisted Engineering Standard

## Purpose

Define how AI coding agents and generative AI tools should participate in software engineering.

The goal is to increase engineering capability without weakening accountability, quality or governance.

## Core Principle

> AI can accelerate engineering activity. It does not remove engineering responsibility.

## 1. Humans Retain Accountability

AI-generated output must not be treated as inherently correct.

Engineers remain accountable for consequential:

- architecture
- code
- security
- deployment
- data changes
- production actions

## 2. Standards Apply Equally

AI-generated code is subject to the same:

- engineering standards
- tests
- security controls
- architecture expectations
- quality gates

as human-generated code.

Do not lower standards because code was generated automatically.

## 3. Agents Must Use Repository Context

Agents should inspect applicable:

- `AGENTS.md`
- skills
- standards
- policies
- architectural decisions
- existing source code

before substantial implementation.

## 4. Guidance Is Not Enforcement

Prompt instructions and agent skills guide behaviour.

They must not be treated as substitutes for enforceable:

- tests
- CI checks
- security scanners
- branch protections
- deployment controls
- cloud policies

Where reliable automated verification is possible, prefer automation.

## 5. Human Approval

High-risk activities must remain subject to human approval as defined by:

`policies/human-approval.md`

Agents must not interpret technical capability as permission.

## 6. Verification

Agents must clearly distinguish between:

- actions executed
- actions suggested
- assumptions made
- verification performed

Agents must never claim:

- tests passed
- builds succeeded
- vulnerabilities were absent
- deployment succeeded

unless supported by evidence.

## 7. Minimise Agent-Specific Knowledge

Durable organisational knowledge should live in portable repository assets.

Avoid storing critical engineering rules only in:

- IDE-specific prompts
- vendor-specific agents
- individual developer configurations
- transient conversations

## 8. Prefer Reusable Skills

Recurring engineering workflows should be represented as reusable skills where appropriate.

Examples include:

- architecture review
- implementation
- testing
- security review
- production readiness

## 9. Avoid Unnecessary Agent Complexity

Start with the simplest capable agent workflow.

Do not introduce:

- multiple agents
- agent hierarchies
- model voting
- autonomous orchestration

unless measurable benefits justify the complexity.

## 10. Tool Permissions

AI agents should receive only the permissions required for the task.

Particular care is required for tools capable of:

- production changes
- deleting resources
- accessing secrets
- changing identity
- modifying repositories
- sending external communications

## 11. Traceability

Material AI-assisted engineering actions should remain reviewable through normal engineering mechanisms such as:

- source control history
- pull requests
- CI evidence
- architecture decisions

Avoid creating a separate undocumented engineering process for AI-generated changes.

## 12. Continuous Improvement

Repeated agent failures should be analysed.

Determine whether the appropriate improvement belongs in:

- a skill
- a standard
- a policy
- an automated control
- repository architecture

Do not continuously solve the same failure only through increasingly large prompts.
