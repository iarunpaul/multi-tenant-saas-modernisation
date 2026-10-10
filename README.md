# Multi-Tenant SaaS Modernisation

## Purpose

This repository is a production-oriented architecture prototype demonstrating the modernisation of a large-scale single-tenant SaaS platform into a secure, scalable and operable multi-tenant architecture.

The prototype is also used to exercise the Agentic Engineering Platform against a realistic enterprise software-engineering problem.

## Business Scenario

A mature B2B SaaS platform currently uses a database-per-customer architecture.

As the customer estate grows, this model creates increasing challenges including:

- database provisioning overhead
- schema upgrade complexity
- infrastructure cost
- operational burden
- observability complexity
- connection and resource management
- slow platform-wide change
- difficult cross-tenant operational analytics

The modernised platform should support a significantly larger tenant estate while maintaining strong tenant isolation and safe migration from the existing model.

## Primary Architecture Goals

The solution should demonstrate:

- secure multi-tenancy
- explicit tenant boundaries
- scalable data architecture
- tenant-aware authentication and authorisation
- safe migration from legacy tenant databases
- operational observability
- resilience and failure handling
- automated engineering controls
- cloud-native deployment practices
- evolutionary architecture

## Engineering Principles

The project follows the Agentic Engineering Platform.

Key principles include:

- standards are durable; agents are replaceable
- architecture follows measurable drivers
- prefer the simplest viable architecture
- security and observability are designed in
- automated controls verify machine-checkable requirements
- high-risk actions require human approval
- consequential decisions are recorded as ADRs

## Prototype Scope

The initial prototype will focus on:

1. tenant resolution
2. tenant isolation
3. multi-tenant persistence
4. tenant-aware APIs
5. authentication and authorisation boundaries
6. migration architecture
7. observability
8. automated quality and security controls

The prototype will evolve incrementally.

## Out of Scope Initially

The following are not assumed to be required:

- microservices
- service mesh
- event sourcing
- CQRS
- Kubernetes
- multi-region active-active deployment
- complex multi-agent orchestration

They may be introduced later where architectural drivers justify them.

## Architecture Workflow

Material design decisions follow:

```text
Requirement
    ↓
Grill
    ↓
Architecture Options
    ↓
Decision
    ↓
ADR
    ↓
Architecture Review
    ↓
Implementation
    ↓
Verification
```

## Status

```text
Phase: Architecture Discovery
Prototype Version: 0.1
```