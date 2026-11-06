---
description: Deep-dive an existing/legacy codebase and generate comprehensive project documentation under docs/project-overview/
agent: doc-keeper
subtask: false
---

# Dive Into Project

Act as a senior software architect, technical lead, and codebase archaeologist to analyze the actual repository and produce a full set of project-overview Markdown documents for a new engineer.

> [!NOTE]
> Read-only analysis. Do NOT modify application code unless explicitly requested.
> The deliverable is the Markdown documentation under `docs/project-overview/` and the resulting mental model of the project.

Role

You are a senior software architect, technical lead, and codebase archaeologist.



I have just joined this project as a new engineer.



This is an existing/legacy project, so I do NOT want you to immediately modify code or implement features.



Your primary goal is to help me understand this project deeply and quickly by analyzing the actual repository.



You must derive your conclusions from the codebase, configuration files, infrastructure files, database definitions, tests, documentation, CI/CD configuration, and other available evidence.



Do NOT guess.



Whenever something is uncertain, explicitly mark it as:



CONFIRMED — directly supported by code/configuration

INFERRED — strongly inferred from multiple pieces of evidence

UNKNOWN — insufficient evidence

CONFLICTING — different parts of the project suggest different behavior



For important conclusions, always mention the evidence:



file path

class/function/module

configuration

database table/entity

API endpoint

infrastructure resource

or other concrete evidence

Primary Goal

Build a comprehensive set of Markdown documents that allows a new engineer to understand this project without reading the entire repository manually.



I want to be able to answer:



What problem does this application solve?

Who uses it?

What are the core business journeys?

What are the most important features?

What happens technically when a user performs an important action?

What is the technology stack?

What is the architecture?

How are frontend, backend, database, external systems, and infrastructure connected?

How is the codebase organized?

Where is the business logic?

What are the most important domain concepts?

What are the important database tables/entities and relationships?

What APIs exist and how do they work?

How does authentication/authorization work?

How does data flow through the system?

How do background jobs/events/queues work?

How does the application communicate with external systems?

How is the project built?

How is it tested?

How is it deployed?

What infrastructure does it use?

How does CI/CD work?

How do I run it locally?

How do I debug it?

What are the operational concerns?

What are the legacy/technical-debt areas?

What are the dangerous parts of the system?

If I need to modify feature X, where should I start?

What should a new engineer understand before touching this codebase?

What are the most important things I should learn during my first week?

IMPORTANT ANALYSIS RULES

Rule 1 — Analyze before documenting

First inspect the repository structure and identify:



frontend

backend

services

libraries/packages

infrastructure

database

scripts

CI/CD

deployment configuration

documentation

tests

configuration

environment files

Docker files

IaC

monitoring/logging

migrations

message brokers

external integrations



Do not start by reading every file sequentially.



Start from the highest-value architectural entry points.

Rule 2 — Follow execution paths

For important functionality, trace the actual execution path.



For example:



User action
→ UI component
→ frontend state
→ API client
→ HTTP endpoint
→ controller
→ service/use case
→ domain logic
→ repository
→ database



Or:



User action
→ API
→ transaction
→ event
→ message broker
→ consumer
→ external service



Do not merely list files.



Explain how the system actually behaves.

Rule 3 — Distinguish business concepts from technical concepts

For each important feature, identify:

Business concept

What does this feature mean to the business/user?

Technical implementation

How is that business concept represented in the code?



For example:



Business:

A user submits an order.

Technical:

OrderPage
  ↓
useCreateOrder()
  ↓
POST /orders
  ↓
OrderController
  ↓
CreateOrderService
  ↓
OrderRepository
  ↓
orders table


DOCUMENTATION STRUCTURE

Create a /docs/project-overview/ directory.



Generate the following Markdown documents.

00 — README.md

Create:



docs/project-overview/README.md



This is the entry point for a new engineer.



Include:



What this project is

What problem it solves

