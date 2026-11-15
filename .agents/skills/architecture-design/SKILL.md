---
name: architecture-design
description: Design or evaluate software architecture for a feature or system using requirements, codebase context, constraints, quality attributes, and operational considerations. Use for cross-cutting changes, new components, data/API design, or architecture reviews.
---

# Architecture Design

## Procedure

1. Review project architecture and conventions; verify their freshness.
2. Establish drivers: functional requirements, quality attributes, constraints, scale, security, operations, and compatibility.
3. Compare viable options and explain trade-offs.
4. Define component boundaries, responsibilities, dependencies, and data/control flows.
5. Specify APIs, events, data models, migrations, and error semantics where applicable.
6. Consider reliability, observability, performance, security, privacy, and failure recovery.
7. Identify incremental migration and backward-compatibility strategy.
8. Record consequential decisions as ADRs.
9. Define verification and rollout requirements.

## Outputs

Architecture proposal, diagrams where useful, contracts, migration/rollout plan, risks, and ADRs.

## Verification

Every major decision traces to a requirement or constraint. Identify assumptions and operational consequences. Do not introduce a distributed system or dependency without a justified need.
