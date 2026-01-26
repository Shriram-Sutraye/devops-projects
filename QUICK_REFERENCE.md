# CI/CD Pipeline Quick Reference

## ⚡ Quick Start Commands

### Check Everything is Running
```bash
# Check Kubernetes nodes
kubectl get nodes

# Check all pods
kubectl get pods -A

# Check services
kubectl get svc

# Check Argo CD status
kubectl get pods -n argocd
```

### Get Important URLs
```bash
# Get Argo CD URL
kubectl get svc argocd-server -n argocd | grep LoadBalancer

# Get Application URL
kubectl get svc spring-boot-app-service | grep LoadBalancer

# Get Argo CD Password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```

### Trigger a New Build
1. Make code changes
2. Commit: `git add . && git commit -m "your message"`
3. Push: `git push`
4. Go to Jenkins and click "Build Now"
5. Check Argo CD to see it sync

---

## 🔧 Key Configuration Files

| File | Purpose | Location |
|------|---------|----------|
| **JenkinsFile** | Defines the CI pipeline | `Jenkins-Zero-To-Hero/java-maven-sonar-argocd-helm-k8s/spring-boot-app/JenkinsFile` |
| **deployment.yml** | Kubernetes deployment config | `Jenkins-Zero-To-Hero/java-maven-sonar-argocd-helm-k8s/spring-boot-app-manifests/deployment.yml` |
| **service.yml** | Kubernetes service config (LoadBalancer) | `Jenkins-Zero-To-Hero/java-maven-sonar-argocd-helm-k8s/spring-boot-app-manifests/service.yml` |
| **pom.xml** | Maven build configuration | `Jenkins-Zero-To-Hero/java-maven-sonar-argocd-helm-k8s/spring-boot-app/pom.xml` |

---

## 🎯 Important Credential IDs

| Where | ID | Type | Purpose |
|-------|----|----|---------|
| Jenkins | `docker-cred` | Username/Password | Docker Hub access |
| Jenkins | `github` | Secret Text | GitHub Personal Access Token |

**⚠️ CRITICAL**: These IDs must match exactly in both Jenkins and the Jenkinsfile!

---

## 📋 Pipeline Stages

```
1. Checkout → Pulls code from GitHub
2. Build & Test → Compiles with Maven, runs tests
3. Build & Push Docker Image → Creates container, pushes to Docker Hub
4. Update Deployment File → Updates Kubernetes manifest with new version
5. (Argo CD Auto-Syncs) → Deploys to Kubernetes
```

---

## 🔄 The Complete Flow

```
Developer → GitHub Push
      ↓
Jenkins Detects Change (webhook or manual)
      ↓
Jenkins Builds & Tests Code
      ↓
Jenkins Creates Docker Image (tagged with build number)
      ↓
Jenkins Pushes to Docker Hub
      ↓
Jenkins Updates deployment.yml in GitHub (new image version)
      ↓
Argo CD Detects GitHub Change
      ↓
Argo CD Pulls New Manifest
      ↓
Argo CD Applies to Kubernetes
      ↓
Kubernetes Pulls New Docker Image
      ↓
App is Live! 🎉
```

---

## 🚨 Common Issues: Quick Fixes

### Jenkins Build Fails: "Permission Denied"
```bash
# SSH into Jenkins server
ssh -i jenkins.pem ubuntu@YOUR-JENKINS-IP

# Remove workspace
sudo rm -rf /var/lib/jenkins/workspace/spring-boot-pipeline

# Rebuild in Jenkins
```

### Can't Access App URL
```bash
# Check if LoadBalancer is ready
kubectl get svc spring-boot-app-service

# If EXTERNAL-IP is <pending>, wait 2-3 minutes
# If it stays pending, check:
kubectl describe svc spring-boot-app-service
```

### Argo CD Shows OutOfSync
1. Go to Argo CD UI
2. Click the app
3. Click "Sync" → "Synchronize"

### Docker Push Fails
1. Check Docker Hub credentials in Jenkins
2. Verify credential ID is `docker-cred`
3. Make sure repository exists in Docker Hub

---

## 💰 AWS Costs

| Resource | Cost | How to Minimize |
|----------|------|-----------------|
| EKS Control Plane | ~$0.10/hour ($73/month) | Delete cluster when not using |
| EC2 Instances (t3.large x2) | ~$0.17/hour ($245/month total) | Use t3.small or delete cluster |
| Load Balancers (x2) | ~$0.05/hour ($36/month each) | Delete when not using |
| **Total** | ~**$0.37/hour** (~$270/month) | **Delete everything after testing!** |

### Delete Everything:
```bash
eksctl delete cluster --name spring-boot-cluster --region us-east-1
```

This command deletes: EKS cluster, worker nodes, load balancers, VPC, everything!

---

## 🔐 Credentials You'll Need

| Service | What | Format | Purpose |
|---------|------|--------|---------|
| **AWS** | Access Key ID | `AKIAIOSFODNN7EXAMPLE` | AWS CLI access |
| **AWS** | Secret Access Key | `wJalrXUtnFE...` | AWS CLI access |
| **GitHub** | Personal Access Token | `ghp_1234567890abcd...` | Jenkins push to GitHub |
| **Docker Hub** | Username | `your-username` | Push images |
| **Docker Hub** | Password | Your password | Push images |
| **Argo CD** | Username | `admin` | Access dashboard |
| **Argo CD** | Password | Generated | Access dashboard |