Who uses it

High-level architecture

Main components

Core journeys

Technology stack

How to run locally

How to deploy

Important documentation links/files

Important repositories/directories

Recommended reading order

Top 10 things a new engineer should know

Top 10 areas to be careful with



At the end include:

Recommended Learning Path

Example:

Day 1
├── Project overview
├── Business domain
└── Core journeys

Day 2
├── Architecture
├── Code structure
└── Data model

Day 3
├── APIs
├── Authentication
└── External integrations

Day 4
├── Infrastructure
├── Deployment
└── CI/CD

Day 5
├── Testing
├── Observability
└── Technical debt


Adapt this based on the actual project.

01 — PROJECT_CONTEXT.md

Create:



docs/project-overview/01-project-context.md



Explain the project from a business perspective.



Include:

Purpose

What problem is this system solving?

Users

Who interacts with it?



For each user type:



role

responsibilities

permissions

typical actions

Business Domain

Explain the major business concepts.



Avoid technical terminology initially.

System Boundaries

Explain:



What this system owns

What it does not own

What external systems it depends on

Business Vocabulary

Create a glossary:

TermMeaningCode Representation

02 — CORE_JOURNEYS.md

Create:



docs/project-overview/02-core-journeys.md



This is one of the MOST IMPORTANT documents.



Identify the major user journeys.



For each journey explain:

Journey: [Name]

Business Goal

What is the user trying to accomplish?

Preconditions

What must already exist?

Main Flow

Explain step-by-step.

Alternative Flows

What can go differently?

Failure Cases

What happens when something fails?

Technical Flow

Trace the real implementation:

User
 ↓
Frontend
 ↓
API
 ↓
Controller
 ↓
Service
 ↓
Repository
 ↓
Database


Use actual names from the repository.

Important Files

List the most relevant files.

Data Changes

Which entities/tables are read or modified?

External Systems

Which external services are involved?

Events / Async Processing

Explain any queues/events/jobs.

Authorization

Explain who can perform this action.

Important Edge Cases

List important edge cases discovered in the code.

Identify at least the top 5–10 most important journeys if the project contains enough functionality.



Rank them:



Critical

High

Medium

Low

03 — ARCHITECTURE.md

Create:



docs/project-overview/03-architecture.md



Explain the architecture from high-level to low-level.



Start with:

                    ┌───────────────┐
                    │     Users     │
                    └───────┬───────┘
                            │
                    ┌───────▼───────┐
                    │   Frontend    │
                    └───────┬───────┘
                            │
                    ┌───────▼───────┐
                    │    Backend    │
                    └───────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
          Database       Queue        External APIs


Replace this with the REAL architecture.



Explain:

Level 1 — System Architecture

Major systems/components.

Level 2 — Application Architecture

Frontend/backend/service boundaries.

Level 3 — Backend Architecture

Explain:



controllers

services

use cases

domain

repositories

infrastructure

modules

middleware

guards

interceptors

validation

error handling



Use the terminology actually used by this project.

Level 4 — Runtime Flow

Explain how a request travels through the application.

Architecture Patterns

Identify patterns such as:



Layered Architecture

Clean Architecture

Hexagonal Architecture

MVC

Modular Monolith

Microservices

Event-driven architecture

CQRS

Repository pattern

Unit of Work

Saga

Outbox

etc.



Do not label a pattern unless the code actually supports it.

04 — TECH_STACK.md

Create:



docs/project-overview/04-tech-stack.md



Create a table:

LayerTechnologyVersionPurposeEvidence

Frontend









Backend









Database









Cache









Queue









Cloud









IaC









CI/CD









Testing









Monitoring









Also explain:

Why each technology appears to be used

Do not invent the original architectural reasoning.



If the reason cannot be established:

The repository confirms X is used, but the original reason is unknown.

05 — CODEBASE_STRUCTURE.md

Create:



docs/project-overview/05-codebase-structure.md



