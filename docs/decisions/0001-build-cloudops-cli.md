# ADR 0001: Build a Python CloudOps CLI

- Status: Accepted
- Date: 2026-09-15

## Context

The project requires repeatable automation for configuration validation, API health checking, log processing, filesystem operations and, later, Azure and Kubernetes administration.

Independent scripts could implement each operation, but they would create inconsistent arguments, output, error handling and testing patterns. A single command-line interface provides one discoverable operational entry point.

## Decision

Build an installable Python CLI named `cloudops` using Typer.

Use separate Python modules for operational logic and keep Typer-specific presentation code in `cli.py`. Commands are grouped by responsibility:

```text
cloudops config ...
cloudops api ...
cloudops logs ...
cloudops files ...
```

Use:

- Pydantic for configuration validation
- PyYAML for YAML parsing and generation
- HTTPX for REST API requests
- Python's standard logging package for structured events
- Pytest for automated testing
- Ruff for formatting and linting

## Rationale

- Python is widely used for DevOps and cloud automation.
- Typer provides typed arguments, generated help and nested commands.
- Separating logic from the CLI makes features easier to test and reuse.
- One executable provides a consistent operator experience.
- The design can later incorporate Azure SDK and Kubernetes API operations.

## Alternatives considered

### Independent Python scripts

Rejected because separate scripts would duplicate argument parsing, logging and error-handling behaviour.

### Bash-only implementation

Bash remains useful for environment setup and command orchestration, but becomes difficult to maintain for nested JSON, YAML, REST and SDK workflows.

### Direct Azure CLI and kubectl commands only

These tools will still be used. However, a Python layer can combine their results with configuration validation, API calls, log processing and consistent reporting.

## Consequences

### Positive

- Consistent command structure
- Testable business logic
- Reusable Python modules
- Generated command help
- Clear extension path for Azure and Kubernetes features

### Negative

- Additional dependencies must be managed.
- Packaging configuration is required.
- The CLI must avoid becoming an unnecessary wrapper around every native command.

## Guardrails

- Add a CLI command only when it combines meaningful operational logic or improves safety.
- Do not hide important Terraform, Azure CLI or Kubernetes concepts from the learner.
- Preserve useful exit codes for automation.
- Require timeouts for network operations.
- Avoid printing secrets or sensitive response data.
- Maintain automated tests for success and failure paths.