---

## 📱 URLs You'll Need

| Service | URL Format | Example |
|---------|------------|---------|
| **Jenkins** | `http://JENKINS-IP:8080` | `http://13.222.248.55:8080` |
| **Argo CD** | `http://ARGOCD-ELB-URL` | `http://aa065842...elb.amazonaws.com` |
| **Your App** | `http://APP-ELB-URL` | `http://a6ee7c973...elb.amazonaws.com` |
| **Docker Hub** | `https://hub.docker.com/r/USERNAME/ultimate-cicd` | - |

---

## ✅ Pre-Flight Checklist

Before running the pipeline, verify:

- [ ] AWS CLI configured: `aws sts get-caller-identity`
- [ ] kubectl installed: `kubectl version --client`
- [ ] eksctl installed: `eksctl version`
- [ ] EKS cluster running: `kubectl get nodes`
- [ ] Argo CD deployed: `kubectl get pods -n argocd`
- [ ] Jenkins credentials added: `docker-cred` and `github`
- [ ] Jenkinsfile updated with YOUR username
- [ ] GitHub repo forked/cloned
- [ ] Docker Hub account created

---

## 🎓 What Each Tool Does

| Tool | Purpose | Analogy |
|------|---------|---------|
| **Jenkins** | Automates building and testing code | The factory worker who builds your product |
| **Docker** | Packages app into a container | The shipping box that holds your product |
| **Docker Hub** | Stores Docker images | The warehouse that stores boxes |
| **Kubernetes (EKS)** | Runs and manages containers | The fleet of trucks delivering your product |
| **Argo CD** | Watches GitHub and deploys changes | The supervisor who checks for new updates |
| **GitHub** | Stores code and configs | The blueprint storage |
| **AWS** | Provides the cloud infrastructure | The land where everything is built |

---

## 📖 File Structure

```
devops-projects/
└── Jenkins-Zero-To-Hero/
    └── java-maven-sonar-argocd-helm-k8s/
        ├── spring-boot-app/              # The application code
        │   ├── src/                      # Java source code
        │   ├── pom.xml                   # Maven build file
        │   ├── Dockerfile                # How to containerize the app
        │   └── JenkinsFile               # CI pipeline definition
        └── spring-boot-app-manifests/    # Kubernetes configs
            ├── deployment.yml            # How to run on K8s
            └── service.yml               # How to expose the app
```

---

## 🔧 Customization Points

### Change App Message
Edit: `spring-boot-app/src/main/resources/templates/index.html`

### Change Docker Image Name
Edit: Line 51 in `JenkinsFile`
```groovy
sh 'docker build -t YOUR-USERNAME/YOUR-APP-NAME:${VERSION} .'
```

### Change Number of Replicas
Edit: `spring-boot-app-manifests/deployment.yml`
```yaml
replicas: 2  # Change to 3, 4, etc.
```

### Change Node Type or Count
When creating cluster:
```bash
eksctl create cluster --node-type t3.medium --nodes 3
```

---

## 🎯 Testing the Pipeline

### Step 1: Make a Simple Change
```bash
cd Jenkins-Zero-To-Hero/java-maven-sonar-argocd-helm-k8s/spring-boot-app
echo "<!-- test -->" >> src/main/resources/templates/index.html
git add .
git commit -m "Test pipeline"
git push
```

### Step 2: Watch It Deploy
1. Jenkins: Watch build progress
2. Docker Hub: See new image with build number
3. GitHub: See deployment.yml updated with new version
4. Argo CD: Watch it sync
5. Browser: Refresh app URL (no visible change, but new version)

---

## 💡 Pro Tips

1. **Always check logs**: `kubectl logs <pod-name>`
2. **Use describe for debugging**: `kubectl describe pod <pod-name>`
3. **Set up webhooks**: Auto-trigger builds on push (Google: "Jenkins GitHub webhook")
4. **Use separate branches**: dev, staging, production
5. **Tag releases**: Use meaningful semver tags (v1.0.0, v1.1.0)
6. **Monitor costs**: Set up AWS billing alerts
7. **Back up configs**: Save all yamls and commands
8. **Document changes**: Write clear commit messages

---

## 🆘 Emergency Commands

### App is Down
```bash
# Check pods
kubectl get pods

# If pod is CrashLoopBackOff
kubectl logs <pod-name>
kubectl describe pod <pod-name>

# Force restart
kubectl rollout restart deployment spring-boot-app
```

### Completely Reset
```bash
# Delete everything in Argo CD
kubectl delete application spring-boot-app -n argocd

# Delete app from Kubernetes
kubectl delete deployment spring-boot-app
kubectl delete svc spring-boot-app-service

# Recreate in Argo CD UI
```

### Rollback to Previous Version
```bash
# See deployment history
kubectl rollout history deployment spring-boot-app

# Rollback
kubectl rollout undo deployment spring-boot-app
```

---

**Keep this file handy for quick reference!** 📌

For detailed instructions, see: [COMPLETE_CICD_PIPELINE_GUIDE.md](./COMPLETE_CICD_PIPELINE_GUIDE.md)
