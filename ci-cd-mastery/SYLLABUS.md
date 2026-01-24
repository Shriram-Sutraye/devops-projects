# CI/CD Mastery Syllabus
## Complete Learning Path: Zero to Interview-Ready

> **Target Role:** DevOps/Infrastructure Engineer (5 years experience level)  
> **Resume Match:** Shriram Kumar's DevOps Resume  
> **Duration:** 3-4 weeks intensive | 6-8 weeks normal pace  
> **Last Updated:** January 2026

---

## 🎯 Learning Objectives

By the end of this course, you will be able to:

1. **Explain** CI/CD concepts confidently in interviews
2. **Write** production-quality pipeline code (Jenkinsfile, GitHub Actions workflows)
3. **Design** CI/CD architectures for real-world applications
4. **Troubleshoot** common pipeline failures
5. **Integrate** pipelines with Docker, Kubernetes, and AWS
6. **Answer** any CI/CD interview question for a 5-year experience level

---

## 📚 Module 0: Foundation Concepts
**Duration:** 1 day | **Priority:** CRITICAL

### 0.1 What is CI/CD?
- [ ] Definition of Continuous Integration (CI)
- [ ] Definition of Continuous Delivery vs Continuous Deployment (CD)
- [ ] The problem CI/CD solves (manual builds, integration hell, slow releases)
- [ ] The CI/CD pipeline lifecycle

### 0.2 Core Terminology
- [ ] **Pipeline** - The complete automated workflow
- [ ] **Stage** - A logical grouping of steps (Build, Test, Deploy)
- [ ] **Step/Task** - A single command or action
- [ ] **Job** - A collection of steps that run on one machine
- [ ] **Agent/Runner** - The machine that executes the pipeline
- [ ] **Artifact** - Output files from a build (JAR, Docker image, etc.)
- [ ] **Trigger** - What starts the pipeline (push, PR, schedule, manual)
- [ ] **Environment** - Target deployment location (dev, staging, prod)

### 0.3 CI/CD Best Practices (Interview Gold)
- [ ] Build once, deploy many
- [ ] Keep builds fast (< 10 minutes)
- [ ] Fail fast - run quick tests first
- [ ] Immutable artifacts
- [ ] Environment parity (dev = staging = prod)
- [ ] Trunk-based development vs feature branches
- [ ] Blue-green and canary deployments

### 0.4 Interview Questions - Module 0
- [ ] "What is CI/CD and why do we need it?"
- [ ] "Explain the difference between Continuous Delivery and Continuous Deployment"
- [ ] "What are the benefits of CI/CD for a development team?"
- [ ] "What happens when a developer pushes code in a CI/CD setup?"

---

## 📚 Module 1: GitHub Actions (Primary)
**Duration:** 5-7 days | **Priority:** HIGH

### 1.1 GitHub Actions Fundamentals
- [ ] What is GitHub Actions and how it differs from other CI tools
- [ ] GitHub-hosted vs Self-hosted runners
- [ ] Understanding the `.github/workflows/` directory
- [ ] YAML syntax essentials for workflows
- [ ] Free tier limits and billing considerations

### 1.2 Workflow File Structure (Deep Dive)
```yaml
# Every line explained:
name: <workflow-name>           # Display name in Actions tab
on: <triggers>                   # When does this run?
env: <global-variables>          # Environment variables for all jobs
jobs:
  <job-id>:
    runs-on: <runner>            # ubuntu-latest, windows-latest, self-hosted
    environment: <env-name>      # Optional: production, staging
    env: <job-variables>         # Job-specific env vars
    steps:
      - name: <step-name>
        uses: <action>           # Use a pre-built action
        with: <inputs>           # Inputs for the action
        run: <commands>          # OR run shell commands
        env: <step-variables>    # Step-specific env vars
```

### 1.3 Triggers (on:) - Complete Reference
- [ ] `push` - Run on code push
  - [ ] Branch filters (`branches: [main, develop]`)
  - [ ] Path filters (`paths: ['src/**']`)
  - [ ] Tag filters (`tags: ['v*']`)
