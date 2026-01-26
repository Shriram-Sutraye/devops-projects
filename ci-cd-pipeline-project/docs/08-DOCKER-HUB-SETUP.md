# 08 - Docker Hub Setup & Full Pipeline

This guide shows you how to push Docker images to Docker Hub and run the complete CI/CD pipeline.

---

## 📋 What You'll Do

Before this chapter, your pipeline:
- ✅ Built Docker images locally
- ❌ Couldn't share them with others

After this chapter:
- ✅ Pushes images to Docker Hub (public registry)
- ✅ Updates deployment files automatically
- ✅ Ready for Kubernetes deployment

---

## 🎯 Part 1: Create Docker Hub Account

### Step 1: Sign Up

1. Go to: https://hub.docker.com
2. Click **"Sign Up"** (top-right corner)
3. Fill in:
   - **Username:** Choose carefully - you'll use this in image names
   - **Email:** Your email
   - **Password:** Strong password
4. Click **"Sign Up"**
5. **Verify your email** (check inbox for verification email)

### Step 2: Log In

1. Go to: https://hub.docker.com
2. Click **"Sign In"**
3. Enter your username and password
4. You should see your dashboard

---

## 🔑 Part 2: Create Access Token

> ⚠️ **Never use your password in Jenkins!** Always use access tokens.

### Step 1: Navigate to Security Settings

1. Click your **profile icon** (top-right corner)
2. Click **"My Account"** from dropdown
3. Click **"Security"** tab on the left sidebar
4. Look for **"Personal access tokens"** section

### Step 2: Generate Token

1. Click **"New Access Token"** button
2. Fill in:
   - **Token description:** `jenkins` (or any name you like)
   - **Access permissions:** Select **"Read & Write"**
3. Click **"Generate"**

### Step 3: Copy the Token

