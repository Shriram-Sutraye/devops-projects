# 06 - Pipeline Setup

This document covers setting up the Jenkins pipeline for the Spring Boot application.

---

## Overview

The pipeline automates:
1. **Checkout** - Pull code from GitHub
2. **Build & Test** - Compile with Maven, run tests
3. **Static Code Analysis** - Scan with SonarQube
4. **Build Docker Image** - Create container image

---

## Prerequisites

Before setting up the pipeline, ensure:
- ✅ Jenkins is running (port 8080)
- ✅ SonarQube is running (port 9000)
- ✅ Docker is installed and Jenkins has Docker access
- ✅ SonarQube token is saved in Jenkins credentials

---

## Step 1: Add SonarQube Credential

1. Go to: **Manage Jenkins** → **Credentials** → **Global**
2. Click **Add Credentials**
3. Fill in:
   - **Kind:** `Secret text`
   - **Secret:** `sqa_4b03602474d2a964e7265b77440f47a90adc9426`
   - **ID:** `sonarqube-token`
   - **Description:** `SonarQube Token`
4. Click **Create**

---

## Step 2: Configure SonarQube Server (Optional)

1. Go to: **Manage Jenkins** → **System**
2. Scroll to **SonarQube servers**
3. Check **Environment variables**
4. Click **Add SonarQube**
5. Fill in:
   - **Name:** `sonarqube`
   - **Server URL:** `http://13.222.248.55:9000`
   - **Token:** Select `sonarqube-token`
6. Click **Save**

---

## Step 3: Create Pipeline Job

1. Go to Jenkins Dashboard
2. Click **New Item**
3. Enter name: `spring-boot-pipeline`
4. Select **Pipeline**
5. Click **OK**

### Configure Pipeline

In the job configuration:

1. Scroll to **Pipeline** section
2. Set **Definition:** `Pipeline script from SCM`
3. Set **SCM:** `Git`
4. Set **Repository URL:** `https://github.com/Shriram-Sutraye/devops-projects.git`
5. Set **Branch:** `*/master`
6. Set **Script Path:** `Jenkins-Zero-To-Hero/java-maven-sonar-argocd-helm-k8s/spring-boot-app/JenkinsFile`
7. Click **Save**

---

## Step 4: Run the Pipeline

1. Click **Build Now**
2. Watch the stages execute:
   - Checkout ✅
   - Build and Test ✅
   - Static Code Analysis ✅
   - Build Docker Image ✅

---

## The Jenkinsfile

Location: `Jenkins-Zero-To-Hero/java-maven-sonar-argocd-helm-k8s/spring-boot-app/JenkinsFile`

```groovy
pipeline {
  agent {
    docker {
      image 'abhishekf5/maven-abhishek-docker-agent:v1'
      args '--user root -v /var/run/docker.sock:/var/run/docker.sock'
    }
  }
  stages {
    stage('Checkout') {
      steps {
        sh 'echo "Checkout passed"'
      }
    }
    stage('Build and Test') {
      steps {
        sh 'cd Jenkins-Zero-To-Hero/java-maven-sonar-argocd-helm-k8s/spring-boot-app && mvn clean package'
      }
    }
    stage('Static Code Analysis') {
      environment {
        SONAR_URL = "http://13.222.248.55:9000"
      }
      steps {
        withCredentials([string(credentialsId: 'sonarqube-token', variable: 'SONAR_AUTH_TOKEN')]) {
          sh 'cd Jenkins-Zero-To-Hero/java-maven-sonar-argocd-helm-k8s/spring-boot-app && mvn org.sonarsource.scanner.maven:sonar-maven-plugin:sonar -Dsonar.login=$SONAR_AUTH_TOKEN -Dsonar.host.url=${SONAR_URL}'
        }
      }
    }
    stage('Build Docker Image') {
      steps {
        sh 'cd Jenkins-Zero-To-Hero/java-maven-sonar-argocd-helm-k8s/spring-boot-app && docker build -t spring-boot-app:${BUILD_NUMBER} .'
        sh 'echo "Docker image built successfully!"'
      }
    }
  }
}
```

---

## Key Concepts

### Docker Agent
The pipeline runs inside a Docker container (`abhishekf5/maven-abhishek-docker-agent:v1`) which has Maven pre-installed.

### Docker-in-Docker
The `-v /var/run/docker.sock:/var/run/docker.sock` flag allows building Docker images from within the container.

### Credentials
The `withCredentials` block injects the SonarQube token securely without exposing it in logs.

---

## Troubleshooting

### "No plugin found for prefix 'sonar'"
Use the full plugin name:
```
mvn org.sonarsource.scanner.maven:sonar-maven-plugin:sonar
```

### "docker-cred" error
Docker Hub credentials not configured. Skip the Docker push stage or add credentials.

### Path not found errors
Ensure paths include `Jenkins-Zero-To-Hero/` prefix since the project is nested.

---

## Next Steps

- [ ] Configure Docker Hub credentials for image push
- [ ] Set up Kubernetes cluster
- [ ] Configure Argo CD for GitOps deployment
