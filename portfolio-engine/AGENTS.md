# Portfolio Engine — Agent Instructions

## Project Purpose

Portfolio Engine is a long-term, content-driven personal portfolio system designed to present Yahaya Khalid's work professionally and remain easy to evolve as his career develops.

The system should make it possible to:

- Change the portfolio design without rewriting the backend.
- Add, remove, or replace projects as stronger work is completed.
- Add future portfolio sections without restructuring the entire application.
- Keep portfolio content separate from presentation concerns.

The project should demonstrate practical software engineering ability, not just serve as a static portfolio website.

---

## Current Technology Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- pydantic-settings
- Uvicorn

### Frontend

- React-based frontend
- Frontend implementation is not yet the primary development focus.

---

## Backend Architecture

The backend follows a layered architecture:

    Routes
       ↓
    Services
       ↓
    Repositories
       ↓
    Models
       ↓
    PostgreSQL

Pydantic schemas define API input and output contracts.

### Responsibilities

#### Routes

Routes are responsible for:

- HTTP endpoints
- Request validation
- Dependency injection
- HTTP status codes
- HTTP error responses
- Returning API responses

Routes should remain thin.

#### Services

Services are responsible for:

- Business logic
- Validation involving multiple domain objects
- Application rules
- Coordinating repositories

Business logic should generally live here rather than inside route handlers.

#### Repositories

Repositories are responsible for:

- Database queries
- Creating records
- Updating records
- Deleting records
- Retrieving records

Repositories should not contain HTTP-specific logic.

#### Models

SQLAlchemy models represent database tables and relationships.

#### Schemas

Pydantic schemas define:

- Request bodies
- Update payloads
- Response structures
- API validation

---

## Development Workflow

Development must be incremental.

For every significant change:

1. Explain what we are building.
2. Explain why it is needed.
3. Provide the Bash command needed.
4. Provide complete file contents when creating or replacing files.
5. Explain how the implementation works.
6. Run the appropriate test or verification.
7. Confirm the expected result.
8. Only then move to the next step.

The preferred development style is:

    Explain
    ↓
    Command
    ↓
    Code
    ↓
    Run
    ↓
    Verify
    ↓
    Next step

Do not make large unrelated changes in a single step.

---

## Coding Principles

Prefer:

- Clear Python
- Strong typing
- Small focused functions
- Explicit business rules
- Maintainable architecture
- Reusable components
- Testable code

Avoid:

- Unnecessary abstraction
- Over-engineering
- Clever code that is difficult to understand
- Duplicated business logic
- Large route handlers
- Raw database logic inside routes

Do not rewrite working architecture simply for stylistic reasons.

---

## Database Rules

PostgreSQL is the primary database.

All database schema changes must use Alembic.

When changing a model:

1. Inspect the existing model.
2. Inspect the existing migration history.
3. Modify the model.
4. Generate an Alembic migration.
5. Review the generated migration.
6. Apply the migration.
7. Verify the database structure.

Do not manually modify the PostgreSQL schema as a replacement for migrations.

---

## API Rules

When adding an endpoint:

1. Define the Pydantic schema.
2. Implement business logic in the service.
3. Implement persistence in the repository.
4. Add the route.
5. Handle expected domain errors.
6. Test success cases.
7. Test important failure cases.

Use appropriate HTTP status codes.

Expected domain errors should be translated into HTTP errors at the route layer.

PATCH endpoints must support partial updates.

Only fields actually supplied by the client should be modified.

---

## Current Domain

The backend currently contains two primary resources:

### Portfolio

Portfolio CRUD has been implemented and tested.

### Project

Project CRUD has been implemented and tested.

Projects belong to portfolios through:

    project.portfolio_id → portfolio.id

Current development data includes:

- Main portfolio ID: 1
- Current project ID: 2

These IDs are development data only and must not be hard-coded as assumptions in application logic.

---

## Current Backend Functionality

The following foundation is already implemented:

- FastAPI application
- Root endpoint
- Health endpoint
- PostgreSQL connection
- SQLAlchemy session
- SQLAlchemy models
- Alembic migrations
- Portfolio schemas
- Portfolio repository
- Portfolio service
- Portfolio routes
- Project schemas
- Project repository
- Project service
- Project routes
- Portfolio CRUD
- Project CRUD
- Project-to-portfolio relationship
- Duplicate slug protection
- Portfolio existence validation
- Partial PATCH updates
- 404 handling
- 409 conflict handling
- Delete operations

This foundation should be preserved and extended rather than rebuilt.

---

## Testing Requirements

Before considering a feature complete:

- Confirm the application imports successfully.
- Test the new endpoint or feature.
- Test successful behavior.
- Test important invalid-input cases.
- Test relevant database behavior.
- Confirm existing functionality still works.

Manual Swagger testing can be used during development, but important functionality should eventually receive automated tests.

---

## Git Workflow

GitHub is the source-control system for this project.

Before beginning significant work:

    git status

Understand the current working-tree state before modifying files.

After completing a logical feature:

1. Review the changes.

    git diff

2. Run relevant tests.
3. Review the final status.

    git status

4. Commit with a clear message.

Example:

    git add .
    git commit -m "feat: add portfolio section"

5. Push after the checkpoint has been verified.

    git push origin main

Never:

- Force push without explicit instruction.
- Reset or discard user changes without explicit instruction.
- Overwrite unrelated work.
- Commit secrets.

---

## Security

Never place secrets in source code.

Never commit:

- API keys
- Passwords
- Database credentials
- Access tokens
- Private SSH keys
- .env files containing secrets

Use environment variables and .env for local configuration.

Confirm .gitignore protects sensitive files before committing.

---

## Change Discipline

Before modifying a file:

1. Inspect the existing file.
2. Understand what it currently does.
3. Check its imports and callers.
4. Identify the smallest required change.
5. Make the change.
6. Verify it.

Do not modify unrelated files simply because they could be improved.

Do not introduce a new dependency unless it provides clear value.

---

## Architecture Growth

The system is intended to grow beyond basic CRUD.

Future areas may include:

- Portfolio sections
- Skills
- Experience
- Education
- Certifications
- Social links
- Resume/CV
- Media
- Project technologies
- Featured projects
- Public portfolio pages
- Authentication
- Portfolio administration
- Frontend content management
- Deployment

New features should fit naturally into the existing architecture.

Do not build all future features prematurely.

---

## Product Direction

Portfolio Engine should eventually allow portfolio content to be managed independently from the frontend presentation.

The long-term concept is:

    Portfolio Data
         ↓
    Portfolio Engine API
         ↓
    Frontend
         ↓
    Public Portfolio

This separation should make it possible to change the frontend design without rebuilding portfolio content.

---

## Communication

When assisting with this project:

- Explain technical concepts clearly.
- Do not assume advanced knowledge.
- Distinguish clearly between Bash commands and file code.
- Explain why a change is being made.
- State what successful output should look like.
- Work one meaningful checkpoint at a time.

The developer should understand the system rather than blindly copy commands.

---

## Primary Goal

Build Portfolio Engine into a professional, maintainable software project that can serve as a strong demonstration of engineering ability.

Priorities:

1. Correctness
2. Maintainability
3. Clear architecture
4. Testability
5. Security
6. Professional API design
7. Extensibility

Avoid unnecessary complexity.