- [ ] `pull_request` - Run on PR events
  - [ ] Types: opened, synchronize, closed, reopened
  - [ ] Target branch filters
- [ ] `workflow_dispatch` - Manual trigger with inputs
- [ ] `schedule` - Cron-based triggers
- [ ] `repository_dispatch` - External webhook triggers
- [ ] `workflow_call` - Reusable workflows

### 1.4 Jobs and Steps
- [ ] Job dependencies (`needs: [job1, job2]`)
- [ ] Job conditions (`if: github.ref == 'refs/heads/main'`)
- [ ] Matrix builds (testing multiple versions)
- [ ] Job outputs and passing data between jobs
- [ ] Parallelism and concurrency control
- [ ] Timeout settings

### 1.5 Actions (uses:)
- [ ] Understanding action syntax (`owner/repo@version`)
- [ ] Essential actions:
  - [ ] `actions/checkout@v4` - Clone your repo
  - [ ] `actions/setup-node@v4` - Setup Node.js
  - [ ] `actions/setup-python@v5` - Setup Python
  - [ ] `actions/cache@v4` - Dependency caching
  - [ ] `actions/upload-artifact@v4` - Save build outputs
  - [ ] `actions/download-artifact@v4` - Retrieve artifacts
- [ ] Docker actions
- [ ] Composite actions (reusable workflows)

### 1.6 Secrets and Variables
- [ ] Repository secrets (`${{ secrets.SECRET_NAME }}`)
- [ ] Environment secrets
- [ ] Organization secrets
- [ ] Variables vs Secrets (when to use each)
- [ ] GITHUB_TOKEN - built-in authentication
- [ ] Security best practices for secrets

### 1.7 Expressions and Contexts
- [ ] `${{ }}` expression syntax
- [ ] Context objects:
  - [ ] `github` - Event information, repo, ref, sha
  - [ ] `env` - Environment variables
  - [ ] `secrets` - Secret values
  - [ ] `job` - Current job info
  - [ ] `steps` - Previous step outputs
  - [ ] `runner` - Runner machine info
- [ ] Conditional expressions (`if:`)
- [ ] Functions: `contains()`, `startsWith()`, `format()`, `toJSON()`

### 1.8 Advanced GitHub Actions
- [ ] Reusable workflows (`workflow_call`)
- [ ] Composite actions (creating your own actions)
- [ ] Self-hosted runners setup on AWS EC2
- [ ] Job concurrency and cancellation
- [ ] Environment protection rules
- [ ] Manual approvals for production deployments
- [ ] Caching strategies for faster builds

### 1.9 Hands-On Projects - GitHub Actions
- [ ] **Project 1.1:** Hello World workflow
- [ ] **Project 1.2:** Node.js app - build, test, lint
- [ ] **Project 1.3:** Python app - build, test, coverage
- [ ] **Project 1.4:** Docker build and push to DockerHub
- [ ] **Project 1.5:** Deploy static site to GitHub Pages
- [ ] **Project 1.6:** Deploy to AWS S3 using AWS credentials
- [ ] **Project 1.7:** Multi-environment deployment (staging → production)
- [ ] **Project 1.8:** Matrix build - test on Node 18, 20, 22

### 1.10 Interview Questions - Module 1
- [ ] "Walk me through a GitHub Actions workflow you've written"
- [ ] "How do you handle secrets in GitHub Actions?"
- [ ] "What's the difference between `uses` and `run` in a step?"
- [ ] "How would you set up a workflow that only runs on the main branch?"
- [ ] "How do you cache dependencies in GitHub Actions?"
- [ ] "Explain GitHub Actions matrix builds"
- [ ] "How would you deploy to production with manual approval?"
- [ ] "What is `actions/checkout` and why is it needed?"

---

## 📚 Module 2: Jenkins (Enterprise Standard)
**Duration:** 7-10 days | **Priority:** HIGH

