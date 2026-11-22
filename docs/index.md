# Unified File Reader Documentation

Documentation and guides for **Unified File Reader** — a lightweight Python library for reading common file formats through a single, consistent helper function (`read_file`).

---

## Guide Index

### Requirements & Scope
- **[Requirements Overview](requirements/overview.md)**: Why this package exists, target file formats, and design scope.
- **[Functional Requirements](requirements/functional-requirements.md)**: Reading behavior, extension matching, and return types.
- **[Non-Functional Requirements](requirements/non-functional-requirements.md)**: Python compatibility, typing standards, and test expectations.

### Architecture & Design
- **[System Overview](architecture/system-overview.md)**: Separation of concerns, the reader registry, and base abstractions.
- **[Component Diagram](architecture/component-diagram.md)**: Class hierarchy and registry relationships.
- **[Data Flow](architecture/data-flow.md)**: What happens step-by-step when `read_file()` is called.
- **[Architecture Decisions](architecture/architecture-decisions.md)**: Engineering trade-offs and rationale (ADRs).

### Technical Design & Extensibility
- **[Core Design & Adding Readers](technical-design/core-design.md)**: Implementing `BaseReader` and registering custom formats.

### API Reference
- **[API Overview](api-reference/overview.md)**: Function signatures, return contracts, and exception hierarchy.

### Development Guide
- **[Setup Guide](development/setup.md)**: Local developer setup using virtual environments.
- **[Configuration](development/configuration.md)**: Tool settings for pyproject.toml, pytest, and flake8.
- **[Development Workflow](development/development-workflow.md)**: Git branching, code style, and PR checklist.

### Packaging & Releases
- **[Deployment Architecture](deployment/deployment-architecture.md)**: How the wheel and source tarball are packaged.
- **[Deployment Process](deployment/deployment-process.md)**: Step-by-step release checklist for PyPI.
- **[Release Notes](releases/release-notes.md)**: Version history and highlights.
- **[Known Issues](releases/known-issues.md)**: Current edge cases and practical workarounds.

### Testing & Operations
- **[Testing Strategy](testing/test-strategy.md)**: Test suite organization, dynamic fixtures, and coverage.
- **[Troubleshooting Guide](operations/troubleshooting.md)**: Common setup pitfalls and quick fixes.

---

## Quick Links
- **[Project README](../README.md)**
- **[Contributing Guide](../CONTRIBUTING.md)**
