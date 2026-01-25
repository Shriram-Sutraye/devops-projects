# All Credentials

This file contains all credentials and access details for the CI/CD pipeline project.

> ⚠️ **SECURITY WARNING:** This file contains sensitive information. Do NOT commit to public repositories!

> 💡 **NOTE:** The Public IP changes every time you stop/start the EC2 instance. Update this file when that happens.

---

## 🖥️ EC2 Instance

| Field | Value |
|-------|-------|
| **Instance ID** | `i-0860e0e7ffe609373` |
| **Public IP** | `13.222.248.55` *(changes on restart)* |
| **Region** | `us-east-1` |
| **Instance Type** | `t3.large` |
| **Key File** | `jenkins.pem` |
| **SSH Command** | `ssh -i "/home/axonritts/Projects/devops-projects/jenkins.pem" ubuntu@13.222.248.55` |

---

## 🔧 Jenkins

| Field | Value |
|-------|-------|
| **URL** | http://13.222.248.55:8080 |
| **Username** | `admin` |
| **Password** | `Admin123.#` |
| **Initial Admin Password** | `7cb9e2f91bd8463a80d022f77441bfd2` |

---

## 🔍 SonarQube

| Field | Value |
|-------|-------|
| **URL** | http://13.222.248.55:9000 |
| **Username** | `admin` |
| **Password** | `Admin123.#` |
| **API Token** | `sqa_4b03602474d2a964e7265b77440f47a90adc9426` |
| **Token ID in Jenkins** | `sonarqube-token` |

---

## 🐳 Docker Hub (if needed later)

| Field | Value |
|-------|-------|
| **Username** | (to be configured) |
| **Password/Token** | (to be configured) |

---

## ☸️ Kubernetes (if needed later)

| Field | Value |
|-------|-------|
| **Cluster Name** | (to be configured) |
| **Kubeconfig Path** | (to be configured) |

---

## 🚀 Argo CD (if needed later)

| Field | Value |
|-------|-------|
| **URL** | (to be configured) |
| **Username** | (to be configured) |
| **Password** | (to be configured) |

---

## 📅 Last Updated

2026-01-25
