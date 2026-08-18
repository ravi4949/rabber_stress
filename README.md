# RubberStress Platform

**RubberStress** is an end-to-end physics-informed Machine Learning platform designed for hyperelastic material characterization and constitutive modeling using Constitutive Artificial Neural Networks (CANNs).

## Repository Architecture

```
RubberStress/
├── ml_core/                        # CANN research core & inference engine
├── backend/                        # FastAPI application server & Celery task worker
├── frontend/                       # React + TypeScript Web Dashboard
├── infra/                          # Docker Compose & Nginx configuration
├── docs/                           # Math theory, API reference, & user guide
└── README.md
```

## Overview of Components

- **`ml_core`**: Implements hyperelastic constitutive models (Neo-Hookean, Mooney-Rivlin, Ogden, Yeoh, Arruda-Boyce), invariant preprocessors, CANN neural architectures (Model A/B/C, ICNN variants), physics-by-construction constraints, training pipelines, and FEM lookup-table validation.
- **`backend`**: FastAPI server providing user authentication, CSV dataset uploads, Celery job scheduling, report generation, and database interactions with PostgreSQL.
- **`frontend`**: React + TypeScript client providing interactive visualization of stress-strain curves, model selection, job status tracking, and report downloads.
- **`infra`**: Containerization setup for orchestration via Docker Compose.
- **`docs`**: Mathematical derivations of hyperelasticity, invariants, automatic differentiation of strain energy functions, and polyconvexity guarantees.
