# Project Roadmap

## Goal

Build a secure, observable and automated Kubernetes platform on Azure while documenting the engineering decisions and troubleshooting process for DevOps and cloud-engineering roles.

## Phase 1: CloudOps CLI foundation

Status: In progress

- [x] Create Python project and virtual environment
- [x] Build installable Typer CLI
- [x] Parse and validate YAML configuration
- [x] Implement REST API health checks
- [x] Parse JSON API responses
- [x] Add structured JSON logging
- [x] Implement log analysis
- [x] Add safe environment scaffolding and dry-run
- [x] Add Bash setup and quality scripts
- [x] Add automated tests and mocked HTTP responses
- [x] Complete Phase 1 documentation
- [x] Verify ignored files and clean Git history

## Phase 2: Containerised platform API

Status: Planned

- [ ] Create FastAPI application
- [ ] Add health, readiness and version endpoints
- [ ] Add Prometheus metrics endpoint
- [ ] Add structured application logging
- [ ] Add unit and API tests
- [ ] Create non-root Docker image
- [ ] Add local Docker Compose workflow
- [ ] Scan the image for vulnerabilities

## Phase 3: Azure infrastructure with Terraform

Status: Planned

- [ ] Bootstrap remote Terraform state
- [ ] Define naming and tagging standards
- [ ] Create resource group
- [ ] Create VNet, subnets and NSGs
- [ ] Create Azure Container Registry
- [ ] Create Key Vault
- [ ] Create Log Analytics workspace
- [ ] Create AKS cluster
- [ ] Create managed identities and role assignments
- [ ] Add validation and security scanning
- [ ] Document deployment, cost and teardown

## Phase 4: Kubernetes deployment

Status: Planned

- [ ] Create namespace
- [ ] Deploy application with raw manifests
- [ ] Configure services and ingress
- [ ] Add ConfigMaps and secret integration
- [ ] Add startup, readiness and liveness probes
- [ ] Add CPU and memory requests and limits
- [ ] Add horizontal scaling
- [ ] Add Pod Disruption Budget
- [ ] Add Kubernetes RBAC
- [ ] Add network policies
- [ ] Practise rollout and rollback

## Phase 5: Helm

Status: Planned

- [ ] Create application chart
- [ ] Template Kubernetes resources
- [ ] Add development values
- [ ] Lint and render manifests
- [ ] Perform install, upgrade and rollback

## Phase 6: Identity, secrets and networking

Status: Planned

- [ ] Configure Microsoft Entra workload identity
- [ ] Connect workloads to Key Vault
- [ ] Apply least-privilege Azure RBAC
- [ ] Configure GitHub OIDC authentication
- [ ] Configure ingress and public IP
- [ ] Add DNS records
- [ ] Enable HTTPS and TLS termination

## Phase 7: CI/CD and DevSecOps

Status: Planned

- [ ] Run Ruff and pytest on pull requests
- [ ] Scan dependencies and secrets
- [ ] Scan Terraform and Kubernetes configuration
- [ ] Build application image
- [ ] Scan container image
- [ ] Push immutable image to ACR
- [ ] Deploy with Helm
- [ ] Verify AKS rollout and application health

## Phase 8: Observability

Status: Planned

- [ ] Deploy Prometheus and Grafana
- [ ] Collect application and Kubernetes metrics
- [ ] Create dashboards
- [ ] Create alert rules
- [ ] Integrate structured logs
- [ ] Document service-level indicators

## Phase 9: Azure Functions

Status: Planned

- [ ] Create timer-triggered Python health monitor
- [ ] Call the deployed API
- [ ] Use managed identity
- [ ] Record health results
- [ ] Alert after repeated failures
- [ ] Add tests and deployment automation

## Phase 10: Reliability and incidents

Status: Planned

- [ ] Simulate failed image deployment
- [ ] Simulate readiness-probe failure
- [ ] Simulate missing Key Vault permission
- [ ] Simulate blocked network traffic
- [ ] Simulate resource pressure
- [ ] Write incident reports and runbooks

## Phase 11: Optional GitOps

Status: Optional

- [ ] Install Argo CD
- [ ] Connect environment configuration repository
- [ ] Demonstrate automated synchronisation
- [ ] Demonstrate drift detection and correction

## Final portfolio release

- [ ] Complete employer-facing README
- [ ] Add final architecture diagrams
- [ ] Add sanitised screenshots
- [ ] Verify no secrets or generated state are tracked
- [ ] Document setup, deployment, verification and teardown
- [ ] Create demonstration script
- [ ] Tag version `v1.0.0`
- [ ] Prepare CV bullet points and interview explanations
