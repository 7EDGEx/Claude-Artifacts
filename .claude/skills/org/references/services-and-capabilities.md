# 7EDGE — Services & Capabilities

## Table of Contents
1. [Service Lines](#service-lines)
2. [Technology Stack](#technology-stack)
3. [Key Specialization: SAP ECC & Oracle EBS Modernization](#key-specialization-sap-ecc--oracle-ebs-modernization)
4. [Delivery Capabilities](#delivery-capabilities)
5. [What 7EDGE Does NOT Do](#what-7edge-does-not-do)

---

## Service Lines

### 1. Cloud Migration (AWS)
**What it is:** Migrating on-premise or data-center workloads to AWS. 7EDGE does not do
lift-and-shift — engagements include re-architecture for cloud-native advantage.

**What 7EDGE delivers:**
- Cloud readiness assessment and migration roadmap
- Re-architecture of monolithic or legacy apps for AWS-native deployment
- Infrastructure-as-code setup (Terraform, CDK)
- Migration execution with rollback planning and zero-downtime strategies
- Post-migration optimization (cost, performance, resilience)

**Target situations:**
- Enterprise running on-premise ERP or custom applications
- Data centers approaching end-of-life or renewal
- Companies facing SAP ECC maintenance deadlines (2027)
- Organizations mandated to move to cloud (compliance, cost, agility)

---

### 2. Legacy-to-Microservices
**What it is:** Decomposing monolithic enterprise applications — particularly SAP ECC,
Oracle EBS, and custom-built ERPs — into loosely coupled, independently deployable
microservices.

**What 7EDGE delivers:**
- Domain analysis and service boundary definition (Domain-Driven Design)
- Strangler fig pattern implementation for incremental decomposition
- API layer design and event-driven integration (Kafka, SQS, EventBridge)
- Data migration and dual-write strategies during transition
- Containerization and Kubernetes/ECS deployment

**Key differentiator:** 7EDGE understands both the application domain (ERP business
processes) and the cloud infrastructure — not just the plumbing.

---

### 3. Custom Software Development
**What it is:** Greenfield product builds or modernization of existing applications.

**What 7EDGE delivers:**
- Full-stack web applications (React.js + Node.js + AWS)
- Backend APIs and services (Python, Node.js, serverless)
- Data platforms and pipelines (AWS-native: RDS, DynamoDB, Redshift, Glue)
- Mobile-integrated backends
- SaaS product development for ISVs

**Tech defaults:** React.js (frontend), Node.js or Python (backend), AWS Lambda +
API Gateway (serverless), DynamoDB or PostgreSQL (data), S3 + CloudFront (static/media).

---

### 4. DevOps & Platform Engineering
**What it is:** Building and running the engineering infrastructure that enables teams
to ship software reliably and fast.

**What 7EDGE delivers:**
- CI/CD pipeline design and implementation (GitHub Actions, CodePipeline, Jenkins)
- Infrastructure-as-code (Terraform, AWS CDK)
- Container orchestration (ECS, EKS)
- Observability stack (CloudWatch, Datadog, OpenTelemetry)
- SRE practices: SLOs, error budgets, incident response runbooks
- Security hardening and compliance tooling (SOC 2, ISO 27001 readiness)

**Typical entry point:** Clients who have moved to cloud but whose deployment pipelines
are manual, fragile, or slow. Or greenfield engagements where DevOps is designed in
from the start.

---

### 5. AI & Automation
**What it is:** Embedding AI/ML and process automation into enterprise workflows,
most commonly as part of a broader modernization engagement.

**What 7EDGE delivers:**
- AI-readiness assessment (can your current infrastructure support AI workloads?)
- LLM integration and RAG-based applications on enterprise data
- ML model deployment pipelines on AWS (SageMaker, Lambda inference)
- Workflow automation (event-driven, rule-based, AI-assisted)
- Document intelligence and process extraction for manufacturing/enterprise

**Important framing:** 7EDGE does not sell AI as a standalone product. The entry
point is always modernization — AI requires modern infrastructure. "We modernize
the foundation, then layer in AI — so you're not adding intelligence on top of
fragile legacy systems."

---

## Technology Stack

### Primary Stack (what 7EDGE defaults to)

| Layer | Technology |
|-------|-----------|
| **Frontend** | React.js, Next.js |
| **Backend** | Node.js, Python (FastAPI, Django) |
| **Cloud** | AWS (primary and preferred) |
| **Serverless** | AWS Lambda, API Gateway |
| **Containers** | Docker, ECS, EKS |
| **Databases** | DynamoDB, PostgreSQL (RDS), Aurora, Redshift |
| **Messaging** | SQS, SNS, EventBridge, Kafka |
| **IaC** | Terraform, AWS CDK |
| **CI/CD** | GitHub Actions, AWS CodePipeline |
| **Observability** | CloudWatch, Datadog, OpenTelemetry |

### Enterprise Systems Context (what clients typically run)

| System | 7EDGE's Engagement |
|--------|-------------------|
| **SAP ECC** | Migration path analysis, API extraction, microservices decomposition |
| **Oracle EBS** | Interface layer modernization, data migration, cloud deployment |
| **Custom ERPs** | Full decomposition and re-architecture |

---

## Key Specialization: SAP ECC & Oracle EBS Modernization

This is 7EDGE's highest-priority active capability and the most relevant for current
ICP. Use this context in any engagement involving legacy ERP.

**The context:** SAP is ending mainstream maintenance for SAP ECC in **2027**. Organizations
still running ECC face a forced decision: migrate to S/4HANA, adopt cloud ERP, or pay
expensive extended maintenance fees. This is driving significant budget activity in
manufacturing and PSU sectors.

**7EDGE's approach:**
1. **Assessment phase:** Map the current ECC landscape — modules in use, customizations,
   integration points, data quality. Identify what can be retired vs. migrated vs. replaced.
2. **Architecture decision:** Determine the target architecture — full S/4HANA migration,
   cloud-native replacement of specific modules, or hybrid approach.
3. **Extraction & API layer:** Build a clean API/service layer around ECC before touching
   core processes — this de-risks the migration.
4. **Phased migration:** Move module by module, not big-bang. Manufacturing companies
   cannot afford operational disruption.
5. **Cloud deployment:** Final state runs on AWS with full DevOps, observability, and
   support tooling in place.

**Key message to prospects:** 7EDGE does not force a specific ERP vendor path. The goal
is to modernize and de-risk the transition — the right end-state depends on the client's
business, not on product licensing relationships.

---

## Delivery Capabilities

**Project scales 7EDGE handles well:**
- 3–18 month migration or modernization engagements
- Teams of 4–15 engineers per engagement
- Multi-phase programs spanning 1–3 years for complex enterprises

**What 7EDGE does NOT do (scope honesty):**
- Large-scale ERP implementations (we modernize around them, not implement them)
- Hyperscale data engineering (petabyte-scale Hadoop/Spark pipelines)
- Mainframe modernization (IBM Z, AS/400)
- SAP BASIS administration or SAP licensing negotiation

---

## What 7EDGE Does NOT Do

Be accurate about this. Do not overscope in proposals or sales materials.

- Not a generalist IT staffing or body-shop firm
- Not a Big 4 SI managing multi-hundred-person programs
- Not a pure cloud consultancy without application delivery capability
- Not an AI-first product company
- Not a managed services provider (post-delivery support is scoped, not open-ended)