1. You'll see a token like: `dckr_pat_xxxxxxxxxxxxxxxxxxxxx`
2. **COPY IT IMMEDIATELY** - it only shows once!
3. Save it somewhere safe (you'll need it in the next step)

> 💡 **Lost the token?** You can always delete it and create a new one.

---

## 🔧 Part 3: Add Docker Hub Credentials to Jenkins

### Step 1: Open Jenkins Credentials

1. Open browser and go to: `http://<YOUR-EC2-IP>:8080`
2. Log in with your Jenkins admin credentials
3. Click **"Manage Jenkins"** (left sidebar)
4. Look for **"Credentials"** in the list and click it
5. Click **"System"** under "Stores scoped to Jenkins"
6. Click **"Global credentials (unrestricted)"**

### Step 2: Add New Credential

1. Click **"+ Add Credentials"** button (top-right area)
2. You'll see a form with several fields

### Step 3: Fill in the Form

| Field | What to Enter | Example |
|-------|---------------|---------|
| **Kind** | Select "Username with password" from dropdown | Username with password |
| **Scope** | Leave as "Global" | Global (Jenkins, nodes, items, all child...) |
| **Username** | Your Docker Hub username | `shriramsutraye` |
| **Password** | Paste the Docker Hub access token | `dckr_pat_eRt5LUW...` |
| **ID** | `docker-cred` | `docker-cred` |
| **Description** | `Docker Hub Credentials` | Docker Hub Credentials |

> ⚠️ **CRITICAL:** The ID must be exactly `docker-cred` (no spaces, no typos!)

### Step 4: Save

1. Click **"Create"** button at the bottom
2. You should see `docker-cred` in the credentials list
3. **Success!** Jenkins can now push to Docker Hub

---

## 🐙 Part 4: Create GitHub Personal Access Token

The pipeline needs to push changes back to GitHub.

### Step 1: Navigate to GitHub Settings

1. Go to: https://github.com/settings/tokens
2. Or: Click your profile → Settings → Developer settings → Personal access tokens → Tokens (classic)

### Step 2: Generate Token

1. Click **"Generate new token"** dropdown
2. Select **"Generate new token (classic)"**
3. Fill in:
   - **Note:** `jenkins` (what this token is for)
   - **Expiration:** Choose `30 days` or `No expiration` (for learning)
   - **Select scopes:** Check ✅ **`repo`** (this gives full control of repositories)
4. Scroll down and click **"Generate token"**

### Step 3: Copy the Token

1. You'll see a token starting with `ghp_` or `gho_`
2. **COPY IT** - you can't see it again!
3. Example: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

## 🔧 Part 5: Add GitHub Token to Jenkins

### Step 1: Back to Jenkins Credentials

1. Go back to Jenkins: `http://<YOUR-EC2-IP>:8080/manage/credentials/`
2. Navigate to: System → Global credentials (same place as before)
3. Click **"+ Add Credentials"** again

### Step 2: Fill in the Form

| Field | What to Enter |
|-------|---------------|
| **Kind** | Select "Secret text" |
| **Scope** | Leave as "Global" |
| **Secret** | Paste your GitHub token |
| **ID** | `github-token` |
| **Description** | `GitHub Token for Jenkins` |

> ⚠️ **CRITICAL:** The ID must be exactly `github-token`

### Step 3: Save

1. Click **"Create"**
2. **Verify:** You should now see 3 credentials:
   - `sonarqube-token`
   - `docker-cred`
   - `github-token`

---

## 📝 Part 6: Update the Jenkinsfile

Your Jenkinsfile needs two new stages.

### Option A: Use Git Commands (Recommended)

In your local terminal:

```bash
cd ~/Projects/devops-projects
git pull origin master
```

The Jenkinsfile should already be updated. If not, continue to Option B.

### Option B: Manual Update

Open the Jenkinsfile:
```bash
nano Jenkins-Zero-To-Hero/java-maven-sonar-argocd-helm-k8s/spring-boot-app/JenkinsFile
```

Add these two stages after the "Static Code Analysis" stage:

```groovy
    stage('Build and Push Docker Image') {
      environment {
        DOCKER_IMAGE = "<YOUR-DOCKERHUB-USERNAME>/spring-boot-app:${BUILD_NUMBER}"
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
        GIT_USER_NAME = "<YOUR-GITHUB-USERNAME>"
      }
      steps {
        withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
          sh '''
            git config user.email "you@example.com"
            git config user.name "Your Name"
            BUILD_NUMBER=${BUILD_NUMBER}
            sed -i "s/replaceImageTag/${BUILD_NUMBER}/g" Jenkins-Zero-To-Hero/java-maven-sonar-argocd-helm-k8s/spring-boot-app-manifests/deployment.yml
            git add Jenkins-Zero-To-Hero/java-maven-sonar-argocd-helm-k8s/spring-boot-app-manifests/deployment.yml
            git commit -m "Update deployment image to version ${BUILD_NUMBER}"
            git push https://${GITHUB_TOKEN}@github.com/${GIT_USER_NAME}/${GIT_REPO_NAME} HEAD:master
          '''
        }
      }
    }
```

**Replace:**
- `<YOUR-DOCKERHUB-USERNAME>` with your Docker Hub username (e.g., `shriramsutraye`)
- `<YOUR-GITHUB-USERNAME>` with your GitHub username (e.g., `Shriram-Sutraye`)
- `you@example.com` with your email
- `Your Name` with your name

Save and push:
```bash
git add -A
git commit -m "Add Docker Hub push and deployment update stages"
git push origin master
```

---

## 🚀 Part 7: Run the Full Pipeline

### Step 1: Navigate to Your Pipeline

1. Go to Jenkins: `http://<YOUR-EC2-IP>:8080`
2. Click on **"spring-boot-pipeline"** in the dashboard

### Step 2: Start a Build

1. Click **"Build Now"** (left sidebar)
2. You'll see a new build appear in "Build History" (bottom-left)
3. The build number will appear with a **blue progress bar**

### Step 3: Watch the Progress

1. Click on the **build number** (e.g., #6, #7)
2. Click **"Console Output"** to see live logs
3. Or click **"Pipeline Overview"** to see stage progress

### What to Expect:

| Stage | Duration | What Happens |
|-------|----------|--------------|
| Checkout SCM | ~1s | Pulls code from GitHub |
| Checkout | ~1s | Confirmation |
| Build and Test | ~30s | Maven compiles and tests |
| Static Code Analysis | ~30s | SonarQube scans code |
| **Build and Push Docker Image** | **~10s** | **Builds and uploads to Docker Hub** |
| **Update Deployment File** | **~1s** | **Updates manifest in GitHub** |

Total time: **~1-2 minutes**

### Step 4: Verify Success

✅ **Green checkmark** next to all stages = SUCCESS!

❌ **Red X** = Something failed (check console output for errors)

---

## ✅ Part 8: Verify Docker Hub

### Check Your Image

1. Go to: https://hub.docker.com
2. Log in
3. Click **"Repositories"** (top menu)
4. You should see: **`spring-boot-app`**
5. Click on it
6. You should see tags like `:1`, `:2`, `:6`, etc. (one for each build)

**Example URL:** `https://hub.docker.com/r/shriramsutraye/spring-boot-app`

---

## ✅ Part 9: Verify GitHub Update

### Check the Commit

1. Go to your GitHub repository
2. Navigate to: `Jenkins-Zero-To-Hero/java-maven-sonar-argocd-helm-k8s/spring-boot-app-manifests/deployment.yml`
3. You should see a recent commit: **"Update deployment image to version X"**
4. Look at the file - the image tag should match your build number

---

## 🛑 Troubleshooting

### "Permission denied while trying to connect to Docker daemon"

**Cause:** Jenkins user doesn't have Docker access

**Fix:**
```bash
ssh -i jenkins.pem ubuntu@<YOUR-EC2-IP>
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
sudo systemctl restart docker
```

### "docker-cred not found"

**Cause:** Credential ID doesn't match

**Fix:**
1. Go to Jenkins → Manage Jenkins → Credentials
2. Check the ID is exactly `docker-cred` (no typos, no spaces)
3. If wrong, delete it and create again

### "unauthorized: authentication required"

**Cause:** Wrong Docker Hub token or username

**Fix:**
1. Delete the `docker-cred` credential in Jenkins
2. Generate a new token in Docker Hub
3. Add it again to Jenkins

### "github-token not found"

**Cause:** Credential ID doesn't match

**Fix:**
- Check the ID is exactly `github-token`
- Verify it exists in Jenkins credentials

### Docker build fails with "no such file or directory"

**Cause:** Wrong path in Jenkinsfile

**Fix:**
- Make sure paths include `Jenkins-Zero-To-Hero/java-maven-sonar-argocd-helm-k8s/spring-boot-app`

---

## 📝 Summary

| What We Did | Why |
|-------------|-----|
| Created Docker Hub account | Public place to store images |
| Generated access token | Secure authentication (not password!) |
| Added credentials to Jenkins | Let Jenkins push images |
| Created GitHub token | Let Jenkins update deployment files |
| Updated Jenkinsfile | Added push and update stages |
| Ran pipeline | Tested everything end-to-end |

**Next Step:** Set up Kubernetes cluster to actually deploy the app!

---

## 🎯 Your Progress

| Stage | Status |
|-------|--------|
| 1. Code → Build | ✅ |
| 2. SonarQube Scan | ✅ |
| 3. Docker Build | ✅ |
| 4. Docker Push | ✅ **← You are here** |
| 5. Update Manifests | ✅ |
| 6. Kubernetes Deploy | ⏳ Next |
| 7. Argo CD GitOps | ⏳ After K8s |
