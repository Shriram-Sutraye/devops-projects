# Complete CI/CD Pipeline Setup Guide
## Jenkins + Kubernetes (AWS EKS) + Argo CD + Docker Hub

> **Target Audience**: Complete beginners with minimal DevOps experience  
> **Time Required**: 3-4 hours  
> **Cost**: ~$0.50-$2.00/hour for AWS resources

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [AWS Account & CLI Setup](#aws-account--cli-setup)
3. [Installing kubectl](#installing-kubectl)
4. [Installing eksctl](#installing-eksctl)
5. [Creating the EKS Cluster](#creating-the-eks-cluster)
6. [Setting Up Argo CD](#setting-up-argo-cd)
7. [Configuring Jenkins Credentials](#configuring-jenkins-credentials)
8. [Creating the Jenkins Pipeline](#creating-the-jenkins-pipeline)
9. [Running Your First Build](#running-your-first-build)
10. [Fixing Service Access (LoadBalancer)](#fixing-service-access-loadbalancer)
11. [Verifying the Complete Pipeline](#verifying-the-complete-pipeline)
12. [Troubleshooting Common Issues](#troubleshooting-common-issues)

---

## What You'll Build

By the end of this guide, you will have:
- A **Kubernetes cluster** running on AWS (Amazon EKS)
- A **Jenkins server** that automatically builds and tests your code
- **Argo CD** that automatically deploys your application to Kubernetes
- A **live Spring Boot web application** accessible from anywhere on the internet

**The Flow**:
1. You push code to GitHub
2. Jenkins automatically detects the change
3. Jenkins builds your app, runs tests, and creates a Docker image
4. Jenkins pushes the image to Docker Hub
5. Jenkins updates the Kubernetes configuration in GitHub
6. Argo CD detects the change and deploys to your cluster
7. Your app is live on the internet!

---

## Prerequisites

### Required Accounts
You need to create **free accounts** on these platforms before starting:

#### 1. AWS Account
- Go to https://aws.amazon.com
- Click "Create an AWS Account"
- Follow the signup process (requires credit card, but we'll use free tier)
- **IMPORTANT**: You'll be charged for EC2 instances and Load Balancers. Budget ~$2-5 for this tutorial

#### 2. GitHub Account
- Go to https://github.com
- Click "Sign up"
- Create your account (completely free)

#### 3. Docker Hub Account
- Go to https://hub.docker.com
- Click "Sign up"
- Create your account (free tier is sufficient)

#### 4. Jenkins Server
For this guide, we assume you already have:
- A Jenkins server running on an AWS EC2 instance
- The public IP address of that server
- Admin access to Jenkins

If you don't have Jenkins yet, follow a separate Jenkins installation guide first.

### Required Tools on Your Computer

You'll need to install these tools on your local machine:

1. **AWS CLI** - Command-line tool to interact with AWS
2. **kubectl** - Command-line tool to interact with Kubernetes
3. **eksctl** - Command-line tool to create EKS clusters easily
4. **Git** - Version control (you probably already have this)

We'll install these step-by-step below.

---

## AWS Account & CLI Setup

### Step 1: Install AWS CLI

#### For Linux (Ubuntu/Debian):
Open your terminal and run these commands **one at a time**:

```bash
# Download the AWS CLI installer
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

# Unzip it (install unzip if you don't have it)
unzip awscliv2.zip

# Install AWS CLI
sudo ./aws/install

# Verify installation
aws --version
```

You should see output like: `aws-cli/2.x.x Python/3.x.x Linux/x.x.x`

#### For Mac:
```bash
# Download and install
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /

# Verify
aws --version
```

#### For Windows:
1. Download the installer from: https://awscli.amazonaws.com/AWSCLIV2.msi
2. Run the downloaded `.msi` file
3. Open Command Prompt and run: `aws --version`

### Step 2: Create AWS Access Keys

1. **Log in to AWS Console**: https://console.aws.amazon.com
2. Click on your username in the top-right corner
3. Click **"Security credentials"**
4. Scroll down to **"Access keys"** section
5. Click **"Create access key"**
6. Choose **"Command Line Interface (CLI)"**
7. Check the box that says "I understand..."
8. Click **"Next"**
9. Optionally add a description tag (like "my-laptop")
10. Click **"Create access key"**
11. **CRITICAL**: Click **"Download .csv file"** and save it somewhere safe
12. You'll see:
    - **Access Key ID**: Looks like `AKIAIOSFODNN7EXAMPLE`
    - **Secret Access Key**: Looks like `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

> ⚠️ **NEVER** share these keys or commit them to GitHub. They're like passwords to your AWS account.

### Step 3: Configure AWS CLI

In your terminal, run:

```bash
aws configure
```

You'll be prompted for 4 things:

```
AWS Access Key ID [None]: <paste your Access Key ID>
AWS Secret Access Key [None]: <paste your Secret Access Key>
Default region name [None]: us-east-1
Default output format [None]: json
```

**Explanation**:
- **Region**: `us-east-1` is Virginia, USA. You can choose others like `us-west-2`, `eu-west-1`, etc.
- **Output format**: `json` is the most common format

To verify it worked:
```bash
aws sts get-caller-identity
```

You should see output with your AWS Account ID and user ARN.

---

## Installing kubectl

`kubectl` is the tool you use to talk to Kubernetes clusters.

### For Linux:

Run these commands:

```bash
# Download kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Make it executable
chmod +x kubectl

# Move it to your PATH
sudo mv kubectl /usr/local/bin/

# Verify installation
kubectl version --client
```

### For Mac:

```bash
# Using Homebrew (if you have it)
brew install kubectl

# OR manually
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Verify
kubectl version --client
```

### For Windows:

1. Download from: https://dl.k8s.io/release/v1.28.0/bin/windows/amd64/kubectl.exe
2. Add the folder containing `kubectl.exe` to your PATH
3. Open Command Prompt and run: `kubectl version --client`

---

## Installing eksctl

`eksctl` is a tool that makes creating EKS clusters super easy.

### For Linux:

```bash
# Download eksctl
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp

# Move to PATH
sudo mv /tmp/eksctl /usr/local/bin

# Verify
eksctl version
```

### For Mac:

```bash
# Using Homebrew
brew tap weaveworks/tap
brew install weaveworks/tap/eksctl

# Verify
eksctl version
```

### For Windows:

1. Download from: https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_Windows_amd64.zip
2. Extract it
3. Add to your PATH
4. Run: `eksctl version`

---

## Creating the EKS Cluster

Now we'll create a Kubernetes cluster on AWS. This is the "computer farm" where your app will run.

### Step 1: Create the Cluster

**IMPORTANT**: This step takes **15-20 minutes**. Don't close your terminal.

Run this exact command:

```bash
eksctl create cluster \
  --name spring-boot-cluster \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.large \
  --nodes 2 \
  --nodes-min 2 \
  --nodes-max 3 \
  --managed
```

**What does this mean?**
- `--name spring-boot-cluster`: Name of your cluster
- `--region us-east-1`: Where in AWS to create it (Virginia)
- `--node-type t3.large`: Size of the computers (t3.large has 2 CPU, 8GB RAM)
- `--nodes 2`: Start with 2 computers (nodes)
- `--nodes-min 2` / `--nodes-max 3`: Can scale between 2-3 nodes
- `--managed`: AWS manages updates for you

You'll see output like this:

```
[ℹ]  eksctl version 0.162.0
[ℹ]  using region us-east-1
[ℹ]  setting availability zones to [us-east-1a us-east-1b]
[ℹ]  creating EKS cluster "spring-boot-cluster" in "us-east-1" region
...
[✔]  EKS cluster "spring-boot-cluster" in "us-east-1" region is ready
```

### Step 2: Verify Cluster Access

Run:

```bash
kubectl get nodes
```

You should see output like:

```
NAME                             STATUS   ROLES    AGE   VERSION
ip-192-168-16-86.ec2.internal    Ready    <none>   2m    v1.32.9-eks-ecaa3a6
ip-192-168-40-218.ec2.internal   Ready    <none>   2m    v1.32.9-eks-ecaa3a6
```

This shows your 2 worker nodes are running!

### Step 3: Check Running Services

Run:

```bash
kubectl get svc
```

You should see:

```
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.100.0.1   <none>        443/TCP   5m
```

Great! Your cluster is ready.

---

## Setting Up Argo CD

Argo CD is the tool that will automatically deploy your app to Kubernetes whenever you update the configuration in GitHub.

### Step 1: Install Argo CD

Run these commands:

```bash
# Create a namespace for Argo CD
kubectl create namespace argocd

# Install Argo CD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Wait about 1-2 minutes for Argo CD to start.

### Step 2: Verify Installation

Check if Argo CD pods are running:

```bash
kubectl get pods -n argocd
```

You should see several pods with STATUS `Running`:

```
NAME                                  READY   STATUS    RESTARTS   AGE
argocd-application-controller-0       1/1     Running   0          2m
argocd-dex-server-xxx                 1/1     Running   0          2m
argocd-redis-xxx                      1/1     Running   0          2m
argocd-repo-server-xxx                1/1     Running   0          2m
argocd-server-xxx                     1/1     Running   0          2m
```

### Step 3: Expose Argo CD UI

We need to access the Argo CD web interface. Run:

```bash
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
```

This changes the service type to LoadBalancer, which gives it a public URL.

Wait 2-3 minutes, then get the URL:

```bash
kubectl get svc argocd-server -n argocd
```

Look for the `EXTERNAL-IP` column. It will look like:

```
NAME            TYPE           EXTERNAL-IP
argocd-server   LoadBalancer   aa065842ebcb740c59f14cf4681206cc-652153952.us-east-1.elb.amazonaws.com
```

Copy this URL. This is your **Argo CD URL**.

### Step 4: Get Argo CD Password

The default username is `admin`. To get the password:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```

You'll see output like: `b90AA24si6ZfaTQf`

This is your **Argo CD password**. Write it down!

### Step 5: Log In to Argo CD

1. Open your browser
2. Go to: `http://YOUR-ARGOCD-URL` (from step 3)
3. Your browser will warn about security. Click **"Advanced"** then **"Proceed"** (this is safe for testing)
4. Log in with:
   - **Username**: `admin`
   - **Password**: (the password from step 4)

You should now see the Argo CD dashboard!

### Step 6: Configure Git Repository in Argo CD

We need to tell Argo CD where your Kubernetes configuration files are.

**In the Argo CD UI:**

1. Click the gear icon ⚙️ on the left sidebar (Settings)
2. Click **"Repositories"**
3. Click **"Connect Repo"** button at the top
4. Fill in:
   - **Choose your connection method**: `VIA HTTPS`
   - **Type**: `git`
   - **Repository URL**: `https://github.com/YOUR-USERNAME/devops-projects` (replace with YOUR GitHub repo)
   - Leave everything else blank (for public repos)
5. Click **"Connect"**

You should see "Connection Status: Successful"

### Step 7: Create Argo CD Application

Now we'll tell Argo CD to deploy our Spring Boot app.

**In the Argo CD UI:**

1. Click **"Applications"** in the left sidebar
2. Click **"+ New App"** button
3. Fill in:
   - **Application Name**: `spring-boot-app`
   - **Project**: `default`
   - **Sync Policy**: Select `Automatic`
   - Check the box: ✅ **Prune Resources**
   - Check the box: ✅ **Self Heal**
   - **Repository URL**: `https://github.com/YOUR-USERNAME/devops-projects`
   - **Revision**: `HEAD`
   - **Path**: `Jenkins-Zero-To-Hero/java-maven-sonar-argocd-helm-k8s/spring-boot-app-manifests`
   - **Cluster URL**: `https://kubernetes.default.svc` (should be auto-selected)
   - **Namespace**: `default`
4. Click **"Create"** at the top

You'll see the application appear. It might say "OutOfSync" at first, that's normal.

Click on the application tile, then click **"Sync"** button at the top, then **"Synchronize"**.

After 30-60 seconds, you should see green checkmarks for all resources!

---

## Configuring Jenkins Credentials

Jenkins needs credentials to:
1. Push Docker images to Docker Hub
2. Push code to GitHub

### Step 1: Access Jenkins

Open your browser and go to:
```
http://YOUR-JENKINS-IP:8080
```

Log in with your Jenkins admin credentials.

### Step 2: Add Docker Hub Credentials

1. Click **"Manage Jenkins"** in the left sidebar
2. Click **"Credentials"** (under Security section)
3. Click on **"System"** under "Stores scoped to Jenkins"
4. Click **"Global credentials (unrestricted)"**
5. Click **"+ Add Credentials"** on the left

Fill in:
- **Kind**: `Username with password`
- **Scope**: `Global`
- **Username**: Your Docker Hub username (e.g., `dmancloud`)
- **Password**: Your Docker Hub password
- **ID**: `docker-cred` (EXACTLY this - the pipeline expects this ID)
- **Description**: `Docker Hub Credentials`

Click **"Create"**.

### Step 3: Create GitHub Personal Access Token

We need a special token to let Jenkins push to GitHub.

1. Go to GitHub: https://github.com
2. Click your profile picture (top-right)
3. Click **"Settings"**
4. Scroll down and click **"Developer settings"** (bottom of left sidebar)
5. Click **"Personal access tokens"**
6. Click **"Tokens (classic)"**
7. Click **"Generate new token"** → **"Generate new token (classic)"**
8. Fill in:
   - **Note**: `Jenkins Pipeline Token`
   - **Expiration**: `90 days` (or custom)
   - **Select scopes**: Check ✅ **repo** (this checks all sub-boxes under repo)
9. Scroll down and click **"Generate token"**
10. **CRITICAL**: Copy the token shown (starts with `ghp_`). You won't be able to see it again!

Example token: `ghp_1234567890abcdef1234567890abcdef12345678`

### Step 4: Add GitHub Token to Jenkins

Back in Jenkins:

1. Go to **Manage Jenkins** → **Credentials** → **System** → **Global credentials**
2. Click **"+ Add Credentials"**
3. Fill in:
   - **Kind**: `Secret text`
   - **Scope**: `Global`
   - **Secret**: Paste your GitHub token (the `ghp_...` token)
   - **ID**: `github` (EXACTLY this)
   - **Description**: `GitHub Personal Access Token`
4. Click **"Create"**

You should now have 2 credentials: `docker-cred` and `github`.

---

## Creating the Jenkins Pipeline

### Step 1: Fork or Clone the Repository

If you haven't already, you need the code repository.

**Option A: Fork the Repository** (Recommended)

1. Go to: https://github.com/Shriram-Sutraye/devops-projects
2. Click **"Fork"** in the top-right
3. This creates a copy under your GitHub account

**Option B: Clone and Push**

```bash
cd ~/Projects
git clone https://github.com/Shriram-Sutraye/devops-projects.git
cd devops-projects
# Change the remote to your GitHub account
git remote set-url origin https://github.com/YOUR-USERNAME/devops-projects.git
git push
```

### Step 2: Update the Jenkinsfile

You need to change 2 things in the Jenkinsfile to match YOUR accounts.

1. Open the file:
   ```
   Jenkins-Zero-To-Hero/java-maven-sonar-argocd-helm-k8s/spring-boot-app/JenkinsFile
   ```

2. Find line 51 (in the "Build & Push Docker Image" stage):
   ```groovy
   sh 'docker build -t dmancloud/ultimate-cicd:${VERSION} .'
   sh 'docker push dmancloud/ultimate-cicd:${VERSION}'
   ```

3. Change `dmancloud` to YOUR Docker Hub username:
   ```groovy
   sh 'docker build -t YOUR-DOCKERHUB-USERNAME/ultimate-cicd:${VERSION} .'
   sh 'docker push YOUR-DOCKERHUB-USERNAME/ultimate-cicd:${VERSION}'
   ```

4. Find line 62 (in the "Update Deployment File" stage):
   ```groovy
   sh 'git config user.email "abc@gmail.com"'
   sh 'git config user.name "Abhishek Veeramalla"'
   ```

5. Change to YOUR email and name:
   ```groovy
   sh 'git config user.email "your-email@example.com"'
   sh 'git config user.name "Your Name"'
   ```

6. Find the git remote URL (around line 67):
   ```groovy
   sh('git push https://${GITHUB_TOKEN}@github.com/Shriram-Sutraye/devops-projects.git HEAD:master')
   ```

7. Change to YOUR GitHub username:
   ```groovy
   sh('git push https://${GITHUB_TOKEN}@github.com/YOUR-USERNAME/devops-projects.git HEAD:master')
   ```

8. **Save the file** and commit:
   ```bash
   git add .
   git commit -m "Updated Jenkinsfile with my credentials"
   git push
   ```

### Step 3: Create the Pipeline in Jenkins

1. In Jenkins, click **"New Item"** on the left
2. Enter name: `spring-boot-pipeline`
3. Select **"Pipeline"**
4. Click **"OK"**

In the configuration page:

5. Scroll down to **"Pipeline"** section
6. **Definition**: Select `Pipeline script from SCM`
7. **SCM**: Select `Git`
8. **Repository URL**: `https://github.com/YOUR-USERNAME/devops-projects`
9. **Credentials**: Leave as `- none -` (for public repos)
10. **Branch**: `*/master` (or `*/main` depending on your repo)
11. **Script Path**: `Jenkins-Zero-To-Hero/java-maven-sonar-argocd-helm-k8s/spring-boot-app/JenkinsFile`
12. Click **"Save"**

---

## Running Your First Build

### Step 1: Trigger the Build

1. On the pipeline page, click **"Build Now"** on the left

You'll see a build appear under "Build History" (e.g., #1).

### Step 2: Monitor the Build

1. Click on the build number (e.g., `#1`)
2. Click **"Console Output"** to see logs in real-time

The pipeline has these stages:
1. **Checkout**: Gets code from GitHub
2. **Build & Test**: Compiles Java code with Maven
3. **Build & Push Docker Image**: Creates container and pushes to Docker Hub
4. **Update Deployment File**: Updates Kubernetes config with new version
5. **Declarative: Post Actions**: Cleanup

A successful build shows:
```
Finished: SUCCESS
```

### Step 3: Verify Docker Image

1. Go to Docker Hub: https://hub.docker.com
2. Log in
3. Click on your repository (e.g., `ultimate-cicd`)
4. You should see a new tag (e.g., `13`)

### Step 4: Verify Argo CD Deployment

1. Go to your Argo CD UI
2. Click on the `spring-boot-app` application
3. You should see it syncing
4. After 30-60 seconds, all resources should be green and "Healthy"

---

## Fixing Service Access (LoadBalancer)

By default, the app uses NodePort which requires opening AWS Security Groups. Let's use LoadBalancer instead.

### Step 1: Update Service Configuration

On your local machine, edit the file:
```
Jenkins-Zero-To-Hero/java-maven-sonar-argocd-helm-k8s/spring-boot-app-manifests/service.yml
```

Change line 6 from:
```yaml
  type: NodePort
```

To:
```yaml
  type: LoadBalancer
```

### Step 2: Commit and Push

```bash
git add .
git commit -m "Change service type to LoadBalancer for public access"
git push
```

### Step 3: Refresh Argo CD

1. Go to Argo CD UI
2. Click on your `spring-boot-app`
3. Click the **"Refresh"** button at the top
4. Wait 30-60 seconds for it to sync

### Step 4: Get the Application URL

Run this command:

```bash
kubectl get svc spring-boot-app-service
```

Look for the `EXTERNAL-IP`:

```
NAME                      TYPE           EXTERNAL-IP
spring-boot-app-service   LoadBalancer   a6ee7c973c6b24cdea8b5e5ac8e69124-654243913.us-east-1.elb.amazonaws.com
```

**Wait 2-3 minutes** for AWS to finish setting up the Load Balancer.

---

## Verifying the Complete Pipeline

### Step 1: Access Your Application

Open your browser and go to:
```
http://YOUR-LOADBALANCER-URL
```

(Use the EXTERNAL-IP from the previous step)

You should see:

```
Jenkins Zero to Hero Pipeline is COMPLETE!
This update was deployed automatically by Jenkins, Docker Hub, and Argo CD!
```

### Step 2: Test the CI/CD Pipeline

Let's make a change and watch it auto-deploy!

1. Edit the file:
   ```
   Jenkins-Zero-To-Hero/java-maven-sonar-argocd-helm-k8s/spring-boot-app/src/main/resources/templates/index.html
   ```

2. Change the message (around line 15):
   ```html
   <h1 class="display-4">Jenkins Zero to Hero Pipeline is COMPLETE!</h1>
   ```

   To:
   ```html
   <h1 class="display-4">I BUILT THIS MYSELF! 🚀</h1>
   ```

3. Commit and push:
   ```bash
   git add .
   git commit -m "Updated welcome message"
   git push
   ```

4. Watch Jenkins:
   - Go to Jenkins
   - You should see a new build start automatically (if you set up webhooks)
   - Or click "Build Now" manually
   - Wait for it to complete

5. Watch Argo CD:
   - Go to Argo CD
   - Click "Refresh" on your app
   - Watch it sync

6. Refresh your browser:
   - Reload your app URL
   - You should see: **"I BUILT THIS MYSELF! 🚀"**

**CONGRATULATIONS! Your CI/CD pipeline is working end-to-end!**

---

## Troubleshooting Common Issues

### Issue 1: Build Fails with "Permission denied" in Git

**Symptom**: Jenkins build fails with:
```
Permission denied warning: failed to remove target/...
```

**Solution**:
1. Go to Jenkins
2. Click **"Manage Jenkins"** → **"Script Console"**
3. Run this script:
   ```groovy
   def jobName = "spring-boot-pipeline"
   def job = Jenkins.instance.getItem(jobName)
   def workspacePath = job.getBuildByNumber(1).getWorkspace().getRemote()
   new File(workspacePath).deleteDir()
   println "Deleted workspace: ${workspacePath}"
   ```
4. Click **"Run"**
5. Try building again

### Issue 2: Can't Access Application (Connection Timeout)

**Symptom**: Browser shows "Connection timed out" when accessing app URL

**Possible Causes**:

**A) LoadBalancer not ready yet**
- Wait 3-5 minutes after creating the LoadBalancer
- Run: `kubectl get svc spring-boot-app-service`
- Make sure EXTERNAL-IP doesn't say `<pending>`

**B) Service type is still NodePort**
- Check: `kubectl get svc spring-boot-app-service`
- If TYPE is `NodePort`, change it to `LoadBalancer` (see [Fixing Service Access](#fixing-service-access-loadbalancer))

**C) Pods not running**
- Run: `kubectl get pods`
- If STATUS is not `Running`, check logs: `kubectl logs <pod-name>`

### Issue 3: Argo CD Shows "OutOfSync"

**Symptom**: Argo CD application shows red "OutOfSync" status

**Solution**:
1. Click on the application
2. Click **"Sync"** button at the top
3. Click **"Synchronize"**
4. If it shows conflicts, select **"Replace"** and sync again

### Issue 4: Jenkins Can't Push to GitHub

**Symptom**: Build fails with:
```
fatal: could not read Username for 'https://github.com': No such device or address
```

**Solution**:
1. Make sure you created the GitHub token (see [Step 3: Create GitHub Personal Access Token](#step-3-create-github-personal-access-token))
2. Verify the credential ID is exactly `github` in Jenkins
3. Check the Jenkinsfile uses the correct GitHub username

### Issue 5: Docker Push Fails

**Symptom**: Build fails with:
```
denied: requested access to the resource is denied
```

**Solution**:
1. Verify Docker Hub credentials in Jenkins are correct
2. Make sure the credential ID is exactly `docker-cred`
3. Check that your Docker Hub username in the Jenkinsfile matches your actual Docker Hub account
4. Ensure the repository exists in Docker Hub (create it if needed)

### Issue 6: EKS Cluster Creation Fails

**Symptom**:
```
Error: failed to create cluster: unable to create stack: AlreadyExistsException
```

**Solution**:
1. A cluster with that name already exists
2. Either delete the old one:
   ```bash
   eksctl delete cluster --name spring-boot-cluster --region us-east-1
   ```
3. Or use a different name in the create command

### Issue 7: kubectl Commands Don't Work

**Symptom**:
```
The connection to the server localhost:8080 was refused
```

**Solution**:
1. Update your kubeconfig:
   ```bash
   aws eks update-kubeconfig --name spring-boot-cluster --region us-east-1
   ```
2. Verify:
   ```bash
   kubectl get nodes
   ```

---

## Cleanup (When You're Done)

To avoid AWS charges, delete everything:

### 1. Delete EKS Cluster
```bash
eksctl delete cluster --name spring-boot-cluster --region us-east-1
```

This takes 10-15 minutes and deletes:
- The EKS cluster
- All worker nodes
- Load Balancers
- Associated networking

### 2. Verify Deletion

Check in AWS Console:
1. Go to EC2 → Load Balancers (should be empty)
2. Go to EKS → Clusters (should be empty)

---

## Summary of What You Built

✅ **Kubernetes Cluster** on AWS EKS  
✅ **Jenkins Pipeline** that builds and tests code  
✅ **Docker Images** automatically created and pushed  
✅ **Argo CD** automatically deploying to Kubernetes  
✅ **Live Application** accessible from anywhere  
✅ **Complete CI/CD** from code push to production  

**You now have professional DevOps skills!** 🎉

---

## Next Steps

To improve this setup:
1. **Add SSL/HTTPS** using cert-manager and Let's Encrypt
2. **Set up monitoring** with Prometheus and Grafana
3. **Add SonarQube** for code quality checks
4. **Implement staging environment** for testing before production
5. **Configure GitHub webhooks** so builds trigger automatically on push
6. **Add database** like PostgreSQL to Kubernetes
7. **Set up alerting** with PagerDuty or Slack notifications

---

## Useful Commands Reference

```bash
# Kubernetes
kubectl get pods                    # List all pods
kubectl get svc                     # List all services
kubectl get nodes                   # List cluster nodes
kubectl logs <pod-name>             # View pod logs
kubectl describe pod <pod-name>     # Detailed pod info
kubectl delete pod <pod-name>       # Delete a pod

# Argo CD (CLI - optional)
argocd app list                     # List applications
argocd app sync spring-boot-app     # Manually sync app
argocd app get spring-boot-app      # Get app details

# AWS EKS
eksctl get cluster                  # List your clusters
eksctl get nodegroup --cluster spring-boot-cluster  # List node groups
aws eks update-kubeconfig --name spring-boot-cluster --region us-east-1  # Update config

# Git
git status                          # Check changes
git add .                           # Stage all changes
git commit -m "message"             # Commit changes
git push                            # Push to GitHub

# Docker
docker ps                           # List running containers
docker images                       # List images
docker build -t name:tag .          # Build image
docker push name:tag                # Push to Docker Hub
```

---

**Document Version**: 1.0  
**Last Updated**: January 2026  
**Tested On**: Ubuntu 22.04, macOS Sonoma, Windows 11  

**Questions?** Check the Troubleshooting section or Google the specific error message.

**Good luck, and happy deploying!** 🚀