Explain the repository structure.



For example:

src/
├── modules/
├── common/
├── infrastructure/
├── config/
└── ...


Explain the responsibility of each important directory.



Then identify:

Important Entry Points

Examples:



application bootstrap

main.ts

App.tsx

routing

dependency injection

module registration

Important Configuration

Explain:



environment variables

config files

feature flags

secrets

runtime configuration

Where should I look when...

Create a practical lookup table:

TaskWhere to start

Add API



Modify business rule



Add database field



Modify UI



Add background job



Modify authentication



Modify deployment



Debug production issue



06 — DOMAIN_MODEL.md

Create:



docs/project-overview/06-domain-model.md



Identify the core domain entities/concepts.



For each:



purpose

important fields

relationships

lifecycle

state transitions

business rules

code representation

database representation



Create an entity relationship diagram using Mermaid where possible.



Example:

erDiagram
    USER ||--o{ ORDER : creates
    ORDER ||--|{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : references


Only include relationships supported by the actual code/database.

07 — DATA_AND_DATABASE.md

Create:



docs/project-overview/07-data-and-database.md



Explain:



database technology

schemas

major tables

important columns

primary keys

foreign keys

indexes

constraints

relationships

migrations

transactions

locking

soft deletes

audit/history

data retention if identifiable



Identify the most important tables.



For each:

TablePurposeImportant columnsRelationshipsUsed by

Explain important queries and data-access patterns.



Identify potentially dangerous queries:



full table scans

N+1 queries

large joins

missing indexes

expensive aggregations

bulk updates

transaction-heavy operations



Only report issues when supported by evidence.

08 — API_AND_INTEGRATIONS.md

Create:



docs/project-overview/08-api-and-integrations.md



Document important APIs.



For each API:

METHOD /path

Purpose:
Authentication:
Authorization:

Request:
Response:

Controller:
Service:
Repository:

Database impact:

External calls:

Errors:


Also document external integrations:



APIs

payment systems

authentication providers

cloud services

storage

messaging

email

third-party systems



For each integration explain:

Our Application
      ↓
Integration Client
      ↓
External System


Include timeout/retry/error handling if identifiable.

09 — AUTH_SECURITY.md

Create:



docs/project-overview/09-auth-security.md



Analyze:



authentication

authorization

roles

permissions

sessions

JWT/OAuth/etc.

token lifecycle

password handling

secrets

encryption

CORS

CSRF

input validation

rate limiting

security middleware

sensitive data



Explain the actual authentication flow.



Example:

Login
 ↓
Authentication endpoint
 ↓
Credential validation
 ↓
Token generation
 ↓
Client
 ↓
Authorization header
 ↓
Authentication middleware
 ↓
Authorization
 ↓
Controller


Do not claim the system is secure merely because a security library exists.



Identify observable risks or unknowns separately.

10 — ASYNC_AND_EVENTS.md

Create:



docs/project-overview/10-async-and-events.md



If the project uses:



queues

Kafka

RabbitMQ

SQS

SNS

EventBridge

cron

workers

background jobs

webhooks

event-driven architecture



document them.



For each flow:

Producer
 ↓
Message/Event
 ↓
Broker
 ↓
Consumer
 ↓
Handler
 ↓
Database / External Service


Explain:



retry

dead-letter behavior

idempotency

ordering

duplicate handling

failure handling

transaction boundaries



If none exist, explicitly state that.

11 — LOCAL_DEVELOPMENT.md

Create:



docs/project-overview/11-local-development.md



Explain exactly how a new engineer can run the project locally.



Include:

Prerequisites

Versions of:



Node

Java

Python

Docker

database

package manager

etc.

Installation

Actual commands from the repository.

Environment Variables

Explain required variables without exposing secrets.

DATABASE_URL
API_URL
...


Explain where values come from.

Start Dependencies

Docker/services/etc.

Start Application

Exact commands.

Run Frontend

Exact commands.

Run Backend

Exact commands.

Run Tests

Exact commands.

Common Problems

Document known issues discovered from:



scripts

README

Docker

CI

configuration

troubleshooting docs

12 — BUILD_TESTING.md

Create:



docs/project-overview/12-build-testing.md



Analyze:



unit tests

integration tests

E2E tests

test frameworks

test setup

fixtures

mocks

test database

coverage

build process

lint

type checking



Explain the testing strategy.



Identify:



well-tested areas

poorly tested areas

critical paths without tests



Do not infer test quality merely from test count.

13 — DEPLOYMENT.md

Create:



docs/project-overview/13-deployment.md



This is another HIGH-PRIORITY document.



Explain the complete deployment lifecycle:

Developer
 ↓
Git
 ↓
Pull Request
 ↓
CI
 ↓
Build
 ↓
Test
 ↓
Artifact/Image
 ↓
Registry
 ↓
Deployment
 ↓
Cloud Infrastructure
 ↓
Application


Document:



environments

development

staging

production

branches

CI/CD

build process

Docker

container registry

deployment platform

infrastructure

environment variables

secrets

database migrations

rollback

release process



For each environment:

EnvironmentInfrastructureDeployment MethodURL/EndpointDatabase

Do not expose secrets.

14 — INFRASTRUCTURE.md

Create:



docs/project-overview/14-infrastructure.md



Analyze infrastructure.



Identify:



AWS/GCP/Azure

VPC/network

compute

containers

load balancers

CDN

database

cache

storage

queues

IAM

DNS

monitoring

logging

Terraform

CloudFormation

Kubernetes



Create an architecture diagram.



Example:

flowchart TB
    User --> CDN
    CDN --> LoadBalancer
    LoadBalancer --> App
    App --> Database
    App --> Cache
    App --> Queue
    Queue --> Worker


Replace with actual infrastructure.

15 — OBSERVABILITY_OPERATIONS.md

Create:



docs/project-overview/15-observability-operations.md



Document:



logging

metrics

tracing

health checks

alerts

dashboards

error tracking

monitoring

incident handling

operational scripts



Answer:

If production breaks, how would I investigate it?

Create a practical troubleshooting flow:

Incident
 ↓
Check health
 ↓
Check logs
 ↓
Check metrics
 ↓
Check recent deployment
 ↓
Check dependencies
 ↓
Check database
 ↓
Identify root cause


Adapt this to the actual project.

16 — CONFIGURATION_AND_ENVIRONMENTS.md

Create:



docs/project-overview/16-configuration-and-environments.md



Explain:



environment variables

configuration hierarchy

feature flags

environment-specific configuration

secrets

external configuration

default values

configuration validation



Create a table:

VariablePurposeRequiredEnvironmentSource

Never include actual secret values.

17 — LEGACY_AND_TECHNICAL_DEBT.md

Create:



docs/project-overview/17-legacy-and-technical-debt.md



Analyze the project specifically as a legacy/existing system.



Identify:

Legacy Areas

old frameworks

deprecated dependencies

outdated patterns

duplicated code

obsolete modules

inconsistent architecture

Technical Debt

Categorize:

Critical

Could cause production/data/security problems.

High

Makes development significantly harder.

Medium

Maintainability concerns.

Low

Cleanup opportunities.



For each item:

Problem:
Evidence:
Impact:
Risk:
Suggested direction:
Confidence:


Do not propose a rewrite unless evidence supports it.

18 — ARCHITECTURE_RISKS.md

Create:



docs/project-overview/18-architecture-risks.md



Identify risks around:



scalability

reliability

performance

data consistency

concurrency

security

deployment

observability

external dependencies

single points of failure

operational complexity



For each:

RiskEvidenceImpactLikelihoodSeverityUnknowns

Do not exaggerate.

19 — FEATURE_CHANGE_GUIDE.md

Create:



docs/project-overview/19-feature-change-guide.md



Create a practical map for future development.



Answer:

If I need to change X, where should I go?

Examples:

Add a new API
→ Controller
→ Service
→ DTO
→ Repository
→ Migration
→ Tests

Modify business rule
→ Domain/service
→ Related tests

Modify UI
→ Page
→ Component
→ Hook
→ API client
→ State

Modify database
→ Entity/model
→ Migration
→ Repository/query
→ Tests

Modify deployment
→ CI/CD
→ Docker
→ IaC
→ Environment configuration


Adapt this to the actual architecture.

20 — NEW_ENGINEER_SURVIVAL_GUIDE.md

Create:



docs/project-overview/20-new-engineer-survival-guide.md



Answer:

What should I understand first?

What should I avoid touching initially?

Which modules are most dangerous?

Which modules are easiest to learn from?

Which code is representative of the architecture?

Which code is legacy and should NOT be used as a pattern?

What mistakes could a new engineer easily make?

What assumptions are dangerous?

What terminology should I learn?

Who/what are the important dependencies?

What should I ask the team?

Create:

First 1 Day

First 3 Days

First Week

First 2 Weeks

learning plans.

21 — SYSTEM_GLOSSARY.md

Create:



docs/project-overview/21-system-glossary.md



Build a glossary of:



business terms

technical terms

abbreviations

internal terminology

important entities

important statuses

important codes



Format:

TermMeaningWhere UsedNotes

22 — UNKNOWN_AND_OPEN_QUESTIONS.md

Create:



docs/project-overview/22-unknown-and-open-questions.md



This is extremely important.



Do NOT pretend to understand something that the repository does not reveal.



Create:

QuestionWhy It MattersEvidence MissingWho/Where to Ask

Examples:



Why was this architecture chosen?

Why does this legacy module exist?

What is the expected business behavior?

Why is this retry count configured this way?

Who owns this external integration?

What production incident caused this workaround?



Separate:



Codebase questions

Business questions

Infrastructure questions

Operational questions

23 — ARCHITECTURE_DECISION_RECORDS.md

Create:



docs/project-overview/23-architecture-decisions.md



Try to reconstruct important architectural decisions from evidence.



For example:

Decision:
Use PostgreSQL instead of MongoDB.

Status:
INFERRED

Evidence:
...

Reason:
Unknown / inferred

Trade-offs:
...

Confidence:
Medium


Do NOT fabricate historical reasons.



Clearly distinguish known facts from inferred reasoning.

24 — REQUEST_LIFECYCLE.md

Create:



docs/project-overview/24-request-lifecycle.md



Trace a typical request from beginning to end.



Explain:

Client
 ↓
DNS
 ↓
CDN
 ↓
Load Balancer
 ↓
Application
 ↓
Middleware
 ↓
Authentication
 ↓
Controller
 ↓
Validation
 ↓
Service
 ↓
Repository
 ↓
Database
 ↓
Response
 ↓
Client


Adapt this to the actual project.



Include:



request IDs

logging

error handling

transactions

caching

retries

external calls



if applicable.

25 — DEEP_DIVE_MAP.md

Create:



docs/project-overview/25-deep-dive-map.md



Create a map of the codebase showing where deeper investigation should happen.



Rank areas:

Must Understand

Should Understand

Useful Later

Probably Don't Need Initially

For every major module include:

Module:
Purpose:
Complexity:
Business Criticality:
Risk:
Dependencies:
Recommended Learning Priority:


FINAL DOCUMENT — KNOWLEDGE_GRAPH.md

Create:



docs/project-overview/KNOWLEDGE_GRAPH.md



Build a concise mental model of the entire system.



Use diagrams where useful.



The document should answer:

WHO
 ↓
does WHAT
 ↓
through WHICH SYSTEM
 ↓
using WHICH DATA
 ↓
calling WHICH SERVICES
 ↓
deployed WHERE
 ↓
observed HOW


Then provide:

The 20% I Need to Understand 80% of the System

List the smallest set of concepts/modules/journeys that give the highest understanding.

ANALYSIS PROCESS

Before generating the documents, perform analysis in this order:

Phase 1 — Repository Reconnaissance

Inspect:



root files

package manifests

README

source structure

Docker

CI/CD

infrastructure

migrations

configuration

tests



Produce a temporary mental model.

Phase 2 — Identify System Boundaries

Determine:



applications

services

databases

external systems

infrastructure

users

Phase 3 — Identify Core Domain

Find:



major entities

business concepts

important workflows

state machines

important business rules

Phase 4 — Trace Core Journeys

Follow actual execution paths through the code.



Prioritize the most business-critical flows.

Phase 5 — Analyze Architecture

Move from:

System
 ↓
Components
 ↓
Modules
 ↓
Classes
 ↓
Functions
 ↓
Database


Phase 6 — Analyze Infrastructure

Understand:

Code
 ↓
Build
 ↓
Artifact
 ↓
CI/CD
 ↓
Infrastructure
 ↓
Runtime


Phase 7 — Analyze Operations

Understand:

Logs
Metrics
Tracing
Alerts
Health checks
Deployments
Rollback
Incident investigation


IMPORTANT: DO NOT READ EVERYTHING

Do NOT waste time generating documentation for every class/function.



Focus on:



Entry points

Core journeys

Business-critical modules

Main domain entities

Important APIs

Data model

Infrastructure

Deployment

External integrations

Critical background processes

Authentication/authorization

Important tests



Only go deeper into individual implementation details when they are necessary to explain a larger system behavior.

EVIDENCE REQUIREMENT

For every important architectural or behavioral statement, provide evidence.



Example:

The application uses PostgreSQL.

Evidence:

docker-compose.yml
DATABASE_URL
src/database/
package.json
migration files


Do not simply say:

The application uses PostgreSQL.

Instead explain why you know it.

CONFIDENCE

For important conclusions use:



HIGH

MEDIUM

LOW



Example:

The application appears to follow a modular monolith architecture.

Confidence: HIGH



Evidence:



...

...

...

DIAGRAM REQUIREMENT

Use Mermaid diagrams whenever they significantly improve understanding.



Useful diagrams include:



system architecture

component architecture

request lifecycle

database relationships

core journeys

deployment architecture

event flows

authentication flow



Do not create diagrams just for decoration.

DOCUMENT QUALITY STANDARD

The documentation should be:



technically accurate

based on actual code

concise but deep

understandable to a new engineer

connected across documents

actionable

explicit about uncertainty



Avoid:



generic software architecture explanations

textbook definitions unrelated to this project

repeating the same information

documenting trivial implementation details

inventing business requirements

inventing architectural decisions

FINAL SELF-REVIEW

After generating all documents, perform a second pass.



Check:



Do the core journeys match the actual code?

Do architecture diagrams match the implementation?

Do deployment instructions match CI/CD?

Do database descriptions match migrations/entities?

Are external integrations actually present?

Are authentication claims supported by code?

Are there contradictions between documents?

Are important unknowns explicitly marked?

Are legacy areas clearly distinguished from recommended patterns?

Can a new engineer use these documents to make a small feature change safely?



If you discover contradictions, update the relevant documents.

FINAL OUTPUT

At the end, provide a concise summary containing:

Project in One Paragraph

Architecture in One Diagram

Top 10 Core Journeys

Top 10 Important Modules

Top 10 Important Tables/Entities

Top 10 External Dependencies

How to Run Locally

How to Deploy

Biggest Risks

Biggest Unknowns

Recommended Reading Order

First Feature I Should Study

Five Questions I Should Ask the Team

Do not modify application code unless explicitly requested.



The deliverable for this task is the Markdown documentation and the resulting mental model of the project.