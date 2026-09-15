# Phase 1: CloudOps CLI Foundation

## Purpose

Phase 1 establishes the local automation foundation for the Azure CloudOps Platform. The goal is to build a tested Python command-line interface that can later operate Azure resources, AKS workloads, deployment pipelines and troubleshooting workflows.

This phase deliberately focuses on local behaviour before any paid Azure infrastructure is created.

## Implemented capabilities

### Installable Python CLI

The project uses a `src` package layout and is installed in editable mode during development. Typer provides a grouped command-line interface:

```text
cloudops
├── api
│   └── check
├── config
│   └── validate
├── files
│   └── scaffold
├── logs
│   └── analyse
└── version
```

### Configuration validation

`cloudops config validate` reads YAML configuration and validates it with Pydantic models.

Validation includes:

- Required project, Azure, Kubernetes and API sections
- Supported environments: `dev`, `staging` and `prod`
- Replica limits
- Valid HTTP or HTTPS API URLs
- Positive timeout values
- Rejection of unknown configuration fields
- Clear errors for missing files, malformed YAML and invalid values

Example:

```bash
cloudops config validate config/example.yaml
```

### REST API health checking

`cloudops api check` performs a timed HTTP GET request using configuration from YAML.

The command handles:

- Successful HTTP responses
- HTTP 4xx and 5xx responses
- Connection failures
- Request timeouts
- Invalid JSON
- JSON responses with an unexpected top-level structure

During Phase 1, `https://httpbin.org/get` is used as a safe test endpoint. It will later be replaced by the platform API deployed to AKS.

Example:

```bash
cloudops api check config/example.yaml
```

### Structured JSON logging

Operational events are written as JSON Lines to `logs/cloudops.log`. Each line is a separate machine-readable JSON object containing fields such as:

- Timestamp
- Severity level
- Logger name
- Event name
- URL
- HTTP status
- Response time
- Error details

Runtime logs are excluded from Git.

### Log analysis

`cloudops logs analyse` processes structured logs one line at a time. Streaming the file avoids loading the entire log into memory.

The summary reports:

- Total non-empty lines
- Valid entries
- Malformed entries
- Successful API checks
- Failed API checks
- Average response time
- HTTP status-code counts

Malformed lines are counted and skipped so one damaged entry does not prevent analysis of the rest of the file.

Example:

```bash
cloudops logs analyse logs/cloudops.log
```

### Environment scaffolding

`cloudops files scaffold` generates starter environment configuration for later Terraform and Helm phases.

Example:

```bash
cloudops files scaffold dev --dry-run
cloudops files scaffold dev
```

The command:

- Supports `dev`, `staging` and `prod`
- Previews changes with `--dry-run`
- Creates YAML, JSON and Markdown files
- Refuses to overwrite existing files
- Returns clear filesystem errors

### Bash automation

Two Bash scripts provide a reproducible developer workflow:

```bash
./scripts/setup.sh
./scripts/check.sh
```

`setup.sh` creates or reuses the virtual environment, installs the project and verifies the CLI. `check.sh` locates the repository from its own path, selects the project interpreter and runs formatting, linting and tests.

Both scripts use strict Bash behaviour through `set -Eeuo pipefail`.

## Testing strategy

Pytest tests are separated by responsibility:

- CLI behaviour
- Configuration parsing and validation
- REST API success and failure paths
- Structured JSON logging
- Log aggregation and malformed-line handling
- Filesystem creation, dry-run and overwrite protection

HTTP requests are mocked during tests. This prevents the automated suite from depending on internet availability or the state of an external service.

Temporary filesystem tests use pytest's `tmp_path` fixture, keeping test output outside the repository and cleaning it automatically.

## Quality controls

The local quality gate runs:

```bash
python -m ruff format --check .
python -m ruff check .
python -m pytest
```

The same checks will be executed by GitHub Actions in a later phase.

## Security considerations

- Runtime logs and `.venv` are excluded from version control.
- Configuration examples contain no credentials.
- API output avoids printing the public IP returned by the temporary test endpoint.
- YAML is parsed with `yaml.safe_load`.
- Scaffolding refuses to overwrite existing configuration.
- HTTP requests have explicit timeouts.

## Troubleshooting completed

Issues encountered and resolved during this phase include:

- CLI executable unavailable when the virtual environment was inactive
- Editable installation required to create the `cloudops` command
- Typer treating a single command as the root command until a callback was added
- Empty or unsaved Python files causing import errors
- Relative paths failing when commands were launched outside the repository root
- Ruff import ordering and function-default warnings
- Scaffolding overwrite protection verified manually

## Phase 1 completion criteria

Phase 1 is complete when:

- All four command groups operate correctly
- Unit tests and CLI tests pass
- Ruff formatting and linting pass
- Bash setup and quality scripts work from different directories
- No secrets, virtual environments, runtime logs or Terraform state are tracked
- Phase 1 documentation matches the implemented code

## Next phase

Phase 2 creates a small FastAPI workload with health, readiness, version and metrics endpoints. The application will be tested locally, containerised with Docker and later deployed to AKS.