### 2.1 Jenkins Architecture
- [ ] What is Jenkins and its history
- [ ] Jenkins Controller (Master) vs Agents (Nodes)
- [ ] Distributed builds architecture
- [ ] Jenkins home directory structure
- [ ] Jenkins URL and reverse proxy setup
- [ ] Why enterprises still use Jenkins

### 2.2 Jenkins Installation & Setup
- [ ] Installation methods:
  - [ ] Docker (recommended for learning)
  - [ ] AWS EC2 installation
  - [ ] WAR file deployment
  - [ ] Package managers (apt, yum)
- [ ] Initial setup wizard
- [ ] Admin user creation
- [ ] Plugin installation
- [ ] System configuration basics

### 2.3 Jenkins Plugins (Essential Ones)
- [ ] **Pipeline** - Pipeline as Code support
- [ ] **Git** - Git integration
- [ ] **GitHub** - GitHub webhooks and status
- [ ] **Docker Pipeline** - Docker integration
- [ ] **Credentials** - Secrets management
- [ ] **Blue Ocean** - Modern UI
- [ ] **Slack Notification** - Team notifications
- [ ] **Email Extension** - Email alerts
- [ ] **AWS Steps** - AWS integrations
- [ ] **Kubernetes** - K8s agent provisioning

### 2.4 Jenkins Pipeline Types
- [ ] **Freestyle Project** - GUI-based (legacy, know but don't use)
- [ ] **Pipeline Project** - Single Jenkinsfile
- [ ] **Multibranch Pipeline** - Auto-discovers branches (production standard)
- [ ] **Organization Folder** - Scans entire GitHub org

### 2.5 Declarative Pipeline Syntax (Deep Dive)
```groovy
// Complete Jenkinsfile structure:
pipeline {
    agent any                    // Where to run

    options {                    // Pipeline options
        timeout(time: 1, unit: 'HOURS')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {                // Global env vars
        APP_NAME = 'my-app'
        DOCKER_REGISTRY = 'docker.io'
    }

    parameters {                 // User inputs
        string(name: 'BRANCH', defaultValue: 'main')
        booleanParam(name: 'DEPLOY', defaultValue: false)
        choice(name: 'ENV', choices: ['dev', 'staging', 'prod'])
    }

    triggers {                   // Auto-triggers
        pollSCM('H/5 * * * *')   // Poll Git every 5 min
        cron('H 2 * * *')        // Nightly at 2 AM
    }

    stages {
        stage('Build') {
            steps {
                // Build commands
            }
        }
        stage('Test') {
            parallel {           // Parallel stages
                stage('Unit Tests') { steps { } }
                stage('Integration Tests') { steps { } }
            }
        }
        stage('Deploy') {
            when {               // Conditional execution
                branch 'main'
                expression { params.DEPLOY == true }
            }
            steps {
                // Deploy commands
            }
        }
    }

    post {                       // Post-build actions
        always { }
        success { }
        failure { }
        unstable { }
    }
}
```

### 2.6 Declarative Pipeline - All Directives
- [ ] `agent` - Where to run (any, none, label, docker, kubernetes)
- [ ] `stages` - Container for all stages
- [ ] `stage` - Named phase of the pipeline
- [ ] `steps` - Actual commands to run
- [ ] `environment` - Environment variables
- [ ] `options` - Pipeline-level settings
- [ ] `parameters` - User-configurable inputs
- [ ] `triggers` - Automatic pipeline triggers
- [ ] `when` - Conditional stage execution
- [ ] `parallel` - Run stages in parallel
- [ ] `post` - Post-build actions (always, success, failure, etc.)
- [ ] `input` - Manual approval gates
- [ ] `tools` - Auto-install tools (JDK, Maven, etc.)

### 2.7 Scripted Pipeline (Know the Basics)
- [ ] Groovy-based syntax
- [ ] `node { }` block
- [ ] `stage { }` block
- [ ] When to use Scripted vs Declarative
- [ ] Shared libraries concept

### 2.8 Jenkins Credentials Management
- [ ] Credential types:
  - [ ] Username/Password
  - [ ] Secret text
  - [ ] Secret file
  - [ ] SSH private key
  - [ ] AWS credentials
- [ ] Credential scopes (Global, System, Folder)
- [ ] Using credentials in pipelines:
  - [ ] `withCredentials()` block
  - [ ] `credentials()` helper
  - [ ] Environment variable binding
- [ ] Credential security best practices

### 2.9 Jenkins Agents/Nodes
- [ ] Permanent agents vs Cloud agents
- [ ] Agent labels and selection
- [ ] Docker agents (`agent { docker { image 'node:20' } }`)
- [ ] Kubernetes agents (dynamic pod provisioning)
- [ ] SSH agent setup
- [ ] JNLP agent setup

### 2.10 Jenkins + Docker Integration
- [ ] Docker-in-Docker vs Docker socket mounting
- [ ] Building Docker images in Jenkins
- [ ] Running tests in Docker containers
- [ ] Docker agent for clean environments
- [ ] Pushing to Docker registries
- [ ] Docker Compose in pipelines

### 2.11 Jenkins + Git Integration
- [ ] Git plugin configuration
- [ ] GitHub webhook setup (step-by-step)
- [ ] Branch discovery for Multibranch
- [ ] Pull request builds
- [ ] Git credentials in Jenkins
- [ ] Commit status reporting to GitHub

### 2.12 Jenkins Shared Libraries
- [ ] What are Shared Libraries?
- [ ] Directory structure (`vars/`, `src/`, `resources/`)
- [ ] Creating reusable pipeline steps
- [ ] Loading libraries in Jenkinsfile
- [ ] When to use shared libraries

### 2.13 Jenkins Best Practices (Interview Gold)
- [ ] Pipeline as Code (Jenkinsfile in repo)
- [ ] Multibranch pipelines for all projects
- [ ] Keep builds under 10 minutes
- [ ] Use parallel stages where possible
- [ ] Archive important artifacts
- [ ] Clean workspace to save disk space
- [ ] Use credentials plugin, never hardcode secrets
- [ ] Implement proper failure notifications

### 2.14 Troubleshooting Jenkins
- [ ] Reading console logs effectively
- [ ] Common errors and fixes:
  - [ ] "No agent found with label X"
  - [ ] "Permission denied" errors
  - [ ] "Out of disk space"
  - [ ] "Build timeout"
  - [ ] "Credential not found"
- [ ] Jenkins log locations
- [ ] Pipeline replay feature
- [ ] Blue Ocean debugger

### 2.15 Hands-On Projects - Jenkins
- [ ] **Project 2.1:** Install Jenkins in Docker
- [ ] **Project 2.2:** Create first declarative pipeline
- [ ] **Project 2.3:** Build a Node.js app with npm
- [ ] **Project 2.4:** Build and push Docker image
- [ ] **Project 2.5:** Set up GitHub webhook integration
- [ ] **Project 2.6:** Multibranch pipeline with PR builds
- [ ] **Project 2.7:** Parallel testing stages
- [ ] **Project 2.8:** Deploy to AWS EC2/ECS
- [ ] **Project 2.9:** Pipeline with manual approval gate
- [ ] **Project 2.10:** Create a simple Shared Library

### 2.16 Interview Questions - Module 2
- [ ] "Explain the Jenkins architecture (master/agent)"
- [ ] "What's the difference between Declarative and Scripted pipeline?"
- [ ] "How do you handle credentials in Jenkins?"
- [ ] "Walk me through setting up a webhook from GitHub to Jenkins"
- [ ] "How do you troubleshoot a failed Jenkins build?"
- [ ] "What is a Multibranch Pipeline and why use it?"
- [ ] "How would you run tests in parallel in Jenkins?"
- [ ] "What plugins are essential for a Jenkins setup?"
- [ ] "How do you implement a deployment approval in Jenkins?"
- [ ] "What is a Jenkins Shared Library?"

---

## 📚 Module 3: AWS CodePipeline & CodeBuild
**Duration:** 3-4 days | **Priority:** MEDIUM

### 3.1 AWS CI/CD Services Overview
- [ ] CodeCommit - Git repository (optional, usually use GitHub)
- [ ] CodeBuild - Build and test service
- [ ] CodeDeploy - Deployment service
- [ ] CodePipeline - Orchestration layer
- [ ] How they work together

### 3.2 CodeBuild Deep Dive
- [ ] What is CodeBuild and when to use it
- [ ] Build environments (managed images)
- [ ] `buildspec.yml` file structure:
```yaml
version: 0.2
env:
  variables:
    APP_ENV: production
  secrets-manager:
    DB_PASSWORD: arn:aws:secretsmanager:...
phases:
  install:
    runtime-versions:
      nodejs: 18
    commands:
      - npm install
  pre_build:
    commands:
      - npm run lint
  build:
    commands:
      - npm run build
  post_build:
    commands:
      - echo "Build complete"
artifacts:
  files:
    - '**/*'
  base-directory: dist
cache:
  paths:
    - node_modules/**/*
```
- [ ] Build phases (install, pre_build, build, post_build)
- [ ] Artifacts and caching
- [ ] Environment variables and secrets
- [ ] VPC integration for private resources
- [ ] Build badges

### 3.3 CodePipeline Deep Dive
- [ ] Pipeline stages and actions
- [ ] Source stage (GitHub, CodeCommit, S3)
- [ ] Build stage (CodeBuild)
- [ ] Deploy stage (S3, ECS, EC2, Lambda)
- [ ] Manual approval actions
- [ ] Cross-account deployments
- [ ] Pipeline artifacts

### 3.4 CodeDeploy Basics
- [ ] Deployment targets (EC2, ECS, Lambda)
- [ ] `appspec.yml` file
- [ ] Deployment strategies:
  - [ ] In-place deployment
  - [ ] Blue/Green deployment
- [ ] Rollback capabilities

### 3.5 Hands-On Projects - AWS CI/CD
- [ ] **Project 3.1:** Create CodeBuild project for Node.js
- [ ] **Project 3.2:** Full CodePipeline: GitHub → CodeBuild → S3
- [ ] **Project 3.3:** Deploy to ECS Fargate with CodePipeline
- [ ] **Project 3.4:** Add manual approval before production

### 3.6 Interview Questions - Module 3
- [ ] "Explain AWS CodePipeline and its components"
- [ ] "What is a buildspec.yml and what are its sections?"
- [ ] "How would you deploy a Docker app to ECS using CodePipeline?"
- [ ] "What's the difference between CodeBuild and Jenkins?"
- [ ] "How do you handle secrets in CodeBuild?"

---

## 📚 Module 4: ArgoCD & GitOps
**Duration:** 2-3 days | **Priority:** MEDIUM-LOW

### 4.1 GitOps Concept
- [ ] What is GitOps?
- [ ] Git as the single source of truth
- [ ] Declarative infrastructure
- [ ] Pull-based vs Push-based deployments
- [ ] Benefits of GitOps

### 4.2 ArgoCD Fundamentals
- [ ] What is ArgoCD?
- [ ] ArgoCD architecture (Application Controller, API Server, Repo Server)
- [ ] ArgoCD Applications
- [ ] Sync strategies (Automatic vs Manual)
- [ ] Health status monitoring

### 4.3 ArgoCD Setup
- [ ] Installing ArgoCD on Kubernetes
- [ ] ArgoCD CLI
- [ ] ArgoCD UI
- [ ] Connecting Git repositories
- [ ] Creating Applications

### 4.4 ArgoCD Application Manifest
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/owner/repo.git
    targetRevision: HEAD
    path: k8s-manifests
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### 4.5 Hands-On Projects - ArgoCD
- [ ] **Project 4.1:** Install ArgoCD on minikube/EKS
- [ ] **Project 4.2:** Deploy app from Git manifests
- [ ] **Project 4.3:** Set up automated sync with self-healing

### 4.6 Interview Questions - Module 4
- [ ] "What is GitOps and why is it beneficial?"
- [ ] "Explain ArgoCD and how it works"
- [ ] "What is the difference between push and pull deployment models?"
- [ ] "How does ArgoCD know when to sync?"

---

## 📚 Module 5: CI/CD Integration Patterns
**Duration:** 2-3 days | **Priority:** HIGH

### 5.1 Docker in CI/CD
- [ ] Building Docker images in pipelines
- [ ] Multi-stage Dockerfile for smaller images
- [ ] Docker layer caching strategies
- [ ] Pushing to registries (DockerHub, ECR, GCR)
- [ ] Image tagging strategies (git sha, semver, latest)
- [ ] Security scanning (Trivy, Snyk)

### 5.2 Kubernetes Deployments from CI/CD
- [ ] kubectl apply in pipelines
- [ ] Helm chart deployments
- [ ] Kustomize for environment-specific configs
- [ ] Rolling updates vs Blue-Green
- [ ] Canary deployments

### 5.3 AWS Integrations
- [ ] Deploying to EC2 (SSH, CodeDeploy)
- [ ] Deploying to ECS (Fargate)
- [ ] Deploying to EKS
- [ ] Deploying to S3 (static sites)
- [ ] Deploying Lambda functions
- [ ] Terraform in CI/CD pipelines

### 5.4 Testing in CI/CD
- [ ] Unit tests (fast, run first)
- [ ] Integration tests (run in isolated containers)
- [ ] End-to-end tests (run against staging)
- [ ] Code coverage reports
- [ ] Static analysis (SonarQube, ESLint)
- [ ] Security scanning (SAST, DAST)

### 5.5 Notifications & Monitoring
- [ ] Slack notifications
- [ ] Email alerts
- [ ] GitHub commit status
- [ ] Build dashboards
- [ ] Metrics collection

---

## 📚 Module 6: Interview Preparation
**Duration:** 2-3 days | **Priority:** CRITICAL

### 6.1 Common Interview Scenarios
- [ ] "Design a CI/CD pipeline for a microservices application"
- [ ] "How would you implement zero-downtime deployments?"
- [ ] "A production deployment failed - walk me through your rollback process"
- [ ] "How do you handle database migrations in CI/CD?"
- [ ] "How would you secure your CI/CD pipeline?"

### 6.2 Whiteboard/Design Questions
- [ ] Draw a complete CI/CD architecture
- [ ] Explain flow from commit to production
- [ ] Multi-environment deployment strategy
- [ ] Disaster recovery for CI/CD systems

### 6.3 Troubleshooting Scenarios
- [ ] "Build is failing with permission denied - how do you debug?"
- [ ] "Pipeline is slow - how do you optimize?"
- [ ] "Secrets are exposed in logs - how do you fix and prevent?"
- [ ] "Docker build fails in CI but works locally - why?"

### 6.4 Tell Me About a Time... (STAR Stories)
- [ ] A CI/CD pipeline you improved
- [ ] A deployment that went wrong and how you fixed it
- [ ] How you implemented CI/CD at a previous company
- [ ] A time you automated a manual process

---

## 📊 Progress Tracking

### Completion Checklist

| Module | Status | Completion Date |
|--------|--------|-----------------|
| Module 0: Foundation | ⬜ Not Started | |
| Module 1: GitHub Actions | ⬜ Not Started | |
| Module 2: Jenkins | ⬜ Not Started | |
| Module 3: AWS CodePipeline | ⬜ Not Started | |
| Module 4: ArgoCD | ⬜ Not Started | |
| Module 5: Integration Patterns | ⬜ Not Started | |
| Module 6: Interview Prep | ⬜ Not Started | |

### Project Completion

| Project | Status | GitHub Link |
|---------|--------|-------------|
| 1.1 GHA Hello World | ⬜ | |
| 1.2 GHA Node.js App | ⬜ | |
| 1.3 GHA Python App | ⬜ | |
| 1.4 GHA Docker Build | ⬜ | |
| 1.5 GHA GitHub Pages | ⬜ | |
| 1.6 GHA AWS Deploy | ⬜ | |
| 1.7 GHA Multi-env | ⬜ | |
| 1.8 GHA Matrix Build | ⬜ | |
| 2.1 Jenkins Docker Install | ⬜ | |
| 2.2 Jenkins First Pipeline | ⬜ | |
| 2.3 Jenkins Node.js | ⬜ | |
| 2.4 Jenkins Docker Build | ⬜ | |
| 2.5 Jenkins Webhook | ⬜ | |
| 2.6 Jenkins Multibranch | ⬜ | |
| 2.7 Jenkins Parallel | ⬜ | |
| 2.8 Jenkins AWS Deploy | ⬜ | |
| 2.9 Jenkins Approval Gate | ⬜ | |
| 2.10 Jenkins Shared Library | ⬜ | |
| 3.1 CodeBuild Node.js | ⬜ | |
| 3.2 CodePipeline to S3 | ⬜ | |
| 3.3 CodePipeline to ECS | ⬜ | |
| 3.4 CodePipeline Approval | ⬜ | |
| 4.1 ArgoCD Install | ⬜ | |
| 4.2 ArgoCD Git Deploy | ⬜ | |
| 4.3 ArgoCD Auto Sync | ⬜ | |

---

## 📁 Recommended Folder Structure

```
ci-cd-mastery/
├── SYLLABUS.md                    # This file
├── module-0-foundation/
│   └── notes.md
├── module-1-github-actions/
│   ├── notes.md
│   ├── cheatsheet.md
│   └── projects/
│       ├── 01-hello-world/
│       ├── 02-nodejs-app/
│       ├── 03-python-app/
│       ├── 04-docker-build/
│       ├── 05-github-pages/
│       ├── 06-aws-deploy/
│       ├── 07-multi-env/
│       └── 08-matrix-build/
├── module-2-jenkins/
│   ├── notes.md
│   ├── cheatsheet.md
│   └── projects/
│       ├── 01-docker-install/
│       ├── 02-first-pipeline/
│       ├── 03-nodejs-app/
│       ├── 04-docker-build/
│       ├── 05-webhook-setup/
│       ├── 06-multibranch/
│       ├── 07-parallel-tests/
│       ├── 08-aws-deploy/
│       ├── 09-approval-gate/
│       └── 10-shared-library/
├── module-3-aws-cicd/
│   ├── notes.md
│   ├── cheatsheet.md
│   └── projects/
│       ├── 01-codebuild-nodejs/
│       ├── 02-pipeline-s3/
│       ├── 03-pipeline-ecs/
│       └── 04-pipeline-approval/
├── module-4-argocd/
│   ├── notes.md
│   └── projects/
│       ├── 01-install/
│       ├── 02-git-deploy/
│       └── 03-auto-sync/
├── module-5-integration/
│   └── notes.md
├── module-6-interview/
│   ├── questions-answers.md
│   ├── design-scenarios.md
│   └── star-stories.md
└── resources/
    ├── sample-apps/
    ├── dockerfiles/
    └── useful-links.md
```

---

## 🔗 Learning Resources

### Official Documentation
- GitHub Actions: https://docs.github.com/en/actions
- Jenkins: https://www.jenkins.io/doc/book/pipeline/
- AWS CodePipeline: https://docs.aws.amazon.com/codepipeline/
- ArgoCD: https://argo-cd.readthedocs.io/

### YouTube Channels
- TechWorld with Nana
- DevOps Directive
- FreeCodeCamp
- CloudBees (Jenkins)

### Practice Platforms
- Killercoda (free Jenkins labs)
- Play with Docker
- AWS Free Tier

---

> **Next Step:** Start with Module 0, then proceed sequentially. Each module builds on the previous one.
