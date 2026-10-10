# Agent Portability Standard

## Purpose

Keep organisational engineering practices portable across AI coding agents and development platforms wherever practical.

## Core Principle

> Standards are durable; agents are replaceable.

## 1. Portable Assets Are Authoritative

Durable engineering knowledge should primarily live in repository-controlled assets such as:

- `AGENTS.md`
- `skills/`
- `standards/`
- `policies/`
- `docs/decisions/`
- automated controls

These assets should remain understandable independently of a particular AI vendor.

## 2. Vendor Integration Should Be Thin

Vendor-specific configuration should provide integration rather than become the source of organisational policy.

Examples include:

- GitHub Copilot configuration
- Claude Code configuration
- Codex configuration
- IDE-specific agent settings

Where possible, vendor integration should reference or consume shared platform assets.

## 3. Avoid Duplication

Do not copy complete organisational standards into separate vendor-specific configuration files.

Duplication creates:

- drift
- inconsistent behaviour
- maintenance overhead
- unclear authority

Where duplication is technically unavoidable, clearly identify the authoritative source.

## 4. Vendor Features May Be Used

Portability does not mean avoiding useful vendor capabilities.

Vendor-specific features may be adopted when they provide clear value.

Examples may include:

- execution harnesses
- remote agents
- worktree management
- enterprise controls
- specialised tool integration

The engineering rules executed through those capabilities should remain portable where practical.

## 5. Adapters Must Be Justified

Create vendor-specific adapters only when necessary.

Before adding an adapter determine whether:

- the agent already understands the shared format
- the feature can reference existing repository assets
- the adapter introduces material maintenance cost

Zero adapter is preferable to an unnecessary adapter.

## 6. Agent Replacement

A different supported agent should be capable of understanding the project's essential engineering expectations without reconstructing them from another vendor's configuration.

## 7. Agent-Specific Optimisation

Agent-specific optimisation is allowed where it improves developer experience or execution reliability.

It must not silently change:

- organisational policy
- quality requirements
- security controls
- architecture standards

## 8. Portability Testing

Periodically exercise important workflows using more than one supported agent where practical.

The purpose is not identical output.

The purpose is validating that essential engineering intent remains portable.
