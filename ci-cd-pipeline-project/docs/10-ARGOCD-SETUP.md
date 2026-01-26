# 10 - Argo CD & GitOps Setup

This guide covers installing Argo CD and deploying the application using GitOps.

---

## 📋 What We Built

- **Argo CD URL:** https://aa065842ebcb740c59f14cf4681206cc-652153952.us-east-1.elb.amazonaws.com
- **Username:** `admin`
- **Password:** `b90AA24si6ZfaTQf` (Initial password)
- **Deployment Strategy:** GitOps (Argo CD watches GitHub → Syncs to EKS)

---

## 🚀 Step 1: Install Argo CD

We installed Argo CD on the EKS cluster:

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

And exposed it via LoadBalancer:

```bash
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
```

---

## 🔗 Step 2: Connect to GitHub

We created an Application manifest (`argocd-app.yaml`) that tells Argo CD:
1. **Source:** Your GitHub Repo (`Jenkins-Zero-To-Hero/.../spring-boot-app-manifests`)
2. **Destination:** Your EKS Cluster (`default` namespace)
3. **Policy:** Auto-sync & Self-heal

---

## ✅ Step 3: Verify Deployment

### In Argo CD UI
1. Go to the URL above
2. Log in with `admin` / `b90AA24si6ZfaTQf`
3. You should see `spring-boot-app` is **Healthy** and **Synced**

### In Kubernetes
```bash
kubectl get pods
```
**Expected Output:**
```
NAME                               READY   STATUS    RESTARTS   AGE
spring-boot-app-54848f6854-xxxxx   1/1     Running   0          2m
spring-boot-app-54848f6854-yyyyy   1/1     Running   0          2m
```

---

## 🔄 The Full GitOps Flow

1. You **push code** to GitHub
2. **Jenkins** builds Docker image & updates `deployment.yml` in GitHub
3. **Argo CD** detects the change in GitHub
4. **Argo CD** updates Kubernetes to match
5. **Kubernetes** pulls the new Docker image
6. **New Version Live!** (Zero manual work)
