# Jenkins CI/CD Pipeline Project

## 🎯 Project Goal

Build a complete, production-grade CI/CD pipeline for a Java application using:

| Tool | Purpose |
|------|---------|
| **Jenkins** | Automation server - the brain of CI/CD |
| **Maven** | Build tool for Java applications |
| **SonarQube** | Code quality & security scanner |
| **Docker** | Containerization |
| **Kubernetes** | Container orchestration |
| **Argo CD** | GitOps continuous deployment |
| **Helm** | Kubernetes package manager |

---

## 🔄 Pipeline Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   GitHub    │────▶│   Jenkins   │────▶│  SonarQube  │────▶│   Docker    │
│  (Source)   │     │   (Build)   │     │  (Quality)  │     │   (Image)   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                                                                   │
                                                                   ▼
                    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
                    │    App      │◀────│   Argo CD   │◀────│ Kubernetes  │
                    │  (Running)  │     │  (GitOps)   │     │  (Deploy)   │
                    └─────────────┘     └─────────────┘     └─────────────┘
```

---

## 📁 Project Structure

```
ci-cd-pipeline-project/
├── docs/                          # You are here
│   ├── 01-PROJECT-OVERVIEW.md     # This file
│   ├── 02-EC2-SETUP.md            # EC2 instance setup
│   ├── 03-JENKINS-INSTALLATION.md # Jenkins install & config
│   ├── 04-DOCKER-SETUP.md         # Docker installation
│   ├── 05-SONARQUBE-SETUP.md      # SonarQube configuration
│   ├── 06-KUBERNETES-SETUP.md     # K8s cluster setup (upcoming)
│   ├── 07-ARGOCD-SETUP.md         # Argo CD configuration (upcoming)
│   └── CREDENTIALS.md             # All credentials in one place
└── app/                           # Application code (upcoming)
```

---

## 📚 Learning Resources

- **Original Project:** [Jenkins-Zero-To-Hero](https://github.com/iam-veeramalla/Jenkins-Zero-To-Hero)
- **Video Tutorial:** [YouTube - Abhishek Veeramalla](https://www.youtube.com/watch?v=zZfhAXfBvVA)

---

## 📅 Progress Tracker

| Step | Status | Date |
|------|--------|------|
| EC2 Instance Setup | ✅ Complete | 2026-01-25 |
| Jenkins Installation | ✅ Complete | 2026-01-25 |
| Docker Installation | ✅ Complete | 2026-01-25 |
| SonarQube Setup | ✅ Complete | 2026-01-25 |
| Jenkins ↔ SonarQube Integration | 🔄 In Progress | 2026-01-25 |
| Kubernetes Cluster | ⏳ Pending | - |
| Argo CD Setup | ⏳ Pending | - |
| Full Pipeline Test | ⏳ Pending | - |
