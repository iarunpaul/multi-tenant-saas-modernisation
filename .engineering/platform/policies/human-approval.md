# Human Approval Policy

## Purpose

Define actions that AI agents and automation must not perform autonomously without explicit authorised human approval.

## Principle

Technical ability does not constitute permission.

## Human Approval Required

Explicit human approval is required before:

### Production Changes

- deploying to production
- changing production infrastructure
- modifying production configuration
- enabling significant production features

unless an organisation-approved automated deployment mechanism explicitly authorises the action.

### Destructive Operations

- deleting production data
- deleting production infrastructure
- irreversible migrations
- destructive schema changes
- removing backups

### Identity and Security

- changing authentication policy
- changing authorisation rules
- changing privileged roles
- changing access-control policy
- creating or rotating high-value production credentials

### External Contracts

- releasing breaking API changes
- releasing incompatible event contracts
- disabling externally consumed functionality

### High-Impact Data Changes

- large-scale data migration
- bulk data deletion
- cross-tenant data operations
- sensitive data export

### Governance Changes

- disabling required security controls
- bypassing quality gates
- weakening branch protection
- weakening mandatory review
- modifying compliance controls

## Approval Must Be Explicit

Do not infer approval from:

- previous similar actions
- repository access
- agent tool permissions
- developer role
- absence of objection

Approval should clearly apply to the intended action.

## Pre-Approval

Organisations may define pre-approved automated workflows.

Examples include:

- approved CI/CD deployment pipelines
- automatic dependency updates
- automated rollback

Such workflows must operate within defined safeguards.

## Emergency Changes

Emergency processes may override normal approval flows only when explicitly defined by organisational incident procedures.

The exception must be documented after the event.

## Agent Behaviour

When approval is required, the agent should:

1. describe the proposed action
2. describe important impact or risk
3. request explicit approval
4. wait before performing the action

Agents must not split a high-risk action into smaller steps to circumvent approval.
