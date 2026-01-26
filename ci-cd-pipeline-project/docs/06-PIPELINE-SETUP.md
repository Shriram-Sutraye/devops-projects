# 06 - Pipeline Setup (Complete)

This section guides you through creating the Jenkins pipeline that ties everything together.

---

## 🎯 Goal
Create a "Pipeline" job in Jenkins that:
1. Pulls code from GitHub
2. Builds Java Code (Maven)
3. Scans for Bugs (SonarQube)
4. Builds Docker Image
5. Pushes Image to Docker Hub
6. Updates Deployment Manifest in GitHub

---

## 📋 Prerequisites
- You must have all 3 credentials in Jenkins (SonarQube, Docker, GitHub).
- You must have the `Jenkinsfile` in your repository.

---

## 🚀 Step 1: Create the Job

1. Open Jenkins: `http://<YOUR-EC2-IP>:8080`
2. Click **"New Item"** (top-left menu).
3. **Enter an item name:** `spring-boot-pipeline`
4. **Select type:** Click **"Pipeline"** (scrolling down slightly).
5. Click **"OK"** button at the bottom.

---

## ⚙️ Step 2: Configure the Pipeline

You are now on the configuration screen. Scroll down to the **"Pipeline"** section (at the bottom).

### Settings to Enter:
1. **Definition:** Select `Pipeline script from SCM` from the dropdown.
2. **SCM:** Select `Git`.
3. **Repository URL:** `https://github.com/<YOUR-GITHUB-USERNAME>/devops-projects.git`
4. **Branch Specifier:** `*/master` (or `*/main` depending on your repo).
5. **Script Path:** 
   ```
   Jenkins-Zero-To-Hero/java-maven-sonar-argocd-helm-k8s/spring-boot-app/JenkinsFile
   ```
   *(Copy this path exactly!)*

6. Click **"Save"** button.

---

## ▶️ Step 3: Run the Pipeline

1. You should now be on the job dashboard.
2. Click **"Build Now"** (left sidebar).
3. Look at the **"Build History"** (bottom left). You will see a blinking circle.
4. Click on the **build number** (e.g., `#1`).
5. Click **"Pipeline Overview"** or **"Console Output"** to see what's happening.

---

## ✅ Step 4: Verify Success

A successful build will show **Green Blocks** for every stage:

1. **Checkout SCM:** Git pull successful.
2. **Build and Test:** Maven compiled the app.
3. **Static Code Analysis:** SonarQube checked the code.
4. **Build and Push Docker Image:** Pushed to your Docker Hub.
5. **Update Deployment File:** Updated `deployment.yml` in your GitHub.

---

## 📄 Reference: The Final Jenkinsfile

This is the code running inside your pipeline:

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
    stage('Build and Push Docker Image') {
      environment {
        DOCKER_IMAGE = "shriramsutraye/spring-boot-app:${BUILD_NUMBER}"
        REGISTRY_CREDENTIALS = credentials('docker-cred')
      }
      steps {
        script {
          sh 'cd Jenkins-Zero-To-Hero/java-maven-sonar-argocd-helm-k8s/spring-boot-app && docker build -t ${DOCKER_IMAGE} .'
          def dockerImage = docker.image("${DOCKER_IMAGE}")
          docker.withRegistry('https://index.docker.io/v1/', "docker-cred") {
            dockerImage.push()
          }
        }
      }
    }
    stage('Update Deployment File') {
      environment {
        GIT_REPO_NAME = "devops-projects"
        GIT_USER_NAME = "Shriram-Sutraye"
      }
      steps {
        withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
          sh '''
            git config user.email "shriram@example.com"
            git config user.name "Shriram Sutraye"
            BUILD_NUMBER=${BUILD_NUMBER}
            sed -i "s/replaceImageTag/${BUILD_NUMBER}/g" Jenkins-Zero-To-Hero/java-maven-sonar-argocd-helm-k8s/spring-boot-app-manifests/deployment.yml
            git add Jenkins-Zero-To-Hero/java-maven-sonar-argocd-helm-k8s/spring-boot-app-manifests/deployment.yml
            git commit -m "Update deployment image to version ${BUILD_NUMBER}"
            git push https://${GITHUB_TOKEN}@github.com/${GIT_USER_NAME}/${GIT_REPO_NAME} HEAD:master
          '''
        }
      }
    }
  }
}
```
