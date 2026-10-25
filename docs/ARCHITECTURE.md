# GRACE Architecture

## System architecture

```mermaid
flowchart TD
    U[Institutional user] --> R[React + TypeScript client]
    R -->|JWT REST /api/v1| D[Django REST Framework]
    D --> P[Permissions and request validation]
    P --> S[Domain services and selectors]
    S --> DB[(PostgreSQL)]
    S --> A[Audit and activity history]
    D --> O[OpenAPI / Swagger]
```

## Major modules

```mermaid
flowchart LR
    Accounts --> Organization
    Organization --> Governance
    Organization --> Risks
    Organization --> Compliance
    Governance --> Monitoring
    Risks --> Monitoring
    Compliance --> Monitoring
    Monitoring --> Dashboard
    Monitoring --> AISupport[AI support]
    AISupport --> HumanReview[Human review]
    HumanReview --> Audit
    Governance --> Reports
    Risks --> Reports
    Compliance --> Reports
```

## AI decision-support flow

```mermaid
flowchart TD
    G[GRC institutional records] --> C[Deterministic calculations]
    C --> M[Monitoring rules]
    M --> F[Structured verified findings]
    F --> X[Controlled AI provider prompt]
    X --> Y[Advisory recommendation]
    Y --> H{Authorized human validation}
    H -->|Accept / modify / reject| N[Management note]
    N --> T[Immutable audit and activity trail]
```

The AI provider receives a controlled snapshot rather than unrestricted database access. Stored user text is explicitly treated as untrusted data. Every response retains its input snapshot and provider metadata and displays the advisory notice. Only an authorized person can accept, modify, or reject it.

## Extension points

The provider protocol permits alternative AI services. The monitoring rule abstraction permits new deterministic controls. Scheduled execution can move from an operating-system scheduler to Celery Beat later without changing the rule layer. Attachments can move from local media storage to managed object storage without changing compliance records.

