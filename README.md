# DevSecOps & Kubernetes Runtime Security Pipeline

This repository demonstrates an end-to-end **DevSecOps pipeline** and **Kubernetes hardening architecture** built to secure cloud-native applications across the entire software development lifecycle (SDLC) - from static code analysis to real-time runtime intrusion detection.

---

## 1. Architecture Overview

```text
+-----------------------------------------------------------------------------------+
|                                  CI/CD PIPELINE                                   |
|                                (GitHub Actions)                                   |
|                                                                                   |
|  +---------------+     +---------------+     +---------------+     +-----------+  |
|  |  Git Commit   | --> |  Semgrep SAST | --> | Checkov IaC   | --> | Docker    |  |
|  |  & Pull Req   |     |  (Python Code)|     | (K8s/TF Scan) |     | Build     |  |
|  +---------------+     +---------------+     +---------------+     +-----+-----+  |
|                                                                          |        |
|                                                                          v        |
|                                                                    +-----------+  |
|                                                                    | Trivy SCA |  |
|                                                                    | Container |  |
|                                                                    +-----+-----+  |
+--------------------------------------------------------------------------|--------+
                                                                           |
                                                                           v
+-----------------------------------------------------------------------------------+
|                            KUBERNETES CLUSTER (Kind/Minikube)                     |
|                                                                                   |
|   +---------------------------------------------------------------------------+   |
|   | DEFAULT NAMESPACE                                                         |   |
|   |                                                                           |   |
|   |   +-------------------------------------------------------------------+   |   |
|   |   | POD: devsecops-app                                                |   |   |
|   |   |                                                                   |   |   |
|   |   |  +------------------+         +--------------------------------+  |   |   |
|   |   |  | App Container    |         | Vault Sidecar Agent            |  |   |   |
|   |   |  | - Non-root 10001 |         | - Authenticates with K8s SA    |  |   |   |
|   |   |  | - ReadOnly Root  | <====== | - Injects secret into          |  |   |   |
|   |   |  | - Capabilities   | (Shared |   /vault/secrets/db-config.txt |  |   |   |
|   |   |  |   Dropped (ALL)  |  In-RAM | (Memory volume, no disk)       |  |   |   |
|   |   |  +------------------+  Volume)+--------------------------------+  |   |   |
|   |   +-------------------------------------------------------------------+   |   |
|   |                                                                           |   |
|   |   +-------------------------------------------------------------------+   |   |
|   |   | NetworkPolicy: Deny-All Default + Port 5000 Ingress Allow         |   |   |
|   |   +-------------------------------------------------------------------+   |   |
|   +---------------------------------------------------------------------------+   |
|                                                                                   |
|   +---------------------------------------------------------------------------+   |
|   | FALCO NAMESPACE (Runtime Threat Detection Engine)                         |   |
|   |                                                                           |   |
|   |   +-------------------------------------------------------------------+   |   |
|   |   | Falco eBPF / Kernel Probe Driver                                  |   |   |
|   |   | -> Monitored Event: kubectl exec / shell spawn in pod              |   |   |
|   |   | -> Action: Trigger WARNING alert log in real-time                  |   |   |
|   |   +-------------------------------------------------------------------+   |   |
|   +---------------------------------------------------------------------------+   |
+-----------------------------------------------------------------------------------+
